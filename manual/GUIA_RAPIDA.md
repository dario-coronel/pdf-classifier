````markdown
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

### Organización:
- 📁 `uploads/pending/` → PDFs sin procesar
- 📁 `uploads/classified/Factura/` → Facturas validadas
- 📁 `uploads/classified/Remito/` → Remitos validados
- etc.

## 🔍 Búsquedas Útiles

### Buscar facturas del mes actual:
```
Tipo: Factura
Fecha desde: 01/10/2025
Fecha hasta: 31/10/2025
```

### Buscar por proveedor:
```
Proveedor: "nombre del proveedor"
```

### Buscar por CUIT:
```
CUIT: 20-12345678-9
```

### Documentos no validados:
```
Estado: Clasificado
```

## 📊 Panel de Control

### Tarjetas de Estadísticas:
- **Total Documentos**: Todos los PDFs procesados
- **Pendientes**: PDFs en carpeta sin procesar
- **Validados**: Documentos confirmados por usuario
- **Errores**: Documentos con problemas

### Gráficos:
- **Barras**: Cantidad por tipo de documento
- **Torta**: Distribución porcentual

## 🛠️ Acciones Principales

### En Dashboard:
| Acción | Descripción |
|--------|-------------|
| Procesar Documentos | Analiza todos los PDFs en pending/ |
| Reentrenar Modelo | Mejora la IA con validaciones |

### En Validación:
| Acción | Descripción |
|--------|-------------|
| ✓ (verde) | Validar documento individual |
| 👁️ (azul) | Ver detalles completos |
| ✓✓ Validar Seleccionados | Validar múltiples a la vez |

### En Búsqueda:
| Acción | Descripción |
|--------|-------------|
| 🔍 Buscar | Aplicar filtros y buscar |
| ❌ Limpiar | Reset todos los filtros |
| 📊 Exportar | Descargar resultados en CSV |

## 🎨 Estados de Documentos

| Estado | Significado | Color |
|--------|-------------|-------|
| **Pendiente** | En carpeta pending/, sin procesar | Gris |
| **Analizando** | En proceso de análisis | Azul |
| **Clasificado** | Clasificado, esperando validación | Amarillo |
| **Validado** | Confirmado por usuario, movido a carpeta | Verde |
| **Error** | Falló el procesamiento | Rojo |

## 📈 Mejorando la Precisión

### Sistema de Confianza:
- 🟢 **>70%**: Alta confianza, generalmente correcto
- 🟡 **50-70%**: Media confianza, revisar
- 🔴 **<50%**: Baja confianza, probablemente incorrecto

### Reentrenamiento:
```
1. Validar 20+ documentos
2. Sidebar → "Reentrenar Modelo"
3. Esperar confirmación
4. ¡Mejora automática!
```

## 🔧 Solución Rápida de Problemas

| Problema | Solución |
|----------|----------|
| "Tesseract not found" | Verificar ruta en .env |
| Sin conexión MySQL | `net start MySQL80` |
| OCR no funciona | Instalar Poppler, agregar a PATH |
| Baja precisión | Validar más documentos, reentrenar |
| Error al procesar | Verificar calidad del PDF |

## 📱 Atajos de Teclado

- `Ctrl + F` → Buscar en página
- `Ctrl + P` → Imprimir (en detalle de documento)
- `Ctrl + Click` → Abrir en nueva pestaña

## 💾 Backup Recomendado

### Diario:
- Carpeta `uploads/classified/`

### Semanal:
- Base de datos MySQL
- Modelos ML (`models/`)

### Comando backup MySQL:
```cmd
mysqldump -u root -p pdf_classifier > backup_YYYYMMDD.sql
```

## 🎓 Mejores Prácticas

1. **Procesar en lotes**: 10-20 documentos a la vez
2. **Validar inmediatamente**: No dejar documentos clasificados sin validar
3. **Revisar confianza baja**: Siempre verificar <70%
4. **Reentrenar periódicamente**: Cada 20-30 validaciones
5. **Mantener orden**: No acumular PDFs en pending/
6. **Backup regular**: Exportar datos importantes

## 📞 Recursos Adicionales

- **README.md**: Documentación técnica completa
- **INSTALL.md**: Guía de instalación detallada
- **database/schema.sql**: Estructura de base de datos

## 🆘 Soporte

Si encuentras problemas:
1. Revisa los logs en la consola
2. Verifica que todos los servicios estén corriendo
3. Consulta INSTALL.md para troubleshooting
4. Revisa los archivos de error en la base de datos

---

**¡Importante!** Este sistema aprende con el uso. Mientras más documentos valides correctamente, mejor será la clasificación automática.

**Versión**: 1.0.0  
**Última actualización**: Octubre 2025

````
