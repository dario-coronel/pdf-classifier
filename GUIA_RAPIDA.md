# Guía Rápida - PDF Classifier

## 📚 ¿Qué hace este sistema?

El **PDF Classifier** es un sistema inteligente que:
- ✅ Clasifica automáticamente documentos PDF (Facturas, Remitos, Notas de Crédito/Débito)
- ✅ Extrae texto con OCR de documentos escaneados
- ✅ Identifica automáticamente datos clave: CUIT, proveedor, fecha, montos
- ✅ Permite validar y corregir clasificaciones
- ✅ Organiza documentos en carpetas por tipo
- ✅ Busca documentos por múltiples criterios
- ✅ Aprende y mejora con cada validación

## 🚀 Inicio Rápido (5 minutos)

### Paso 1: Instalar Requisitos
```cmd
# Instalar Python 3.8+
# Instalar MySQL
# Instalar Tesseract OCR
```

### Paso 2: Configurar Proyecto
```cmd
cd c:\Clases\PP3\pdf-classifier
start.bat
```

### Paso 3: Configurar Base de Datos
```cmd
mysql -u root -p
source database/schema.sql
exit
```

### Paso 4: Editar .env
```env
DB_PASSWORD=tu-contraseña-mysql
TESSERACT_PATH=C:/Program Files/Tesseract-OCR/tesseract.exe
```

### Paso 5: Iniciar
```cmd
run.bat
```

¡Listo! Abre http://localhost:5000

## 📋 Flujo de Trabajo Diario

### 1️⃣ Cargar Documentos
```
Copiar PDFs → uploads/pending/
```

### 2️⃣ Procesar
```
Dashboard → Botón "Procesar Documentos" (sidebar)
```

### 3️⃣ Validar
```
"Validar Documentos" → Revisar clasificaciones → Validar
```

### 4️⃣ Buscar
```
"Buscar Documentos" → Aplicar filtros → Ver resultados
```

## 🎯 Tipos de Documentos

| Tipo | Palabras Clave Detectadas |
|------|---------------------------|
| **Factura** | factura, tipo a/b/c, iva, cae, afip |
| **Nota de Crédito** | nota credito, devolución, bonificación |
| **Nota de Débito** | nota debito, cargo, intereses |
| **Remito** | remito, entrega, bultos, transporte |
| **Desconocido** | Cuando no se identifica el tipo |

## 💡 Consejos de Uso

### Para Mejor Precisión:
- ✅ Usa PDFs de buena calidad
- ✅ Valida al menos 20 documentos antes de confiar 100%
- ✅ Reentrenar modelo después de validar lotes grandes
- ✅ Corrige errores para entrenar el sistema

## 📊 Panel de Control

### Tarjetas de Estadísticas:
- **Total Documentos**: Todos los PDFs procesados
- **Pendientes**: PDFs en carpeta sin procesar
- **Validados**: Documentos confirmados por usuario
- **Errores**: Documentos con problemas

---
