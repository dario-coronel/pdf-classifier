# Guía de Instalación - Tesseract OCR y Poppler

## 🔍 Tesseract OCR

### Instalación en Windows

1. **Descargar el instalador**:
   - URL: https://github.com/UB-Mannheim/tesseract/wiki
   - Archivo: tesseract-ocr-w64-setup-5.3.3.20231005.exe (o versión más reciente)
   - Tamaño: ~50 MB

2. **Ejecutar el instalador**:
   ```
   - Doble clic en el archivo descargado
   - Click "Next" en la pantalla de bienvenida
   ```

3. **IMPORTANTE - Seleccionar idiomas**:
   ```
   En la pantalla "Choose Components":
   ✅ Tesseract OCR (obligatorio)
   ✅ Additional language data (required)
      ✅ Spanish - spa (MUY IMPORTANTE para documentos en español)
      ✅ English - eng (recomendado)
   
   Expandir "Additional language data" y marcar:
   [x] Spanish
   [x] English
   ```

4. **Ruta de instalación**:
   ```
   Ruta por defecto: C:\Program Files\Tesseract-OCR
   
   ⚠️ IMPORTANTE: Anota esta ruta, la necesitarás después
   ```

5. **Completar instalación**:
   ```
   - Click "Install"
   - Esperar a que termine (1-2 minutos)
   - Click "Finish"
   ```

### Verificar instalación de Tesseract

Abrir Command Prompt (cmd) y ejecutar:

```cmd
"C:\Program Files\Tesseract-OCR\tesseract.exe" --version
```

Deberías ver algo como:
```
tesseract 5.3.3
 leptonica-1.83.1
  libgif 5.2.1 : libjpeg 8d (libjpeg-turbo 2.1.5.1) : libpng 1.6.40 : libtiff 4.5.1 : zlib 1.2.13 : libwebp 1.3.2
```

---

## 📄 Poppler (para pdf2image)

### Instalación en Windows

1. **Descargar Poppler**:
   - URL: https://github.com/oschwartz10612/poppler-windows/releases/
   - Buscar: "Release-XX.XX.X-0"
   - Descargar: poppler-XX.XX.X_x86.zip (versión más reciente)
   - Tamaño: ~100 MB

2. **Extraer archivos**:
   ```
   - Extraer el archivo ZIP descargado
   - Se creará una carpeta: poppler-XX.XX.X
   - Dentro verás: bin/, include/, lib/, share/
   ```

3. **Copiar a ubicación permanente**:
   ```
   OPCIÓN A - Recomendada (requiere permisos admin):
   Copiar toda la carpeta poppler-XX.XX.X a:
   C:\Program Files\poppler
   
   OPCIÓN B - Alternativa:
   Copiar a cualquier ubicación fija, ejemplo:
   C:\Tools\poppler
   ```

4. **Agregar al PATH del sistema**:

   **Método GUI (recomendado):**
   ```
   1. Click derecho en "Este equipo" → Propiedades
   2. "Configuración avanzada del sistema"
   3. Click "Variables de entorno"
   4. En "Variables del sistema", buscar "Path"
   5. Click "Editar"
   6. Click "Nuevo"
   7. Agregar: C:\Program Files\poppler\Library\bin
      (o la ruta donde copiaste poppler + \Library\bin)
   8. Click "Aceptar" en todas las ventanas
   ```

   **Método CMD (alternativo con permisos admin):**
   ```cmd
   setx /M PATH "%PATH%;C:\Program Files\poppler\Library\bin"
   ```

### Verificar instalación de Poppler

**IMPORTANTE**: Cerrar y abrir nueva ventana de CMD después de modificar PATH

```cmd
pdftoppm -v
```

Deberías ver:
```
pdftoppm version 23.XX.X
Copyright 2005-2023 The Poppler Developers - http://poppler.freedesktop.org
```

---

## ⚙️ Configurar PDF Classifier

Una vez instalados Tesseract y Poppler, configura el archivo .env:

1. **Copiar archivo de ejemplo**:
   ```cmd
   cd c:\Clases\PP3\pdf-classifier
   copy .env.example .env
   ```

2. **Editar .env** (usar Notepad o tu editor favorito):
   ```cmd
   notepad .env
   ```

3. **Configurar las rutas**:
   ```env
   # Flask Configuration
   FLASK_APP=app.py
   FLASK_ENV=development
   SECRET_KEY=tu-clave-secreta-cambiar-en-produccion-123456789

   # Database Configuration
   DB_HOST=localhost
   DB_PORT=3306
   DB_USER=root
   DB_PASSWORD=TU_PASSWORD_MYSQL_AQUI
   DB_NAME=pdf_classifier

   # Folders Configuration
   UPLOAD_FOLDER=uploads/pending
   CLASSIFIED_FOLDER=uploads/classified
   TEMP_FOLDER=uploads/temp

   # OCR Configuration - IMPORTANTE: Ajustar esta ruta
   TESSERACT_PATH=C:/Program Files/Tesseract-OCR/tesseract.exe

   # ML Model Configuration
   MODEL_PATH=models/classifier_model.pkl
   VECTORIZER_PATH=models/vectorizer.pkl
   MIN_CONFIDENCE=0.6
   ```

4. **Guardar y cerrar** el archivo .env

---

## ✅ Verificación Final

Ejecuta estos comandos para verificar que todo está correcto:

```cmd
cd c:\Clases\PP3\pdf-classifier

REM Verificar Python
python --version

REM Verificar MySQL
mysql --version

REM Verificar Tesseract
"C:\Program Files\Tesseract-OCR\tesseract.exe" --version

REM Verificar Poppler
pdftoppm -v

REM Si todos muestran sus versiones, ¡estás listo!
```

---

## 🚀 Siguiente Paso: Inicializar el Sistema

Una vez verificado todo:

```cmd
cd c:\Clases\PP3\pdf-classifier

REM Ejecutar script de inicio
start.bat
```

Esto instalará las dependencias Python y creará la estructura necesaria.

---

## ⚠️ Problemas Comunes

### Tesseract: "No se reconoce como comando"

**Causa**: No está en PATH o ruta incorrecta en .env

**Solución**:
```cmd
REM Usar ruta completa en .env
TESSERACT_PATH=C:/Program Files/Tesseract-OCR/tesseract.exe

REM O agregar a PATH del sistema
```

### Poppler: "pdftoppm no se reconoce"

**Causa**: No está en PATH

**Solución**:
1. Cerrar TODAS las ventanas de CMD
2. Abrir nueva ventana de CMD
3. Probar de nuevo: `pdftoppm -v`
4. Si aún no funciona, verificar que agregaste la ruta correcta al PATH

### Error: "ImportError: DLL load failed"

**Causa**: Falta Microsoft Visual C++ Redistributable

**Solución**:
```
Descargar e instalar:
https://aka.ms/vs/17/release/vc_redist.x64.exe
```

### Tesseract no encuentra idioma español

**Causa**: No se instaló el paquete de idioma español

**Solución**:
1. Desinstalar Tesseract
2. Reinstalar marcando "Spanish" en "Additional language data"
3. O descargar manualmente spa.traineddata de:
   https://github.com/tesseract-ocr/tessdata
4. Copiar a: C:\Program Files\Tesseract-OCR\tessdata\

---

## 📞 Ayuda Adicional

Si tienes problemas:
1. Verifica que las rutas en .env sean correctas
2. Asegúrate de cerrar y reabrir CMD después de cambiar PATH
3. Ejecuta los comandos de verificación uno por uno
4. Revisa que tengas permisos de administrador

---

**Una vez completados estos pasos, estarás listo para ejecutar `start.bat` y comenzar a usar el sistema.**
