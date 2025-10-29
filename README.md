# 📄 PDF Classifier - Sistema de Clasificación de Documento

Sistema avanzado de clasificación automática de documentos PDF usando Machine Learning, OCR y extracción inteligente de datos.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.0-green.svg)
![MySQL](https://img.shields.io/badge/MySQL-8.0-orange.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 🚀 Características

## 📚 Documentación consolidada

La documentación de usuario (Guía Rápida, Instalación, FAQ, Mejores Prácticas y otros) se ha consolidado dentro de la carpeta `manual/` en la raíz del proyecto. Para una experiencia de lectura ordenada, abrir:

- `manual/GUIA_RAPIDA.md`
- `manual/INSTALL.md`
- `manual/FAQ.md`
- `manual/MEJORES_PRACTICAS.md`
- `manual/INSTALACION_TESSERACT_POPPLER.md`
- `manual/ESTRUCTURA.md`
- `manual/ESTADO_INSTALACION.md`
- `manual/RESUMEN_EJECUTIVO.md`

Mantuvimos `README.md` como índice principal y entrada rápida; toda la documentación extensa está ahora en `manual/`.


- **Clasificación Automática**: Utiliza Machine Learning para clasificar documentos en categorías predefinidas
- **OCR Integrado**: Extrae texto de documentos escaneados usando Tesseract
- **Extracción de Datos**: Identifica automáticamente CUIT, proveedor, fecha, número de documento y montos
- **Dashboard Profesional**: Interfaz web moderna con Bootstrap y visualizaciones
- **Búsqueda Avanzada**: Busca documentos por tipo, fecha, CUIT, proveedor, etc.
- **Validación Manual**: Permite validar y corregir clasificaciones automáticas
- **Reentrenamiento**: El modelo aprende de las validaciones para mejorar continuamente
- **Base de Datos MySQL**: Almacenamiento robusto y escalable

## 🆕 Novedades recientes (Oct 2025)

- Leyendas del dashboard mejoradas: los porcentajes en las leyendas ahora se muestran con 1 decimal y no se cortan visualmente.
- Colores consistentes en los gráficos: cada tipo de documento tiene un color fijo en todos los gráficos (facilita identificación visual).
- Botón "Abrir Carpeta" en la vista de `Configuración`: ahora podés abrir desde la UI la carpeta `uploads/pending`, la carpeta `uploads/classified` o una subcarpeta por tipo. Nota: esta acción solo funciona cuando la aplicación corre en modo desarrollo/debug y en la misma máquina donde corre el servidor.

Estas mejoras son orientadas a facilitar la revisión visual de estadísticas y la apertura rápida de carpetas cuando trabajás localmente.

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

## 📚 Regenerar documentación estática (HTML)

Si actualizás los archivos Markdown en `manual/` y querés generar HTML estático en `manual/html/`, ejecutá:

```cmd
tools\gen_docs.bat
```

El script activará el `venv` (si existe) y ejecutará `tools/md_to_html.py`.


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

### Abrir carpetas desde la UI

En la vista `Configuración` ahora hay botones para abrir carpetas directamente desde la interfaz:

- **Abrir Carpeta de Carga** -> abre `uploads/pending`.
- **Abrir Carpeta de Clasificados** -> abre `uploads/classified`.
- **Abrir subcarpeta por tipo** -> seleccioná un tipo y se abrirá `uploads/classified/<Tipo>`.

Importante: Esto solo funciona si la aplicación se está ejecutando en la misma máquina (localhost) y en modo debug (desarrollo). Si accedés a la app desde otra máquina o en producción, la acción fallará de forma segura y la UI mostrará la ruta que debés abrir manualmente.

### Notas para desarrolladores

- La ruta del backend para esta acción es `POST /api/open-folder` y está protegida para que funcione únicamente en `app.debug == True`.
- El servidor valida `subfolder` contra la lista de tipos definida en `Config.DOCUMENT_TYPES` para evitar abrir rutas arbitrarias.
- En Windows se usa `os.startfile(path)`, en macOS `open` y en Linux `xdg-open`.

### Troubleshooting rápido

- Si al hacer clic no pasa nada: verificá la consola del navegador (F12 → Console) para errores JS y la salida del servidor para tracebacks.
- Si el servidor corre en una VM o contenedor remoto, la función de abrir carpeta no podrá abrir el Explorador en tu máquina local — usar el fallback que indica la ruta en disco.
- Si la carpeta no existe, revisá que las rutas en `config.py` sean correctas y que las carpetas se hayan creado (la app crea las carpetas al iniciarse si están ausentes).

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
