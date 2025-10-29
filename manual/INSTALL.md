````markdown
# PDF Classifier - Installation Guide

## Windows Installation Steps

### 1. Install Python
1. Download Python 3.8+ from https://www.python.org/downloads/
2. During installation, CHECK "Add Python to PATH"
3. Verify installation:
```cmd
python --version
```

### 2. Install MySQL
1. Download MySQL Community Server from https://dev.mysql.com/downloads/mysql/
2. Run the installer
3. Set root password (remember it!)
4. Start MySQL service:
```cmd
net start MySQL80
```

### 3. Install Tesseract OCR
1. Download from: https://github.com/UB-Mannheim/tesseract/wiki
2. Run installer
3. During installation:
   - Check "Additional language data"
   - Select "Spanish" (spa)
4. Note the installation path (usually C:\Program Files\Tesseract-OCR)

### 4. Install Poppler (for PDF processing)
1. Download from: https://github.com/oschwartz10612/poppler-windows/releases/
2. Extract to C:\Program Files\poppler
3. Add to PATH:
   - Right-click "This PC" → Properties
   - Advanced system settings → Environment Variables
   - Edit "Path" → Add "C:\Program Files\poppler\Library\bin"

### 5. Setup Project
1. Open Command Prompt as Administrator
2. Navigate to project folder:
```cmd
cd c:\Clases\PP3\pdf-classifier
```

3. Run the setup script:
```cmd
start.bat
```

This will:
- Create virtual environment
- Install Python packages
- Create necessary folders
- Initialize database structure

### 6. Configure Database
1. Open MySQL Command Line:
```cmd
mysql -u root -p
```

2. Run the schema file:
```sql
source c:/Clases/PP3/pdf-classifier/database/schema.sql
```

Or use MySQL Workbench:
- Open MySQL Workbench
- Connect to your database
- File → Run SQL Script
- Select: database/schema.sql
- Execute

### 7. Configure Environment
1. Edit `.env` file with your settings:
```env
SECRET_KEY=change-this-to-random-string
DB_PASSWORD=your-mysql-password
TESSERACT_PATH=C:/Program Files/Tesseract-OCR/tesseract.exe
```

### 8. Test Installation
Run the test script:
```cmd
python test_classifier.py
```

### 9. Start the Application
```cmd
run.bat
```

Or manually:
```cmd
venv\Scripts\activate
python app.py
```

Access at: http://localhost:5000

## Quick Start Workflow

1. **Add PDF files** to `uploads/pending/` folder

2. **Process documents**:
   - Open http://localhost:5000
   - Click "Procesar Documentos" in sidebar
   - Wait for processing to complete

3. **Validate classifications**:
   - Click "Validar Documentos"
   - Review predicted types
   - Correct if needed
   - Click "Validar"

4. **Search documents**:
   - Click "Buscar Documentos"
   - Apply filters
   - Export results

## Troubleshooting

### "Tesseract not found"
- Check TESSERACT_PATH in .env
- Verify Tesseract is installed correctly
- Make sure tesseract.exe exists at the specified path

### "Connection refused" (MySQL)
- Check MySQL service is running: `net start MySQL80`
- Verify DB credentials in .env
- Test connection: `mysql -u root -p`

### "No module named 'X'"
- Activate virtual environment: `venv\Scripts\activate`
- Reinstall packages: `pip install -r requirements.txt`

### "pdf2image failed"
- Install Poppler
- Add Poppler to PATH
- Restart Command Prompt

### Low classification accuracy
- Process and validate more documents
- Click "Reentrenar Modelo" after 20+ validations
- The model improves with more training data

## Testing with Sample Documents

1. Create test PDFs in `uploads/pending/`
2. Run batch processing:
```cmd
python process_batch.py
```

## Default Credentials

There is no authentication by default. For production:
- Add Flask-Login
- Implement user authentication
- Add HTTPS
- Use environment-specific configurations

## Support

For issues:
1. Check logs in console
2. Verify all dependencies are installed
3. Check database connection
4. Ensure folders have write permissions

## Performance Tips

- Process documents in batches of 10-20
- Retrain model after every 20+ validations
- Keep classified folders organized
- Regular database backups
- Monitor disk space in uploads folder

````
