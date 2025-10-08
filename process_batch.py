"""
Script to process a batch of PDF files for testing
"""

import os
import sys
import time
from app import app, db
from services.document_service import DocumentService
from config import Config

def process_test_files():
    """Process all PDF files in the upload folder"""
    with app.app_context():
        service = DocumentService()
        
        # Check if folder exists and has files
        if not os.path.exists(Config.UPLOAD_FOLDER):
            print(f"Error: Upload folder not found: {Config.UPLOAD_FOLDER}")
            return
        
        pdf_files = [f for f in os.listdir(Config.UPLOAD_FOLDER) if f.lower().endswith('.pdf')]
        
        if not pdf_files:
            print(f"No PDF files found in {Config.UPLOAD_FOLDER}")
            return
        
        print(f"Found {len(pdf_files)} PDF files to process\n")
        print("=" * 60)
        
        start_time = time.time()
        processed = 0
        errors = 0
        
        for i, filename in enumerate(pdf_files, 1):
            print(f"\n[{i}/{len(pdf_files)}] Processing: {filename}")
            file_path = os.path.join(Config.UPLOAD_FOLDER, filename)
            
            try:
                doc_id = service.process_single_document(file_path, filename)
                if doc_id:
                    processed += 1
                    print(f"  ✓ Successfully processed (ID: {doc_id})")
                else:
                    errors += 1
                    print(f"  ✗ Failed to process")
            except Exception as e:
                errors += 1
                print(f"  ✗ Error: {e}")
        
        elapsed_time = time.time() - start_time
        
        print("\n" + "=" * 60)
        print(f"Processing completed in {elapsed_time:.2f} seconds")
        print(f"Processed: {processed}")
        print(f"Errors: {errors}")
        print("=" * 60)
        
        # Show statistics
        stats = service.get_statistics()
        print("\nCurrent Statistics:")
        print(f"  Total documents: {stats['total']}")
        print(f"  Pending: {stats['pending']}")
        print(f"  Classified: {stats['classified']}")
        print(f"  Validated: {stats['validated']}")
        print(f"  Errors: {stats['errors']}")
        
        if stats['by_type']:
            print("\nBy Type:")
            for doc_type, count in stats['by_type'].items():
                print(f"  {doc_type}: {count}")

if __name__ == '__main__':
    print("PDF Classifier - Batch Processing")
    print("=" * 60)
    process_test_files()
