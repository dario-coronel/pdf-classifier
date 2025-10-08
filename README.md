# 📄 PDF Classifier - Sistema de Clasificación de Documentos

Sistema avanzado de clasificación automática de documentos PDF usando Machine Learning, OCR y extracción inteligente de datos.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.0-green.svg)
![MySQL](https://img.shields.io/badge/MySQL-8.0-orange.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 🚀 Características

- **Clasificación Automática**: Utiliza Machine Learning para clasificar documentos en categorías predefinidas
- **OCR Integrado**: Extrae texto de documentos escaneados usando Tesseract
- **Extracción de Datos**: Identifica automáticamente CUIT, proveedor, fecha, número de documento y montos
- **Dashboard Profesional**: Interfaz web moderna con Bootstrap y visualizaciones
- **Búsqueda Avanzada**: Busca documentos por tipo, fecha, CUIT, proveedor, etc.
- **Validación Manual**: Permite validar y corregir clasificaciones automáticas
- **Reentrenamiento**: El modelo aprende de las validaciones para mejorar continuamente
- **Base de Datos MySQL**: Almacenamiento robusto y escalable

## 📋 Requisitos Previos

### Software Necesario

1. **Python 3.8+**
   - Descargar desde: https://www.python.org/downloads/

2. **MySQL Server**
   - Descargar desde: https://dev.mysql.com/downloads/mysql/

3. **Tesseract OCR**
   - Windows: https://github.com/UB-Mannheim/tesseract/wiki
   - Durante la instalación, asegúrese de instalar los datos de idioma español

4. **Poppler** (para pdf2image)
   - Windows: Descargar desde https://github.com/oschwartz10612/poppler-windows/releases/
   - Extraer y agregar a PATH o especificar la ruta en el código

## 🔧 Instalación

### 1. Clonar el Repositorio

```bash
cd c:\Clases\PP3\pdf-classifier
```

### 2. Crear Entorno Virtual

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Instalar Dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar Base de Datos

1. Crear la base de datos en MySQL:

```bash
mysql -u root -p
```

```sql
source database/schema.sql
```

O importar manualmente el archivo `database/schema.sql`

### 5. Configurar Variables de Entorno

Copiar `.env.example` a `.env` y configurar:

```bash
copy .env.example .env
```

Editar `.env` con sus credenciales:

```env
SECRET_KEY=tu-clave-secreta-aqui
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=tu-contraseña
DB_NAME=pdf_classifier
TESSERACT_PATH=C:/Program Files/Tesseract-OCR/tesseract.exe
```

### 6. Crear Carpetas Necesarias

Las carpetas se crean automáticamente al iniciar la aplicación, pero puede crearlas manualmente:

```bash
mkdir uploads\pending
mkdir uploads\classified
mkdir uploads\temp
mkdir models
```

## 🎯 Uso

### 1. Iniciar la Aplicación

```bash
python app.py
```

La aplicación estará disponible en: http://localhost:5000

### 2. Flujo de Trabajo

1. **Cargar Documentos**:
   - Copiar archivos PDF a la carpeta `uploads/pending`

2. **Procesar Documentos**:
   - En el dashboard, hacer clic en "Procesar Documentos"
   - El sistema extraerá texto, clasificará y extraerá metadata

3. **Validar Clasificaciones**:
   - Ir a "Validar Documentos"
   - Revisar las clasificaciones automáticas
   - Corregir si es necesario
   - Validar documentos

4. **Buscar Documentos**:
   - Ir a "Buscar Documentos"
   - Aplicar filtros (tipo, fecha, CUIT, proveedor)
   - Exportar resultados si es necesario

### 3. Reentrenar el Modelo

Después de validar varios documentos:

```bash
# Desde el dashboard, clic en "Reentrenar Modelo"
# O desde la API:
curl -X POST http://localhost:5000/api/retrain-model
```

## 📁 Estructura del Proyecto

```
pdf-classifier/
├── app.py                      # Aplicación Flask principal
├── config.py                   # Configuración
├── requirements.txt            # Dependencias
├── .env                        # Variables de entorno
├── database/
│   └── schema.sql             # Schema de la base de datos
├── models/
│   ├── __init__.py
│   └── document.py            # Modelos SQLAlchemy
├── services/
│   ├── pdf_processor.py       # Procesamiento de PDFs y OCR
│   ├── classifier.py          # Clasificador ML
│   └── document_service.py    # Lógica de negocio
├── templates/
│   ├── base.html             # Template base
│   ├── dashboard.html        # Dashboard principal
│   ├── pending.html          # Validación de documentos
│   ├── search.html           # Búsqueda de documentos
│   ├── document_detail.html  # Detalle del documento
│   └── settings.html         # Configuración
└── uploads/
    ├── pending/              # PDFs para procesar
    ├── classified/           # PDFs clasificados
    │   ├── Factura/
    │   ├── Nota de Debito/
    │   ├── Nota de Credito/
    │   ├── Remito/
    │   └── Desconocido/
    └── temp/                 # Archivos temporales
```

## 🔌 API Endpoints

### Documentos

- `GET /api/documents` - Listar documentos con filtros
- `GET /api/documents/<id>` - Obtener detalle de documento
- `POST /api/process` - Procesar documentos pendientes
- `POST /api/validate` - Validar un documento
- `POST /api/validate-batch` - Validar múltiples documentos

### Estadísticas

- `GET /api/statistics` - Obtener estadísticas del sistema
- `GET /api/document-types` - Listar tipos de documentos

### Machine Learning

- `POST /api/retrain-model` - Reentrenar el modelo

## 🎨 Tipos de Documentos Soportados

1. **Factura** - Facturas A, B, C
2. **Nota de Débito** - Notas de débito
3. **Nota de Crédito** - Notas de crédito
4. **Remito** - Remitos de entrega
5. **Desconocido** - Documentos no identificados

## 🔍 Búsqueda de Documentos

### Filtros Disponibles

- Tipo de documento
- Estado (pendiente, clasificado, validado, error)
- Rango de fechas
- CUIT
- Proveedor
- Límite de resultados

### Exportación

Los resultados se pueden exportar a CSV desde la interfaz de búsqueda.

## 🧠 Machine Learning

El sistema utiliza:

- **TF-IDF Vectorizer** para extracción de características
- **Naive Bayes Multinomial** para clasificación
- **Clasificación basada en reglas** como fallback

### Mejora Continua

El modelo mejora automáticamente:
1. Los documentos validados se guardan como datos de entrenamiento
2. Cuando hay suficientes datos nuevos, el sistema puede reentrenarse
3. El modelo actualizado mejora la precisión de futuras clasificaciones

## 🛠️ Solución de Problemas

### Error: "Tesseract not found"

Verificar que Tesseract esté instalado y la ruta en `.env` sea correcta:

```env
TESSERACT_PATH=C:/Program Files/Tesseract-OCR/tesseract.exe
```

### Error: "Connection refused" (MySQL)

Verificar que MySQL esté corriendo:

```bash
# Windows
net start MySQL80
```

### Error: "pdf2image" no funciona

Instalar Poppler y agregarlo al PATH del sistema, o especificar la ruta en el código.

## 📈 Futuras Mejoras

- [ ] Soporte para más tipos de archivos (Word, Excel, imágenes)
- [ ] API REST completa con autenticación
- [ ] Procesamiento asíncrono con Celery
- [ ] Dashboard de analíticas avanzadas
- [ ] Integración con servicios en la nube
- [ ] Modelos de Deep Learning (BERT, transformers)
- [ ] Interfaz móvil

## 📝 Licencia

Este proyecto es de código abierto y está disponible bajo la licencia MIT.

## 👨‍💻 Autor

Desarrollado para el sistema de clasificación de documentos PDF.

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Cree una rama para su característica
3. Commit sus cambios
4. Push a la rama
5. Abra un Pull Request

## 📧 Soporte

Para problemas o preguntas, por favor abra un issue en el repositorio.
