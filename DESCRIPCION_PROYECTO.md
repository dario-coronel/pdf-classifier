# PDF Classifier - Descripción Completa del Proyecto

**Fecha:** 5 de Noviembre de 2025  
**Autor:** Sistema de Clasificación Automática de Documentos PDF  
**Repositorio:** pdf-classifier

---

## 📋 Visión General

**PDF Classifier** es un sistema web desarrollado en Python con Flask que clasifica automáticamente documentos PDF en categorías específicas (Facturas, Notas de Débito, Notas de Crédito, Remitos) utilizando Machine Learning, procesamiento de lenguaje natural y OCR.

### Características Principales
- ✅ Clasificación automática mediante red neuronal (MLPClassifier)
- ✅ Sistema de reglas inteligente para mejorar precisión
- ✅ Extracción automática de metadata (CUIT, fechas, montos, números)
- ✅ Interfaz web moderna y responsive
- ✅ Validación humana de resultados
- ✅ Reentrenamiento continuo del modelo
- ✅ Visualización con gráficos y estadísticas

---

## 🏗️ Arquitectura del Sistema

### 1. Capa de Presentación (Frontend)

**Tecnologías:**
- Flask con Jinja2 (templates)
- Bootstrap 5 (diseño responsive)
- jQuery + DataTables (tablas interactivas)
- Chart.js (visualización de datos)
- SweetAlert2 (notificaciones)

**Páginas Principales:**

#### Dashboard (`/`)
- Estadísticas globales del sistema
- Gráficos de distribución por tipo de documento
- Tabla de documentos recientes
- Acceso rápido a funciones principales

#### Validar Documentos (`/documents/pending`)
- Lista de documentos pendientes de validación
- Vista previa del PDF
- Corrección de clasificación si es necesaria
- Validación individual o por lotes

#### Buscar Documentos (`/documents/search`)
- Filtros avanzados:
  - Tipo de documento
  - Estado (pendiente/clasificado/validado/error)
  - Rango de fechas
  - CUIT
  - Proveedor
- Exportación a CSV
- Resultados paginados con DataTables

#### Detalle de Documento (`/documents/view/<id>`)
- Visualización del PDF en iframe
- Metadata extraída:
  - CUIT
  - Proveedor
  - Fecha del documento
  - Número de documento
  - Monto total
- Confianza de clasificación
- Historial de procesamiento

#### Configuración (`/settings`)
- Gestión de tipos de documentos
- Estado del sistema
- Acceso a carpetas
- Reentrenamiento del modelo

**Sistema de Colores por Tipo (Implementación Reciente):**
- 🟢 **Factura** → Verde (#1cc88a)
- 🔴 **Nota de Débito** → Rojo (#e74a3b)
- 🟡 **Nota de Crédito** → Amarillo (#f6c23e)
- 🔵 **Remito** → Azul (#4e73df)
- ⚫ **Desconocido** → Gris (#6c757d)

---

### 2. Capa de Aplicación (Backend)

**Framework:** Flask 3.0 + SQLAlchemy

#### Servidor Principal (`app.py`)
```python
- Define rutas HTTP (endpoints)
- Inicializa base de datos
- Configura servicios
- Maneja requests/responses
- Gestiona sesiones y errores
```

**Endpoints Principales:**
- `GET /` → Dashboard
- `GET /documents/pending` → Documentos pendientes
- `GET /documents/search` → Búsqueda
- `GET /documents/view/<id>` → Detalle
- `POST /api/process` → Procesar documentos
- `POST /api/validate` → Validar documento
- `POST /api/retrain-model` → Reentrenar modelo
- `GET /api/documents` → API lista documentos

---

### 3. Capa de Servicios

#### **DocumentService** (`services/document_service.py`)

**Responsabilidades:**
- Orquestar el procesamiento completo de documentos
- Coordinar extracción, clasificación y almacenamiento
- Gestionar archivos en el sistema de carpetas
- Generar estadísticas y reportes
- Manejo de errores y logging

**Métodos Principales:**
```python
process_pending_documents()
├─ Escanea carpeta pending/
├─ Por cada PDF:
│  ├─ extract_text_and_metadata()
│  ├─ classify_document()
│  ├─ save_to_database()
│  └─ move_to_classified_folder()
└─ Retorna resumen de procesamiento

get_statistics()
├─ Total documentos
├─ Por tipo de documento
├─ Por estado (validado/pendiente)
├─ Tasa de errores
└─ Distribuciones para gráficos

validate_document(doc_id, corrected_type, user)
├─ Actualizar tipo si fue corregido
├─ Cambiar status a 'validated'
├─ Mover archivo a carpeta final
└─ Agregar a training data
```

---

#### **PDFProcessor** (`services/pdf_processor.py`)

**Responsabilidades:**
- Extraer texto de PDFs mediante múltiples estrategias
- Extraer metadata estructurada (CUIT, fechas, montos, etc.)
- Manejo robusto de diferentes formatos de PDF

**Pipeline de Extracción de Texto:**
```
1. PyPDF2 (texto nativo)
   ├─ Rápido
   ├─ Para PDFs con texto embebido
   └─ Si falla → paso 2

2. pdfplumber
   ├─ Extrae tablas y estructura
   ├─ Mejor para documentos complejos
   └─ Si falla → paso 3

3. pytesseract (OCR)
   ├─ Convierte PDF a imágenes (pdf2image)
   ├─ Aplica OCR con Tesseract
   └─ Más lento pero funciona con PDFs escaneados
```

**Extracción de Metadata:**
```python
extract_metadata(text)
├─ CUIT
│  └─ Regex: \d{2}-\d{8}-\d
│
├─ Fechas
│  ├─ DD/MM/YYYY
│  ├─ DD-MM-YYYY
│  └─ YYYY-MM-DD
│
├─ Montos
│  ├─ $X,XXX.XX
│  ├─ $X.XXX,XX
│  └─ Variantes sin símbolo
│
└─ Números de Documento
   ├─ Factura N°: XXXXX
   ├─ N° XXXXX
   └─ Comprobante XXXXX
```

**Normalización:**
- Limpieza de espacios múltiples
- Normalización de caracteres especiales
- Conversión a lowercase para matching

---

#### **Classifier** (`services/classifier.py`)

**Arquitectura del Modelo ML:**

```
Modelo: MLPClassifier (Red Neuronal Feed-Forward)
├─ Capa de entrada: 1000 features (TF-IDF)
├─ Capa oculta 1: 100 neuronas
├─ Capa oculta 2: 50 neuronas
└─ Capa de salida: 4 clases
   ├─ Factura
   ├─ Nota de Debito
   ├─ Nota de Credito
   └─ Remito
```

**Vectorización TF-IDF:**
```python
TfidfVectorizer
├─ max_features = 1000
├─ ngram_range = (1, 2)  # unigramas y bigramas
├─ min_df = 1
├─ max_df = 0.8
└─ sublinear_tf = True
```

**Pipeline de Clasificación:**
```
1. Normalización
   ├─ Lowercase
   ├─ Remover puntuación excesiva
   └─ Normalizar espacios

2. Vectorización
   ├─ Aplicar TF-IDF
   └─ Vector de 1000 dimensiones

3. Predicción ML
   ├─ Clasificador neuronal
   └─ Probabilidades por clase

4. Post-procesado con Reglas (NUEVO)
   ├─ Detección de keywords
   ├─ Override o boost de probabilidades
   └─ Razón de decisión

5. Decisión Final
   ├─ Clase predicha
   ├─ Confianza (0.0 - 1.0)
   └─ Razón (ML o regla aplicada)
```

**Training Data Embebido:**
```python
# Ejemplos por defecto para inicialización
TRAINING_DATA = {
    'Factura': [
        'factura tipo a numero fecha cuit razon social ...',
        'comprobante original factura ...',
        # ... más ejemplos
    ],
    'Nota de Debito': [...],
    'Nota de Credito': [...],
    'Remito': [...]
}
```

**Reentrenamiento:**
```python
retrain()
├─ Obtener documentos validados de DB
├─ Combinar con training data embebido
├─ Verificar mínimo de ejemplos por clase
├─ Re-entrenar MLPClassifier
├─ Guardar nuevo modelo (joblib)
└─ Retornar métricas de accuracy
```

---

#### **Rules** (`services/rules.py`) - IMPLEMENTACIÓN RECIENTE

**Objetivo:** Mejorar la precisión de clasificación detectando keywords explícitas en el documento.

**Estrategia:**

```
1. Prioridad Header (Primera página, primeras líneas)
   ├─ Extrae primeras 3-5 líneas
   ├─ Busca keywords exactas:
   │  ├─ "FACTURA" → Override a Factura
   │  ├─ "NOTA DE DEBITO" → Override a Nota de Debito
   │  ├─ "NOTA DE CREDITO" → Override a Nota de Credito
   │  └─ "REMITO" → Override a Remito
   └─ Si match exacto → OVERRIDE (ignora ML)

2. Body Matching (Documento completo)
   ├─ Fuzzy matching de keywords
   ├─ Variantes y sinónimos
   └─ Si match → BOOST probabilidad (+0.3)

3. Políticas de Aplicación
   ├─ rule_override_header_exact
   │  └─ Confianza alta en keyword de header
   │
   ├─ rule_boost_body_exact
   │  └─ Incrementa probabilidad de clase
   │
   └─ rule_boost_body_fuzzy
      └─ Incrementa con menor peso
```

**Funciones Principales:**

```python
normalize(text)
├─ Lowercase
├─ Normalizar espacios
└─ Remover acentos opcionales

fuzzy_match(keyword, text, threshold=0.8)
├─ Ratio de similitud
└─ Verdadero si > threshold

extract_header_lines(text, max_lines=5)
├─ Split por líneas
├─ Tomar primeras N no vacías
└─ Retornar como texto único

detect_document_keyword(text)
├─ Chequear header primero
├─ Luego body con fuzzy
└─ Retornar (tipo, razón) o (None, None)

apply_rule_boost(predicted_label, probs_dict, text)
├─ Detectar keyword en texto
├─ Si header exact → override
├─ Si body fuzzy → boost probabilidad
├─ Recalcular max probabilidad
└─ Retornar (nuevo_label, nueva_confianza, razón)
```

**Ejemplo de Aplicación:**

```python
# Entrada ML
predicted = "Nota de Debito"
probs = {
    "Factura": 0.45,
    "Nota de Debito": 0.38,
    "Nota de Credito": 0.12,
    "Remito": 0.05
}
text = "FACTURA TIPO A\n..."

# Procesado por reglas
final_label, final_conf, reason = apply_rule_boost(
    predicted, probs, text
)

# Salida
final_label = "Factura"  # ← OVERRIDE
final_conf = 0.95  # ← Alta confianza
reason = "rule_override_header_exact"
```

---

### 4. Capa de Datos

#### Base de Datos MySQL

**Tabla: `documents`**
```sql
CREATE TABLE documents (
    id INT PRIMARY KEY AUTO_INCREMENT,
    filename VARCHAR(255) NOT NULL,
    original_filename VARCHAR(255) NOT NULL,
    document_type_id INT,
    status ENUM('pending','analyzing','classified','validated','error'),
    confidence_score DECIMAL(5,4),
    
    -- Metadata extraída
    cuit VARCHAR(20),
    provider VARCHAR(255),
    document_date DATE,
    document_number VARCHAR(100),
    total_amount DECIMAL(15,2),
    
    -- Texto completo
    extracted_text LONGTEXT,
    
    -- Timestamps
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    processed_at TIMESTAMP NULL,
    
    -- Info archivo
    file_size INT,
    
    FOREIGN KEY (document_type_id) REFERENCES document_types(id),
    INDEX idx_status (status),
    INDEX idx_type (document_type_id),
    INDEX idx_cuit (cuit),
    INDEX idx_date (document_date)
);
```

**Tabla: `document_types`**
```sql
CREATE TABLE document_types (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT,
    active BOOLEAN DEFAULT TRUE,
    color VARCHAR(7),  -- Hex color para UI
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Datos iniciales
INSERT INTO document_types (name, description, color) VALUES
('Factura', 'Factura de compra o venta', '#1cc88a'),
('Nota de Debito', 'Nota de débito', '#e74a3b'),
('Nota de Credito', 'Nota de crédito', '#f6c23e'),
('Remito', 'Remito de entrega', '#4e73df'),
('Desconocido', 'Tipo no identificado', '#6c757d');
```

**Tabla: `ml_training_data`**
```sql
CREATE TABLE ml_training_data (
    id INT PRIMARY KEY AUTO_INCREMENT,
    document_type_id INT NOT NULL,
    text_content LONGTEXT NOT NULL,
    source VARCHAR(50),  -- 'validated', 'manual', 'default'
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (document_type_id) REFERENCES document_types(id),
    INDEX idx_type (document_type_id)
);
```

**Tabla: `processing_logs`**
```sql
CREATE TABLE processing_logs (
    id INT PRIMARY KEY AUTO_INCREMENT,
    document_id INT,
    step VARCHAR(100),  -- 'extraction', 'classification', 'validation'
    status ENUM('success','error','warning'),
    message TEXT,
    error_details TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (document_id) REFERENCES documents(id)
);
```

---

### 5. Flujo de Procesamiento Completo

#### Paso 1: Ingreso de Documentos
```
Usuario → Coloca PDFs en uploads/pending/
   ↓
Watchdog detecta nuevos archivos
   ↓
Se dispara process_pending_documents()
```

#### Paso 2: Extracción
```
Por cada PDF:
   ↓
PDFProcessor.extract_text()
   ├─ Intento 1: PyPDF2
   ├─ Intento 2: pdfplumber
   └─ Intento 3: pytesseract (OCR)
   ↓
PDFProcessor.extract_metadata()
   ├─ CUIT (regex)
   ├─ Fechas (regex + parsing)
   ├─ Montos (regex + parsing)
   └─ Números (regex)
```

#### Paso 3: Clasificación
```
Texto extraído
   ↓
Classifier.classify()
   ↓
1. Normalizar texto
   ↓
2. Vectorizar (TF-IDF)
   ↓
3. Predecir (MLPClassifier)
   ├─ Obtener probabilidades por clase
   ↓
4. Post-procesado con Rules
   ├─ detect_document_keyword()
   ├─ apply_rule_boost()
   │  ├─ ¿Keyword en header? → Override
   │  └─ ¿Keyword en body? → Boost
   ↓
5. Decisión final
   ├─ Clase predicha
   ├─ Confianza (0.0-1.0)
   └─ Razón de clasificación
```

#### Paso 4: Almacenamiento
```
Guardar en DB (tabla documents)
   ├─ Metadata extraída
   ├─ Texto completo
   ├─ Clasificación
   └─ Confianza
   ↓
Mover archivo físico
   ├─ Si confianza >= 0.7
   │  └─ uploads/classified/<TipoDoc>/
   └─ Si confianza < 0.7
      └─ Permanece en uploads/pending/
```

#### Paso 5: Validación Humana
```
Usuario revisa en /documents/pending
   ↓
¿Clasificación correcta?
   ├─ SÍ → Validar
   │     ├─ Status → 'validated'
   │     ├─ Mover a carpeta final
   │     └─ Agregar a training data
   │
   └─ NO → Corregir tipo
         ├─ Actualizar document_type_id
         ├─ Status → 'validated'
         ├─ Mover a carpeta correcta
         └─ Agregar a training data
```

#### Paso 6: Mejora Continua
```
Periódicamente:
   ↓
Reentrenar modelo
   ├─ Obtener documentos validados
   ├─ Combinar con training data embebido
   ├─ Entrenar nuevo MLPClassifier
   ├─ Validar accuracy
   └─ Guardar modelo actualizado
   ↓
Modelo mejora con cada validación ♻️
```

---

## 📁 Estructura de Archivos

```
pdf-classifier/
│
├── app.py                          # Servidor Flask principal
├── config.py                       # Configuración global
├── requirements.txt                # Dependencias Python
├── .env                            # Variables de entorno (local, no en repo)
│
├── models/                         # Modelos ML serializados
│   ├── __init__.py
│   ├── document.py                 # ORM SQLAlchemy
│   ├── classifier_model.pkl        # Red neuronal entrenada
│   ├── vectorizer.pkl              # Vectorizador TF-IDF
│   └── classifier_model_labels.pkl # Mapeo de labels
│
├── services/                       # Lógica de negocio
│   ├── __init__.py
│   ├── classifier.py               # Clasificación ML + reglas
│   ├── pdf_processor.py            # Extracción de PDF
│   ├── document_service.py         # Orquestación
│   └── rules.py                    # Post-procesado (NUEVO)
│
├── templates/                      # Vistas Jinja2
│   ├── base.html                   # Layout base + macros
│   ├── dashboard.html              # Dashboard principal
│   ├── pending.html                # Documentos pendientes
│   ├── search.html                 # Búsqueda avanzada
│   ├── document_detail.html        # Vista detalle
│   └── settings.html               # Configuración
│
├── static/                         # Assets frontend
│   ├── css/
│   │   └── custom.css              # Estilos personalizados (NUEVO)
│   ├── js/
│   └── images/
│
├── uploads/                        # Almacenamiento de PDFs
│   ├── pending/                    # Documentos sin clasificar
│   ├── classified/                 # Documentos clasificados
│   │   ├── Factura/
│   │   ├── Nota de Debito/
│   │   ├── Nota de Credito/
│   │   ├── Remito/
│   │   └── Desconocido/
│   └── temp/                       # Archivos temporales
│
├── database/
│   └── schema.sql                  # Esquema completo de DB
│
├── tests/                          # Tests y scripts de debug
│   ├── test_rules.py               # Tests unitarios de reglas
│   ├── run_smoke.py                # Smoke test de clasificación
│   ├── debug_detect.py             # Debug de detección
│   └── print_model_info.py         # Inspección del modelo
│
├── tools/                          # Herramientas auxiliares
│   ├── md_to_html.py               # Convertidor documentación
│   └── gen_docs.bat                # Script generación docs
│
├── manual/                         # Documentación del proyecto
│   ├── INDEX.md
│   ├── README.md
│   ├── INSTALL.md
│   ├── GUIA_RAPIDA.md
│   ├── FAQ.md
│   ├── ESTRUCTURA.md
│   ├── ESTADO_INSTALACION.md
│   ├── MEJORES_PRACTICAS.md
│   ├── RESUMEN_EJECUTIVO.md
│   └── INSTALACION_TESSERACT_POPPLER.md
│
├── run.bat                         # Script inicio (CMD)
├── start.bat                       # Script inicio alternativo
├── start.ps1                       # Script inicio (PowerShell)
├── process_batch.py                # Procesamiento masivo
└── verificar_instalacion.py        # Verificar dependencias
```

---

## 🔧 Configuración

### Variables de Entorno (`.env`)
```ini
# Base de datos
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=tu_password
DB_NAME=pdf_classifier

# OCR
TESSERACT_PATH=C:/Program Files/Tesseract-OCR/tesseract.exe
POPPLER_PATH=C:/path/to/poppler/bin

# Flask
SECRET_KEY=tu_clave_secreta_aqui
DEBUG=True

# Clasificación
MIN_CONFIDENCE=0.7
```

### Archivo de Configuración (`config.py`)
```python
class Config:
    # Database
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_USER = os.getenv('DB_USER', 'root')
    DB_PASSWORD = os.getenv('DB_PASSWORD', '')
    DB_NAME = os.getenv('DB_NAME', 'pdf_classifier')
    
    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}"
        f"@{DB_HOST}/{DB_NAME}?charset=utf8mb4"
    )
    
    # Flask
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')
    DEBUG = os.getenv('DEBUG', 'True') == 'True'
    
    # File paths
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
    PENDING_FOLDER = os.path.join(UPLOAD_FOLDER, 'pending')
    CLASSIFIED_FOLDER = os.path.join(UPLOAD_FOLDER, 'classified')
    TEMP_FOLDER = os.path.join(UPLOAD_FOLDER, 'temp')
    MODELS_FOLDER = os.path.join(BASE_DIR, 'models')
    
    # OCR
    TESSERACT_PATH = os.getenv(
        'TESSERACT_PATH',
        'C:/Program Files/Tesseract-OCR/tesseract.exe'
    )
    POPPLER_PATH = os.getenv('POPPLER_PATH', None)
    
    # ML Classifier
    MIN_CONFIDENCE = float(os.getenv('MIN_CONFIDENCE', '0.7'))
    MODEL_FILE = 'classifier_model.pkl'
    VECTORIZER_FILE = 'vectorizer.pkl'
    LABELS_FILE = 'classifier_model_labels.pkl'
    
    # Processing
    MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB
    ALLOWED_EXTENSIONS = {'pdf'}
```

---

## 🚀 Instalación y Uso

### Requisitos Previos
```
✓ Python 3.8+
✓ MySQL 8.0+
✓ Tesseract OCR
✓ Poppler (para pdf2image)
```

### Paso 1: Instalación de Dependencias Externas

**Windows:**
```powershell
# Tesseract OCR
# Descargar desde: https://github.com/UB-Mannheim/tesseract/wiki
# Instalar en: C:\Program Files\Tesseract-OCR\

# Poppler
# Descargar desde: https://github.com/oschwartz10612/poppler-windows/releases
# Extraer en carpeta del proyecto: pdf-classifier/poppler-24.08.0/
```

**Linux:**
```bash
sudo apt-get install tesseract-ocr
sudo apt-get install poppler-utils
```

### Paso 2: Configuración del Proyecto

```powershell
# 1. Clonar o descargar proyecto
cd C:\Clases\PP3\pdf-classifier

# 2. Crear entorno virtual
python -m venv venv

# 3. Activar entorno virtual
.\venv\Scripts\Activate.ps1   # PowerShell
# o
venv\Scripts\activate.bat      # CMD

# 4. Instalar dependencias Python
pip install -r requirements.txt

# 5. Crear archivo .env con configuración
# Copiar .env.example a .env y editar valores
```

**Contenido de `requirements.txt`:**
```
Flask==3.0.0
Flask-SQLAlchemy==3.1.1
Flask-Login==0.6.3
Flask-WTF==1.2.1
mysql-connector-python==8.2.0
PyMySQL==1.1.0
cryptography==41.0.7
python-dotenv==1.0.0
Werkzeug==3.0.1
WTForms==3.1.1

# PDF Processing
PyPDF2==3.0.1
pdfplumber==0.10.3
pdf2image==1.16.3
Pillow==11.3.0

# OCR
pytesseract==0.3.10

# Machine Learning
scikit-learn==1.5.2
numpy==2.1.0
pandas==2.2.3
joblib==1.4.2

# NLP
nltk==3.8.1

# Utils
python-dateutil==2.8.2
watchdog==6.0.0
```

### Paso 3: Configuración de Base de Datos

```sql
-- 1. Crear base de datos
CREATE DATABASE pdf_classifier CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- 2. Crear usuario (opcional)
CREATE USER 'pdf_user'@'localhost' IDENTIFIED BY 'tu_password';
GRANT ALL PRIVILEGES ON pdf_classifier.* TO 'pdf_user'@'localhost';
FLUSH PRIVILEGES;

-- 3. Importar esquema
mysql -u root -p pdf_classifier < database/schema.sql
```

### Paso 4: Inicialización

```powershell
# Opción A: Usar script de inicio (recomendado)
.\start.ps1

# Opción B: Manual
python -c "from app import app, db; app.app_context().push(); db.create_all()"
```

### Paso 5: Ejecutar Aplicación

```powershell
# Iniciar servidor Flask
python app.py

# Servidor disponible en:
# http://localhost:5000
# http://127.0.0.1:5000
```

---

## 📊 Casos de Uso

### Caso 1: Procesar Documentos Nuevos

1. Colocar PDFs en `uploads/pending/`
2. En la web, ir a Dashboard
3. Click en "Procesar Documentos"
4. El sistema:
   - Extrae texto de cada PDF
   - Clasifica automáticamente
   - Extrae metadata (CUIT, fechas, montos)
   - Mueve archivos según confianza
5. Revisar resultados en "Validar Documentos"

### Caso 2: Validar Clasificación

1. Ir a "Validar Documentos"
2. Ver lista de documentos clasificados
3. Para cada documento:
   - Ver PDF en preview
   - Verificar tipo asignado
   - Corregir si es necesario
   - Click en "Validar"
4. Documento se mueve a carpeta final
5. Se agrega a training data automáticamente

### Caso 3: Buscar Documentos

1. Ir a "Buscar Documentos"
2. Aplicar filtros:
   - Tipo: "Factura"
   - Proveedor: "ACME S.A."
   - Fecha desde: 01/01/2025
   - Fecha hasta: 31/03/2025
3. Click en "Buscar"
4. Ver resultados en tabla
5. Exportar a CSV si es necesario

### Caso 4: Reentrenar Modelo

1. Validar al menos 10 documentos de cada tipo
2. Ir a "Configuración"
3. Click en "Reentrenar Modelo"
4. Esperar confirmación
5. El modelo mejora su precisión con los nuevos ejemplos

---

## 🧪 Tests y Validación

### Tests Implementados

**`tests/test_rules.py`** - Tests unitarios del sistema de reglas
```python
# Verificar detección de keywords
# Verificar override de ML
# Verificar boost de probabilidades
# Casos con múltiples keywords
```

**`tests/run_smoke.py`** - Smoke test de clasificación
```python
# Clasificar documentos de ejemplo
# Verificar que no haya errores
# Mostrar resultados y reglas aplicadas
```

**`tests/print_model_info.py`** - Inspeccionar modelo
```python
# Mostrar arquitectura de red neuronal
# Features del vectorizador
# Clases de salida
```

### Ejecutar Tests

```powershell
# Tests de reglas
python tests/test_rules.py

# Smoke test
python tests/run_smoke.py

# Info del modelo
python tests/print_model_info.py
```

---

## 📈 Métricas y Estadísticas

### Dashboard Analytics

**Métricas Principales:**
- Total de documentos procesados
- Distribución por tipo de documento
- Tasa de documentos validados
- Tasa de errores
- Confianza promedio

**Gráficos:**
1. **Barra:** Cantidad de documentos por tipo
2. **Pie (Todos):** Distribución general
3. **Pie (Validados):** Distribución de validados
4. **Pie (No Validados):** Distribución de pendientes

**Tabla de Recientes:**
- 10 documentos más recientes
- Estado con colores
- Confianza en barra de progreso
- Acceso directo a detalle

---

## 🎨 Personalización de UI

### Sistema de Colores (Implementación Reciente)

**Archivo:** `static/css/custom.css`
```css
.badge-factura {
    background-color: #1cc88a;
    color: #ffffff;
}

.badge-nota-debito {
    background-color: #e74a3b;
    color: #ffffff;
}

.badge-nota-credito {
    background-color: #f6c23e;
    color: #212529;
}

.badge-remito {
    background-color: #4e73df;
    color: #ffffff;
}

.badge-desconocido {
    background-color: #6c757d;
    color: #ffffff;
}
```

**Macro Jinja2 en `base.html`:**
```jinja2
{% macro doc_type_class(name) -%}
    {%- set n = (name or '')|lower -%}
    {%- if 'factura' in n -%}
        badge-factura
    {%- elif 'nota' in n and 'deb' in n -%}
        badge-nota-debito
    {%- elif 'nota' in n and 'cred' in n -%}
        badge-nota-credito
    {%- elif 'remito' in n -%}
        badge-remito
    {%- else -%}
        badge-desconocido
    {%- endif -%}
{%- endmacro %}
```

**Uso en Templates:**
```html
<span class="badge {{ doc_type_class(doc.document_type.name) }}">
    {{ doc.document_type.name }}
</span>
```

**JavaScript para Client-Side:**
```javascript
function docTypeClassJS(name) {
    if (!name) return 'badge-desconocido';
    const n = String(name).toLowerCase();
    if (n.includes('factura')) return 'badge-factura';
    if (n.includes('nota') && n.includes('deb')) return 'badge-nota-debito';
    if (n.includes('nota') && n.includes('cred')) return 'badge-nota-credito';
    if (n.includes('remito')) return 'badge-remito';
    return 'badge-desconocido';
}
```

---

## 🔍 Troubleshooting

### Problema: Tesseract no encontrado
**Síntoma:** Warning al iniciar: "Tesseract not found"
**Solución:**
1. Instalar Tesseract OCR
2. Actualizar ruta en `.env`:
   ```
   TESSERACT_PATH=C:/Program Files/Tesseract-OCR/tesseract.exe
   ```

### Problema: Error de conexión a MySQL
**Síntoma:** `Can't connect to MySQL server`
**Solución:**
1. Verificar que MySQL esté corriendo
2. Verificar credenciales en `.env`
3. Verificar que la base de datos exista

### Problema: Baja precisión de clasificación
**Síntoma:** Muchos documentos mal clasificados
**Solución:**
1. Validar más documentos manualmente
2. Reentrenar el modelo
3. Verificar que el sistema de reglas esté activo

### Problema: OCR no funciona con PDFs escaneados
**Síntoma:** Texto extraído vacío
**Solución:**
1. Instalar Poppler
2. Configurar `POPPLER_PATH` en `.env`
3. Verificar que pytesseract funcione

---

## 🔐 Seguridad

### Consideraciones de Seguridad

1. **Archivos sensibles:**
   - `.env` debe estar en `.gitignore`
   - No subir credenciales a repositorio

2. **Base de datos:**
   - Usar usuario con permisos limitados
   - Sanitizar inputs de búsqueda

3. **Archivos subidos:**
   - Validar extensión (solo PDF)
   - Limitar tamaño de archivo
   - Escanear por malware si es crítico

4. **Producción:**
   - Usar servidor WSGI (Gunicorn, uWSGI)
   - NO usar Flask debug en producción
   - Configurar HTTPS

---

## 📚 Tecnologías Utilizadas

### Backend
- **Flask 3.0** - Web framework
- **SQLAlchemy** - ORM
- **MySQL** - Base de datos
- **scikit-learn** - Machine Learning
- **PyPDF2** - Extracción de texto
- **pdfplumber** - Parsing estructurado
- **pytesseract** - OCR
- **pdf2image** - Conversión PDF a imagen
- **joblib** - Serialización de modelos
- **watchdog** - Monitoreo de archivos

### Frontend
- **Bootstrap 5** - CSS framework
- **jQuery** - Manipulación DOM
- **DataTables** - Tablas interactivas
- **Chart.js** - Visualización de datos
- **SweetAlert2** - Notificaciones elegantes
- **Font Awesome** - Iconos

### Herramientas Externas
- **Tesseract OCR** - Motor OCR
- **Poppler** - Renderización PDF

---

## 🚀 Mejoras Futuras Planificadas

### Corto Plazo
- ✅ ~~Sistema de reglas post-ML~~ (Implementado)
- ✅ ~~Colores por tipo de documento~~ (Implementado)
- ⏳ Features adicionales para ML (keywords, posición)
- ⏳ Documentación completa

### Mediano Plazo
- Autenticación de usuarios
- Roles y permisos
- API REST completa
- Exportación avanzada (Excel, JSON)
- Plantillas de documentos por proveedor

### Largo Plazo
- Modelos específicos por proveedor
- Extracción de ítems de factura (líneas de productos)
- Integración con sistemas contables
- OCR mejorado con deep learning
- Clustering automático de documentos similares
- Dashboard analytics avanzado

---

## 📝 Notas de Desarrollo

### Historial de Cambios Recientes

**5 de Noviembre de 2025:**
- ✅ Implementado sistema de reglas (`services/rules.py`)
- ✅ Integración de reglas con clasificador ML
- ✅ Sistema de colores por tipo de documento
- ✅ Macro Jinja2 y helper JS para badges
- ✅ Tests unitarios y smoke tests
- ✅ Actualización de Chart.js con colores fijos

**Archivos Modificados:**
- `services/classifier.py` - Integración de reglas
- `templates/base.html` - Macro y CSS custom
- `templates/dashboard.html` - Colores fijos en charts
- `templates/document_detail.html` - Uso de macro
- `templates/search.html` - Helper JS para badges

**Archivos Creados:**
- `services/rules.py` - Sistema de reglas
- `static/css/custom.css` - Estilos personalizados
- `tests/test_rules.py` - Tests de reglas
- `tests/run_smoke.py` - Smoke test
- `tests/debug_detect.py` - Debug helper
- `tests/print_model_info.py` - Inspección modelo

### TODO List Actualizada

- [x] Proponer mejoras de clasificación
- [x] Implementar post-procesado por reglas
- [x] Evaluación y tests
- [x] Arrancar servidor para tests
- [x] Implementar UI color mapping
- [ ] Agregar features de keywords y posición al ML
- [ ] Documentar estrategia en MEJORES_PRACTICAS.md
- [ ] Configuración de pesos de reglas en config.py

---

## 📞 Contacto y Soporte

**Repositorio:** pdf-classifier  
**Owner:** dario-coronel  
**Branch:** main  
**Fecha del documento:** 5 de Noviembre de 2025

---

## 📄 Licencia

Este proyecto es parte de un trabajo académico para la materia PP3 (Práctica Profesional 3).

---

**Fin del Documento**

---

## Apéndice A: Comandos Útiles

```powershell
# Iniciar proyecto
.\start.ps1

# Activar venv
.\venv\Scripts\Activate.ps1

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar aplicación
python app.py

# Procesar batch
python process_batch.py

# Verificar instalación
python verificar_instalacion.py

# Tests
python tests/test_rules.py
python tests/run_smoke.py
python tests/print_model_info.py

# Regenerar documentación
python tools/md_to_html.py
```

## Apéndice B: Estructura de Respuesta de Clasificación

```python
{
    'predicted_class': 'Factura',
    'confidence': 0.87,
    'all_probabilities': {
        'Factura': 0.87,
        'Nota de Debito': 0.08,
        'Nota de Credito': 0.03,
        'Remito': 0.02
    },
    'rule_applied': 'rule_boost_body_exact',
    'rule_reason': 'Keyword "factura" found in document body'
}
```

## Apéndice C: Formato de Metadata Extraída

```python
{
    'cuit': '20-12345678-9',
    'provider': 'ACME S.A.',
    'document_date': datetime.date(2025, 11, 5),
    'document_number': 'A-00001234',
    'total_amount': Decimal('15234.50'),
    'extracted_text': 'FACTURA TIPO A\nNúmero: A-00001234\n...'
}
```

---

**Este documento puede ser abierto y editado en Microsoft Word.**
