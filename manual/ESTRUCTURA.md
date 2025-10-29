````markdown
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

---

**Última actualización**: Octubre 2025  
**Versión**: 1.0.0

````
