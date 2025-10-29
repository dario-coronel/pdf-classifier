import os
import shutil
from datetime import datetime
from typing import List, Optional, Dict
from werkzeug.utils import secure_filename
from models import db
from models.document import Document, DocumentType, ProcessingLog, MLTrainingData
from services.pdf_processor import PDFProcessor
from services.classifier import DocumentClassifier
from config import Config


class DocumentService:
    """Service for document processing and management"""
    
    def __init__(self):
        self.pdf_processor = PDFProcessor()
        self.classifier = DocumentClassifier()
    
    def process_pending_documents(self) -> List[int]:
        """Process all pending documents in upload folder"""
        processed_ids = []
        
        # Get all PDF files in upload folder
        if not os.path.exists(Config.UPLOAD_FOLDER):
            return processed_ids
        
        for filename in os.listdir(Config.UPLOAD_FOLDER):
            if filename.lower().endswith('.pdf'):
                file_path = os.path.join(Config.UPLOAD_FOLDER, filename)
                try:
                    doc_id = self.process_single_document(file_path, filename)
                    if doc_id:
                        processed_ids.append(doc_id)
                except Exception as e:
                    print(f"Error processing {filename}: {e}")
        
        return processed_ids
    
    def process_single_document(self, file_path: str, original_filename: str) -> Optional[int]:
        """Process a single document"""
        try:
            # Check if document already exists
            existing = Document.query.filter_by(original_filename=original_filename).first()
            if existing:
                print(f"Document {original_filename} already exists")
                return existing.id

            # Normalize filename
            safe_filename = secure_filename(original_filename)
            pending_folder = Config.UPLOAD_FOLDER
            safe_file_path = os.path.join(pending_folder, safe_filename)

            # If the file_path is not the same as the safe_file_path, rename/move it
            if os.path.abspath(file_path) != os.path.abspath(safe_file_path):
                if not os.path.exists(safe_file_path):
                    os.rename(file_path, safe_file_path)
                file_path = safe_file_path

            # Create document record
            doc = Document(
                filename=safe_filename,
                original_filename=original_filename,
                file_path=file_path,
                file_size=os.path.getsize(file_path),
                status='analyzing'
            )
            db.session.add(doc)
            db.session.commit()
            
            # Log processing start
            self._log_action(doc.id, 'processing_started', 'Document processing initiated')
            
            # Extract text
            print(f"Extracting text from {original_filename}...")
            extracted_text, is_ocr = self.pdf_processor.extract_text(file_path)
            doc.extracted_text = extracted_text
            
            # Extract metadata
            print(f"Extracting metadata...")
            metadata = self.pdf_processor.extract_metadata(extracted_text)
            doc.cuit = metadata.get('cuit')
            doc.provider = metadata.get('provider')
            doc.document_number = metadata.get('document_number')
            doc.total_amount = metadata.get('total_amount')
            
            if metadata.get('document_date'):
                try:
                    doc.document_date = datetime.strptime(metadata['document_date'], '%Y-%m-%d').date()
                except:
                    pass
            
            # Classify document
            print(f"Classifying document...")
            predicted_type, confidence = self.classifier.classify(extracted_text)
            
            # Get document type ID
            doc_type = DocumentType.query.filter_by(name=predicted_type).first()
            if doc_type:
                doc.predicted_type_id = doc_type.id
                doc.document_type_id = doc_type.id  # Default to predicted
                doc.confidence_score = confidence
            
            doc.status = 'classified'
            doc.processed_at = datetime.utcnow()
            
            db.session.commit()
            
            # Log success
            self._log_action(
                doc.id, 
                'processing_completed',
                f"Classified as {predicted_type} with {confidence:.2%} confidence"
            )
            
            print(f"✓ Document {original_filename} processed successfully as {predicted_type}")
            return doc.id
            
        except Exception as e:
            print(f"Error processing document: {e}")
            if 'doc' in locals():
                doc.status = 'error'
                doc.error_message = str(e)
                db.session.commit()
                self._log_action(doc.id, 'processing_error', str(e))
            return None
    
    def validate_document(self, document_id: int, validated_type: str, user: str = 'system') -> bool:
        """Validate and move document to classified folder"""
        try:
            doc = Document.query.get(document_id)
            if not doc:
                return False
            
            # Update document type
            doc_type = DocumentType.query.filter_by(name=validated_type).first()
            if not doc_type:
                return False
            
            doc.document_type_id = doc_type.id
            doc.is_validated = True
            doc.validated_by = user
            doc.validated_at = datetime.utcnow()
            doc.status = 'validated'
            
            # Move file to classified folder
            destination_folder = os.path.join(Config.CLASSIFIED_FOLDER, validated_type)
            os.makedirs(destination_folder, exist_ok=True)
            
            new_path = os.path.join(destination_folder, doc.filename)
            
            if os.path.exists(doc.file_path):
                shutil.move(doc.file_path, new_path)
                doc.file_path = new_path
            
            # Save training data
            training_data = MLTrainingData(
                document_id=doc.id,
                text_features=doc.extracted_text[:5000],  # Limit size
                correct_type_id=doc_type.id
            )
            db.session.add(training_data)
            
            db.session.commit()
            
            # Log validation
            self._log_action(
                doc.id,
                'document_validated',
                f"Validated as {validated_type} by {user}"
            )
            
            return True
            
        except Exception as e:
            print(f"Error validating document: {e}")
            db.session.rollback()
            return False
    
    def validate_batch(self, validations: List[Dict]) -> int:
        """Validate multiple documents at once"""
        success_count = 0
        
        for validation in validations:
            doc_id = validation.get('document_id')
            doc_type = validation.get('document_type')
            user = validation.get('user', 'system')
            
            if self.validate_document(doc_id, doc_type, user):
                success_count += 1
        
        # Optionally retrain model after batch validation
        if success_count >= 10:
            self.retrain_model()
        
        return success_count
    
    def search_documents(self, filters: Dict) -> List[Document]:
        """Search documents with filters"""
        query = Document.query
        
        # Filter by document type
        if filters.get('document_type'):
            doc_type = DocumentType.query.filter_by(name=filters['document_type']).first()
            if doc_type:
                query = query.filter(Document.document_type_id == doc_type.id)
        
        # Filter by date range
        if filters.get('date_from'):
            query = query.filter(Document.document_date >= filters['date_from'])
        
        if filters.get('date_to'):
            query = query.filter(Document.document_date <= filters['date_to'])
        
        # Filter by CUIT
        if filters.get('cuit'):
            query = query.filter(Document.cuit.like(f"%{filters['cuit']}%"))
        
        # Filter by provider
        if filters.get('provider'):
            query = query.filter(Document.provider.like(f"%{filters['provider']}%"))
        
        # Filter by status
        if filters.get('status'):
            query = query.filter(Document.status == filters['status'])
        
        # Order by date
        query = query.order_by(Document.created_at.desc())
        
        # Limit results
        limit = filters.get('limit', 100)
        return query.limit(limit).all()
    
    def get_statistics(self) -> Dict:
        """Get processing statistics"""
        total_docs = Document.query.count()
        pending_docs = Document.query.filter_by(status='pending').count()
        classified_docs = Document.query.filter_by(status='classified').count()
        validated_docs = Document.query.filter_by(is_validated=True).count()
        error_docs = Document.query.filter_by(status='error').count()


        # Statistics by type (all docs)
        type_stats = (
            db.session.query(
                DocumentType.name,
                db.func.count(Document.id)
            )
            .join(Document, Document.document_type_id == DocumentType.id)
            .group_by(DocumentType.name)
            .all()
        )

        # Statistics by type (only validated)
        validated_type_stats = (
            db.session.query(
                DocumentType.name,
                db.func.count(Document.id)
            )
            .join(Document, Document.document_type_id == DocumentType.id)
            .filter(Document.is_validated == True)
            .group_by(DocumentType.name)
            .all()
        )

        # Statistics by type (not validated)
        not_validated_type_stats = (
            db.session.query(
                DocumentType.name,
                db.func.count(Document.id)
            )
            .join(Document, Document.document_type_id == DocumentType.id)
            .filter((Document.is_validated == False) | (Document.is_validated == None))
            .group_by(DocumentType.name)
            .all()
        )

        return {
            'total': total_docs,
            'pending': pending_docs,
            'classified': classified_docs,
            'validated': validated_docs,
            'errors': error_docs,
            'by_type': dict(type_stats),
            'validated_by_type': dict(validated_type_stats),
            'not_validated_by_type': dict(not_validated_type_stats)
        }
    
    def retrain_model(self) -> bool:
        """Retrain ML model with validated documents"""
        try:
            # Get validated training data
            training_data = db.session.query(
                MLTrainingData, DocumentType.name
            ).join(DocumentType, MLTrainingData.correct_type_id == DocumentType.id)\
             .filter(MLTrainingData.used_for_training == False)\
             .limit(1000).all()
            
            if len(training_data) < 10:
                print("Not enough new training data")
                return False
            
            # Prepare data
            documents_data = [
                {
                    'text': data.text_features,
                    'type': type_name
                }
                for data, type_name in training_data
            ]
            
            # Retrain
            success = self.classifier.retrain(documents_data)
            
            if success:
                # Save model
                self.classifier.save_model()
                
                # Mark data as used
                for data, _ in training_data:
                    data.used_for_training = True
                db.session.commit()
                
                print("Model retrained successfully")
            
            return success
            
        except Exception as e:
            print(f"Error retraining model: {e}")
            return False
    
    def _log_action(self, document_id: int, action: str, details: str = None):
        """Log document processing action"""
        try:
            log = ProcessingLog(
                document_id=document_id,
                action=action,
                details=details
            )
            db.session.add(log)
            db.session.commit()
        except Exception as e:
            print(f"Error logging action: {e}")
