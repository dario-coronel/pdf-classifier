"""
Initialization script for PDF Classifier
Creates necessary directories and initializes the database
"""

import os
import sys
from config import Config

def create_directories():
    """Create all necessary directories"""
    directories = [
        Config.UPLOAD_FOLDER,
        Config.CLASSIFIED_FOLDER,
        Config.TEMP_FOLDER,
        os.path.join(Config.BASE_DIR, 'models')
    ]
    
    # Add subdirectories for each document type
    for doc_type in Config.DOCUMENT_TYPES:
        directories.append(os.path.join(Config.CLASSIFIED_FOLDER, doc_type))
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✓ Created directory: {directory}")

def initialize_database():
    """Initialize database tables"""
    from app import app, db
    
    with app.app_context():
        try:
            db.create_all()
            print("✓ Database tables created successfully")
            
            # Check if document types exist
            from models.document import DocumentType
            existing_types = DocumentType.query.count()
            
            if existing_types == 0:
                print("⚠ Warning: No document types found in database")
                print("  Please run the SQL schema file: database/schema.sql")
            else:
                print(f"✓ Found {existing_types} document types in database")
            
        except Exception as e:
            print(f"✗ Error initializing database: {e}")
            sys.exit(1)

def check_dependencies():
    """Check if all required dependencies are installed"""
    dependencies = {
        'flask': 'Flask',
        'flask_sqlalchemy': 'Flask-SQLAlchemy',
        'PyPDF2': 'PyPDF2',
        'pdfplumber': 'pdfplumber',
        'PIL': 'Pillow',
        'pytesseract': 'pytesseract',
        'sklearn': 'scikit-learn',
        'pandas': 'pandas',
        'numpy': 'numpy'
    }
    
    print("\nChecking dependencies...")
    missing = []
    
    for module, package in dependencies.items():
        try:
            __import__(module)
            print(f"✓ {package}")
        except ImportError:
            print(f"✗ {package} - NOT FOUND")
            missing.append(package)
    
    if missing:
        print(f"\n⚠ Missing dependencies: {', '.join(missing)}")
        print("Run: pip install -r requirements.txt")
        sys.exit(1)

def check_tesseract():
    """Check if Tesseract is installed"""
    print("\nChecking Tesseract OCR...")
    
    if os.path.exists(Config.TESSERACT_PATH):
        print(f"✓ Tesseract found at: {Config.TESSERACT_PATH}")
    else:
        print(f"⚠ Tesseract not found at: {Config.TESSERACT_PATH}")
        print("  Please install Tesseract OCR and update the path in .env")

def main():
    """Main initialization function"""
    print("=" * 60)
    print("PDF Classifier - Initialization")
    print("=" * 60)
    
    print("\n[1/4] Checking dependencies...")
    check_dependencies()
    
    print("\n[2/4] Checking Tesseract OCR...")
    check_tesseract()
    
    print("\n[3/4] Creating directories...")
    create_directories()
    
    print("\n[4/4] Initializing database...")
    initialize_database()
    
    print("\n" + "=" * 60)
    print("✓ Initialization completed successfully!")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Ensure MySQL is running")
    print("2. Import database/schema.sql into MySQL")
    print("3. Copy PDF files to uploads/pending/")
    print("4. Run: python app.py")
    print("\nAccess the application at: http://localhost:5000")
    print("=" * 60)

if __name__ == '__main__':
    main()
