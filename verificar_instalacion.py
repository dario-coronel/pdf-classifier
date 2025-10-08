"""
Script para verificar que todas las dependencias están instaladas correctamente
"""

import sys
import os

print("=" * 70)
print("VERIFICACIÓN DE INSTALACIÓN - PDF CLASSIFIER")
print("=" * 70)

# 1. Verificar Python
print("\n[1/6] Verificando Python...")
print(f"✓ Python {sys.version.split()[0]} instalado")

# 2. Verificar Tesseract
print("\n[2/6] Verificando Tesseract OCR...")
try:
    import pytesseract
    from config import Config
    
    if os.path.exists(Config.TESSERACT_PATH):
        print(f"✓ Tesseract encontrado en: {Config.TESSERACT_PATH}")
        pytesseract.pytesseract.tesseract_cmd = Config.TESSERACT_PATH
        version = pytesseract.get_tesseract_version()
        print(f"  Versión: {version}")
    else:
        print(f"✗ Tesseract NO encontrado en: {Config.TESSERACT_PATH}")
        print("  Por favor, actualiza TESSERACT_PATH en el archivo .env")
except Exception as e:
    print(f"✗ Error: {e}")

# 3. Verificar Poppler
print("\n[3/6] Verificando Poppler...")
poppler_path = os.path.join(os.path.dirname(__file__), 'poppler-24.08.0', 'Library', 'bin')
pdftotext = os.path.join(poppler_path, 'pdftotext.exe')

if os.path.exists(pdftotext):
    print(f"✓ Poppler encontrado en: {poppler_path}")
else:
    print(f"✗ Poppler NO encontrado")
    print(f"  Buscado en: {poppler_path}")
    print("  Por favor, descarga y extrae Poppler en la carpeta del proyecto")

# 4. Verificar MySQL
print("\n[4/6] Verificando conexión a MySQL...")
try:
    from sqlalchemy import create_engine
    from config import Config
    
    engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)
    connection = engine.connect()
    connection.close()
    print("✓ Conexión a MySQL exitosa")
    print(f"  Base de datos: {Config.DB_NAME}")
except Exception as e:
    print(f"✗ Error conectando a MySQL: {e}")
    print("  Verifica que MySQL esté corriendo y las credenciales en .env sean correctas")

# 5. Verificar paquetes Python
print("\n[5/6] Verificando paquetes Python...")
packages = {
    'flask': 'Flask',
    'flask_sqlalchemy': 'Flask-SQLAlchemy',
    'PyPDF2': 'PyPDF2',
    'pdfplumber': 'pdfplumber',
    'PIL': 'Pillow',
    'pytesseract': 'pytesseract',
    'sklearn': 'scikit-learn',
    'pandas': 'pandas',
    'numpy': 'numpy',
    'pdf2image': 'pdf2image'
}

missing_packages = []
for module, package in packages.items():
    try:
        __import__(module)
        print(f"  ✓ {package}")
    except ImportError:
        print(f"  ✗ {package} - NO INSTALADO")
        missing_packages.append(package)

if missing_packages:
    print(f"\n⚠ Faltan paquetes. Instala con:")
    print(f"  pip install {' '.join(missing_packages)}")

# 6. Verificar estructura de carpetas
print("\n[6/6] Verificando estructura de carpetas...")
folders = [
    'uploads/pending',
    'uploads/classified',
    'uploads/temp',
    'models'
]

for folder in folders:
    if os.path.exists(folder):
        print(f"  ✓ {folder}")
    else:
        print(f"  ✗ {folder} - NO EXISTE")
        try:
            os.makedirs(folder, exist_ok=True)
            print(f"    → Carpeta creada")
        except Exception as e:
            print(f"    → Error creando carpeta: {e}")

# Resumen
print("\n" + "=" * 70)
print("RESUMEN")
print("=" * 70)

if not missing_packages:
    print("\n✓ ¡Todas las dependencias están instaladas correctamente!")
    print("\nPróximos pasos:")
    print("1. Asegúrate de configurar DB_PASSWORD en el archivo .env")
    print("2. Importa la base de datos: mysql -u root -p < database/schema.sql")
    print("3. Ejecuta la aplicación: python app.py")
else:
    print("\n⚠ Hay dependencias faltantes. Por favor, instálalas y vuelve a ejecutar.")
    print("   Ejecuta: pip install -r requirements.txt")

print("=" * 70)
