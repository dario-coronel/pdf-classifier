# 📄 PDF Classifier - Sistema de Clasificación de Documento

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

## 📋 Resumen Ejecutivo

**PDF Classifier** es un sistema inteligente de clasificación automática de documentos PDF que utiliza Machine Learning y OCR para identificar, categorizar y organizar documentos empresariales de forma automatizada.

## ✨ Características Principales
- Clasificación automática de Facturas, Notas de Crédito, Notas de Débito, Remitos y Documentos Desconocidos
- OCR integrado (Tesseract) para procesar documentos escaneados
- Extracción automática de CUIT, proveedor, fecha, número y monto
- Dashboard web moderno, búsqueda avanzada y visualizaciones
- Aprendizaje continuo: el sistema mejora con cada validación

## 💼 Beneficios
- Ahorro de tiempo: hasta 95% menos en clasificación
- Reducción de errores y costos operativos
- Organización y trazabilidad total de documentos
- Escalabilidad: preparado para grandes volúmenes y nuevos tipos

---

# 🎯 Mejores Prácticas y Recomendaciones

## Calidad de los PDFs
- Usa PDFs generados digitalmente o escaneos de al menos 300 DPI
- Evita archivos protegidos, rotados o de baja calidad
- Tamaño recomendado: < 10 MB por documento

## Organización de Archivos
- Usa nombres descriptivos: `{tipo}_{proveedor}_{numero}_{fecha}.pdf`
- Ejemplo: `factura_empresa_sa_0001_20231015.pdf`
- Mantén los archivos en `uploads/pending/` hasta ser procesados

## Flujo de Trabajo Sugerido
1. Carga PDFs en `uploads/pending/`
2. Procesa desde el dashboard
3. Valida y corrige clasificaciones
4. Reentrena el modelo periódicamente

## Mantenimiento y Performance
- Reentrena el modelo tras validar 10+ documentos nuevos
- Realiza backups periódicos de la base de datos y modelos
- Limpia archivos temporales y documentos antiguos

## Seguridad y Escalabilidad
- No expongas la app en producción sin HTTPS y autenticación
- Usa Docker para aislar el entorno y facilitar despliegues
- El sistema puede crecer fácilmente con más datos y usuarios

---

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

## 🚀 Ejecución (SOLO con Docker Compose)


> ⚠️ **IMPORTANTE:** El proyecto debe ejecutarse SIEMPRE usando Docker Compose. No se recomienda ni soporta la ejecución directa en Windows fuera de Docker. Todas las dependencias (incluyendo Poppler y Tesseract) se instalan automáticamente en el contenedor.

1. Copia el archivo `.env.example` a `.env` y revisa que los valores coincidan con los del `docker-compose.yml`:
   ```sh
   cp .env.example .env
   ```

2. Levanta la app y la base de datos con:
   ```sh
   docker-compose up --build
   ```

3. Accede a la aplicación en: [http://localhost:5000](http://localhost:5000)

- La base de datos se inicializa automáticamente con usuario `root` y contraseña `root`.
- Los datos se guardan en el volumen `db_data` (persistente entre reinicios).

**¡Listo! Tu entorno de desarrollo/pruebas está aislado y listo para usar SOLO con Docker.**

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

## ⚙️ Variables de Entorno

Copia `.env.example` a `.env` y configura:
- DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME
- TESSERACT_PATH (ruta a tesseract.exe)
- Otros paths según tu entorno

## 📂 Estructura del Proyecto

```
├── app.py                  # App principal Flask
├── config.py               # Configuración
├── models/                 # Modelos de base de datos y ML
├── services/               # Lógica de negocio y procesamiento
├── templates/              # Vistas HTML (Jinja2)
├── static/                 # Archivos estáticos (css, js, img)
├── uploads/                # PDFs subidos y procesados
├── database/schema.sql     # Esquema de base de datos
├── requirements.txt        # Dependencias Python
├── .env.example            # Ejemplo de configuración
└── ...
```

## ▶️ Uso

1. Inicia el servidor Flask:

```bash
python app.py
```

2. Accede a la app en tu navegador:

```
http://localhost:5000
```

## 🧑‍💻 Contribuir

1. Haz un fork del repositorio
2. Crea una rama: `git checkout -b feature/nueva-funcionalidad`
3. Realiza tus cambios y haz commit
4. Haz push a tu rama: `git push origin feature/nueva-funcionalidad`
5. Abre un Pull Request

## 📄 Licencia

MIT

## 📬 Preguntas Frecuentes (FAQ)

- **¿Dónde se guardan los archivos PDF?**
  - En la carpeta `uploads/` (subcarpetas según estado: pending, classified, temp).
- **¿Cómo agrego nuevos tipos de documento?**
  - Agrega el tipo en la tabla `document_types` de la base de datos y reinicia la app.
- **¿Qué hago si el OCR no reconoce bien el texto?**
  - Asegúrate de tener Tesseract bien instalado y los datos de idioma español.
- **¿Puedo usar otra base de datos?**
  - El sistema está optimizado para MySQL, pero puedes adaptar los modelos para otros motores compatibles con SQLAlchemy.

## 🛠️ Ejemplos de API

- Obtener lista de documentos:
  ```bash
  curl http://localhost:5000/api/documents
  ```
- Validar un documento:
  ```bash
  curl -X POST -H "Content-Type: application/json" \
    -d '{"document_id": 1, "document_type": "Factura", "user": "admin"}' \
    http://localhost:5000/api/validate
  ```
- Reentrenar modelo:
  ```bash
  curl -X POST http://localhost:5000/api/retrain-model
  ```

## 🏆 Badges y Contribución

![Contributions welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg)
![Issues](https://img.shields.io/github/issues/dario-coronel/pdf-classifier)

## 🤝 Soporte y Contacto

¿Tienes dudas, sugerencias o encontraste un bug? Abre un issue en GitHub o contacta a dario.coronel [at] email.com

---

¡Gracias por usar PDF Classifier! Si te resulta útil, dale una estrella ⭐ en GitHub.
