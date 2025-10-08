from datetime import datetime
from models import db


class DocumentType(db.Model):
    __tablename__ = 'document_types'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    documents = db.relationship('Document', foreign_keys='Document.document_type_id', backref='document_type', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'is_active': self.is_active
        }


class Document(db.Model):
    __tablename__ = 'documents'
    
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    original_filename = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.String(500), nullable=False)
    file_size = db.Column(db.BigInteger)
    
    document_type_id = db.Column(db.Integer, db.ForeignKey('document_types.id'))
    predicted_type_id = db.Column(db.Integer, db.ForeignKey('document_types.id'))
    confidence_score = db.Column(db.Numeric(5, 4))
    
    status = db.Column(db.Enum('pending', 'analyzing', 'classified', 'validated', 'error'), default='pending')
    is_validated = db.Column(db.Boolean, default=False)
    validated_by = db.Column(db.String(100))
    validated_at = db.Column(db.DateTime)
    
    # Extracted information
    extracted_text = db.Column(db.Text)
    cuit = db.Column(db.String(20))
    provider = db.Column(db.String(200))
    document_date = db.Column(db.Date)
    document_number = db.Column(db.String(100))
    total_amount = db.Column(db.Numeric(15, 2))
    
    # Metadata
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    processed_at = db.Column(db.DateTime)
    error_message = db.Column(db.Text)
    
    # Relationships
    predicted_type = db.relationship('DocumentType', foreign_keys=[predicted_type_id])
    logs = db.relationship('ProcessingLog', backref='document', lazy=True, cascade='all, delete-orphan')
    training_data = db.relationship('MLTrainingData', backref='document', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'filename': self.filename,
            'original_filename': self.original_filename,
            'file_size': self.file_size,
            'document_type': self.document_type.name if self.document_type else None,
            'predicted_type': self.predicted_type.name if self.predicted_type else None,
            'confidence_score': float(self.confidence_score) if self.confidence_score else None,
            'status': self.status,
            'is_validated': self.is_validated,
            'cuit': self.cuit,
            'provider': self.provider,
            'document_date': self.document_date.isoformat() if self.document_date else None,
            'document_number': self.document_number,
            'total_amount': float(self.total_amount) if self.total_amount else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'processed_at': self.processed_at.isoformat() if self.processed_at else None
        }


class ProcessingLog(db.Model):
    __tablename__ = 'processing_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    document_id = db.Column(db.Integer, db.ForeignKey('documents.id'))
    action = db.Column(db.String(100), nullable=False)
    details = db.Column(db.Text)
    user = db.Column(db.String(100))
    ip_address = db.Column(db.String(45))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class MLTrainingData(db.Model):
    __tablename__ = 'ml_training_data'
    
    id = db.Column(db.Integer, primary_key=True)
    document_id = db.Column(db.Integer, db.ForeignKey('documents.id'))
    text_features = db.Column(db.Text)
    correct_type_id = db.Column(db.Integer, db.ForeignKey('document_types.id'))
    used_for_training = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    correct_type = db.relationship('DocumentType', foreign_keys=[correct_type_id])
