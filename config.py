import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Base configuration"""
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    # Database
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_PORT = os.getenv('DB_PORT', '3306')
    DB_USER = os.getenv('DB_USER', 'root')
    DB_PASSWORD = os.getenv('DB_PASSWORD', '')
    DB_NAME = os.getenv('DB_NAME', 'pdf_classifier')
    
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Folders
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads', 'pending')
    CLASSIFIED_FOLDER = os.path.join(BASE_DIR, 'uploads', 'classified')
    TEMP_FOLDER = os.path.join(BASE_DIR, 'uploads', 'temp')
    
    # OCR
    TESSERACT_PATH = os.getenv('TESSERACT_PATH', 'C:/Program Files/Tesseract-OCR/tesseract.exe')
    
    # ML Model
    MODEL_PATH = os.path.join(BASE_DIR, 'models', 'classifier_model.pkl')
    VECTORIZER_PATH = os.path.join(BASE_DIR, 'models', 'vectorizer.pkl')
    MIN_CONFIDENCE = float(os.getenv('MIN_CONFIDENCE', '0.6'))
    
    # Document Types
    DOCUMENT_TYPES = [
        'Factura',
        'Nota de Debito',
        'Nota de Credito',
        'Remito',
        'Desconocido'
    ]
    
    # File Upload
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    ALLOWED_EXTENSIONS = {'pdf'}
    
    @staticmethod
    def init_app(app):
        # Create necessary directories
        os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
        os.makedirs(Config.CLASSIFIED_FOLDER, exist_ok=True)
        os.makedirs(Config.TEMP_FOLDER, exist_ok=True)
        os.makedirs(os.path.join(Config.BASE_DIR, 'models'), exist_ok=True)
        
        # Create subdirectories for each document type
        for doc_type in Config.DOCUMENT_TYPES:
            os.makedirs(os.path.join(Config.CLASSIFIED_FOLDER, doc_type), exist_ok=True)


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
