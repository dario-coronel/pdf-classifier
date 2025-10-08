# 📁 Estructura del Proyecto PDF Classifier

```
pdf-classifier/
│
├── 📄 README.md                    # Documentación principal del proyecto
├── 📄 INSTALL.md                   # Guía de instalación detallada
├── 📄 GUIA_RAPIDA.md              # Guía rápida de uso
├── 📄 requirements.txt             # Dependencias Python
├── 📄 .env.example                 # Ejemplo de configuración
├── 📄 .env                         # Configuración (no incluir en git)
├── 📄 .gitignore                   # Archivos ignorados por git
│
├── 🐍 app.py                       # Aplicación Flask principal
├── ⚙️ config.py                    # Configuración de la aplicación
├── 🔧 init.py                      # Script de inicialización
├── 🧪 test_classifier.py          # Tests del clasificador
├── 📊 process_batch.py            # Procesamiento por lotes
├── 🌐 api_examples.py             # Ejemplos de uso de API
│
├── 🪟 start.bat                    # Script de instalación (Windows)
├── 🚀 run.bat                      # Script para ejecutar (Windows)
│
├── 📂 database/
│   └── 📄 schema.sql              # Esquema de base de datos MySQL
│
├── 📂 models/                      # Modelos de datos (ORM)
│   ├── __init__.py
│   └── document.py                # Modelos: Document, DocumentType, etc.
│
├── 📂 services/                    # Lógica de negocio
│   ├── __init__.py
│   ├── pdf_processor.py           # Procesamiento PDF y OCR
│   ├── classifier.py              # Clasificador ML
│   └── document_service.py        # Servicio de documentos
│
├── 📂 templates/                   # Templates HTML (Jinja2)
│   ├── base.html                  # Template base con sidebar
│   ├── dashboard.html             # Dashboard principal
│   ├── pending.html               # Validación de documentos
│   ├── search.html                # Búsqueda de documentos
│   ├── document_detail.html       # Detalle de documento
│   └── settings.html              # Configuración
│
├── 📂 uploads/                     # Carpeta de documentos
│   ├── pending/                   # PDFs pendientes de procesamiento
│   ├── classified/                # PDFs clasificados y validados
│   │   ├── Factura/
│   │   ├── Nota de Credito/
│   │   ├── Nota de Debito/
│   │   ├── Remito/
│   │   └── Desconocido/
│   └── temp/                      # Archivos temporales
│
└── 📂 models/                      # Modelos ML entrenados
    ├── classifier_model.pkl       # Modelo de clasificación
    ├── vectorizer.pkl             # Vectorizador TF-IDF
    └── classifier_model_labels.pkl # Etiquetas del modelo

```

## 📝 Descripción de Archivos Principales

### Configuración y Documentación
- **README.md**: Documentación completa del proyecto
- **INSTALL.md**: Guía paso a paso de instalación
- **GUIA_RAPIDA.md**: Referencia rápida para usuarios
- **requirements.txt**: Lista de todas las dependencias Python
- **.env**: Variables de entorno (DB, rutas, etc.)

### Aplicación Principal
- **app.py**: Servidor Flask con todas las rutas y endpoints
- **config.py**: Configuración centralizada (DB, folders, ML params)
- **init.py**: Script para inicializar el proyecto

### Base de Datos
- **database/schema.sql**: 
  - Tablas: documents, document_types, processing_logs, ml_training_data
  - Vistas: document_statistics, recent_documents
  - Índices y relaciones

### Modelos de Datos (ORM)
- **models/document.py**:
  - `DocumentType`: Tipos de documentos
  - `Document`: Documentos procesados
  - `ProcessingLog`: Logs de procesamiento
  - `MLTrainingData`: Datos para entrenamiento ML

### Servicios (Lógica de Negocio)
- **services/pdf_processor.py**:
  - Extracción de texto (PyPDF2, pdfplumber)
  - OCR con Tesseract
  - Extracción de metadata (CUIT, proveedor, fecha, monto)

- **services/classifier.py**:
  - Clasificador ML (TF-IDF + Naive Bayes)
  - Clasificación basada en reglas
  - Reentrenamiento del modelo

- **services/document_service.py**:
  - Procesamiento de documentos
  - Validación y movimiento de archivos
  - Búsqueda y estadísticas

### Templates Web
- **base.html**: Layout principal con sidebar y navbar
- **dashboard.html**: Página principal con estadísticas y gráficos
- **pending.html**: Interfaz para validar documentos clasificados
- **search.html**: Búsqueda avanzada con filtros
- **document_detail.html**: Vista detallada de un documento
- **settings.html**: Configuración del sistema

### Scripts de Utilidad
- **start.bat**: Instalación automática en Windows
- **run.bat**: Ejecutar la aplicación
- **test_classifier.py**: Probar el clasificador ML
- **process_batch.py**: Procesar PDFs por lotes
- **api_examples.py**: Ejemplos de uso de la API

## 🎨 Tecnologías Utilizadas

### Backend
- **Flask** 3.0 - Framework web
- **SQLAlchemy** - ORM para base de datos
- **MySQL** - Base de datos relacional
- **PyMySQL** - Conector MySQL

### Procesamiento PDF
- **PyPDF2** - Extracción de texto
- **pdfplumber** - Análisis avanzado de PDFs
- **pdf2image** - Conversión PDF a imagen
- **Pillow** - Procesamiento de imágenes

### OCR y ML
- **pytesseract** - OCR (Tesseract wrapper)
- **scikit-learn** - Machine Learning
- **pandas** - Manipulación de datos
- **numpy** - Operaciones numéricas
- **NLTK** - Procesamiento de lenguaje natural

### Frontend
- **Bootstrap 5** - Framework CSS
- **Font Awesome** - Iconos
- **jQuery** - JavaScript
- **DataTables** - Tablas interactivas
- **Chart.js** - Gráficos y visualizaciones

## 🔄 Flujo de Datos

```
1. PDF → uploads/pending/
         ↓
2. PDF Processor (extract text + OCR)
         ↓
3. Metadata Extractor (CUIT, proveedor, etc.)
         ↓
4. ML Classifier (predict document type)
         ↓
5. Database (save document + metadata)
         ↓
6. User Validation (confirm/correct)
         ↓
7. Move to uploads/classified/{type}/
         ↓
8. ML Training Data (for retraining)
```

## 📊 Base de Datos - Relaciones

```
document_types
    ↓ (1:N)
documents
    ↓ (1:N)
    ├── processing_logs
    └── ml_training_data
```

## 🔌 Endpoints API

### Documentos
- `GET /api/documents` - Listar con filtros
- `GET /api/documents/<id>` - Ver detalle
- `POST /api/process` - Procesar pendientes
- `POST /api/validate` - Validar uno
- `POST /api/validate-batch` - Validar varios

### Sistema
- `GET /api/statistics` - Estadísticas
- `GET /api/document-types` - Tipos disponibles
- `POST /api/retrain-model` - Reentrenar ML

### Páginas Web
- `GET /` - Dashboard
- `GET /documents/pending` - Validación
- `GET /documents/search` - Búsqueda
- `GET /documents/view/<id>` - Detalle
- `GET /settings` - Configuración

## 🎯 Archivos que NO deben estar en Git

```
.env
uploads/
models/*.pkl
__pycache__/
*.pyc
venv/
*.log
```

## 📦 Tamaño Aproximado

- Código fuente: ~100 KB
- Dependencias (venv): ~500 MB
- Modelo ML entrenado: ~5 MB
- Base de datos (vacía): ~1 MB
- Base de datos (1000 docs): ~50 MB
- PDFs clasificados: Variable

## 🚀 Comandos Rápidos

```bash
# Instalación
start.bat

# Ejecutar
run.bat

# Procesar lote
python process_batch.py

# Probar clasificador
python test_classifier.py

# Inicializar DB
python init.py

# Ver ejemplos API
python api_examples.py
```

---

**Última actualización**: Octubre 2025  
**Versión**: 1.0.0
