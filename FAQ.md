# ❓ Preguntas Frecuentes (FAQ) - PDF Classifier

## 📑 Índice
1. [General](#general)
2. [Instalación](#instalación)
3. [Uso Diario](#uso-diario)
4. [Técnicas](#técnicas)
5. [Troubleshooting](#troubleshooting)

---

## 🌟 General

### ¿Qué es PDF Classifier?
Es un sistema inteligente que clasifica automáticamente documentos PDF (facturas, remitos, notas de crédito/débito) usando Machine Learning y OCR.

### ¿Necesito conocimientos de programación para usarlo?
No. La interfaz web es intuitiva y no requiere conocimientos técnicos. Solo necesitas saber usar un navegador web.

### ¿Funciona con documentos escaneados?
Sí. El sistema incluye OCR (Tesseract) que puede leer texto de documentos escaneados, aunque los resultados son mejores con PDFs digitales.

### ¿Cuántos documentos puede procesar?
No hay límite estricto. Depende de tu hardware:
- **Computadora básica**: 50-100 docs/día
- **Computadora media**: 200-500 docs/día  
- **Servidor**: 1000+ docs/día

### ¿Cuánto cuesta?
El sistema es gratuito (código abierto). Solo necesitas:
- Computadora con Windows
- MySQL (gratis)
- Python (gratis)
- Tesseract OCR (gratis)

### ¿Necesito conexión a Internet?
No para el funcionamiento básico. Funciona completamente offline. Solo necesitas Internet para instalar las dependencias inicialmente.

---

## 💻 Instalación

### ¿Cuáles son los requisitos mínimos?
- **SO**: Windows 10 o superior
- **RAM**: 4 GB (recomendado 8 GB)
- **Disco**: 10 GB libres
- **CPU**: Dual core o superior

### ¿Cuánto tiempo toma la instalación?
Entre 30 minutos y 2 horas, dependiendo de:
- Velocidad de Internet (para descargas)
- Si ya tienes Python/MySQL instalado
- Tu experiencia técnica

### ¿Puedo instalarlo en Linux o Mac?
Sí, pero necesitarás adaptar los scripts .bat a .sh. El código Python es multiplataforma.

### ¿Necesito permisos de administrador?
Sí, para:
- Instalar Python, MySQL y Tesseract
- Crear carpetas del sistema
- Iniciar servicios (MySQL)

### ¿Qué hago si falla la instalación?
1. Revisa el archivo INSTALL.md
2. Verifica que todos los requisitos estén instalados
3. Lee los mensajes de error
4. Consulta la sección Troubleshooting

---

## 🎯 Uso Diario

### ¿Cómo empiezo a usar el sistema?

**Flujo básico:**
```
1. Copiar PDFs a uploads/pending/
2. Abrir http://localhost:5000
3. Clic en "Procesar Documentos"
4. Ir a "Validar Documentos"
5. Revisar y confirmar clasificaciones
```

### ¿Cuánto tarda en procesar un documento?
- **PDF digital**: 5-15 segundos
- **PDF escaneado**: 20-40 segundos
- **PDF de mala calidad**: hasta 1 minuto

### ¿Qué hago si la clasificación está mal?
1. Ve a "Validar Documentos"
2. Selecciona el tipo correcto del dropdown
3. Haz clic en el botón ✓ verde
4. El sistema aprende de la corrección

### ¿Puedo procesar varios documentos a la vez?
Sí. El sistema procesa todos los PDFs en uploads/pending/ cuando haces clic en "Procesar Documentos".

### ¿Cómo busco un documento específico?
1. Ve a "Buscar Documentos"
2. Usa filtros:
   - Por tipo de documento
   - Por fecha
   - Por CUIT
   - Por proveedor
3. Haz clic en "Buscar"

### ¿Puedo exportar los resultados?
Sí. En la página de búsqueda hay un botón "Exportar" que genera un archivo CSV.

### ¿Qué pasa con los documentos después de validarlos?
Se mueven automáticamente a:
```
uploads/classified/{TipoDocumento}/nombre_archivo.pdf
```

### ¿Puedo deshacer una validación?
No automáticamente. Necesitarías:
1. Mover el archivo manualmente de vuelta a pending/
2. Borrar el registro de la base de datos
3. Volver a procesar

---

## 🔧 Técnicas

### ¿Cómo funciona la clasificación?
El sistema usa dos métodos combinados:
1. **Machine Learning**: TF-IDF + Naive Bayes
2. **Reglas**: Búsqueda de palabras clave

Si ML tiene baja confianza, usa las reglas como fallback.

### ¿Qué es el "score de confianza"?
Un porcentaje (0-100%) que indica qué tan seguro está el sistema de su clasificación:
- **>80%**: Alta confianza ✅
- **60-80%**: Media confianza ⚠️
- **<60%**: Baja confianza ❌

### ¿Cómo mejora el sistema con el tiempo?
Cada vez que validas un documento:
1. Se guarda como dato de entrenamiento
2. Después de 50+ validaciones, puedes reentrenar
3. El modelo aprende los patrones de tus documentos
4. La precisión mejora gradualmente

### ¿Cuándo debo reentrenar el modelo?
- Después de 50+ validaciones nuevas
- Si notas que la precisión es baja
- Cada 1-2 semanas en uso intensivo
- Cuando agregues nuevos tipos de documentos

### ¿Qué datos extrae el sistema?
Del texto del documento intenta identificar:
- **CUIT**: XX-XXXXXXXX-X
- **Proveedor**: Razón social o nombre
- **Fecha**: Del documento
- **Número**: Número de comprobante
- **Monto**: Total del documento

### ¿Por qué algunos datos no se extraen?
Posibles razones:
- Mala calidad del PDF
- Formato no estándar
- OCR con errores
- Documento sin esos datos

### ¿Puedo agregar nuevos tipos de documentos?
Sí, necesitas:
1. Agregar el tipo en la base de datos
2. Actualizar Config.DOCUMENT_TYPES en config.py
3. Crear la carpeta en uploads/classified/
4. Procesar y validar documentos de ese tipo

---

## 🔍 Troubleshooting

### ¿Por qué no se procesa ningún documento?

**Verifica:**
- ¿Los archivos están en uploads/pending/?
- ¿Son archivos PDF válidos?
- ¿El nombre tiene caracteres especiales?
- ¿Hay errores en la consola?

**Solución:**
```cmd
# Ver si hay PDFs
dir uploads\pending\*.pdf

# Ver logs
python app.py
# Luego procesar y ver errores en consola
```

### ¿Por qué la precisión es baja?

**Causas comunes:**
- Pocos documentos validados (< 20)
- Modelo sin entrenar
- PDFs de mala calidad
- Tipos de documentos muy similares

**Solución:**
1. Validar al menos 50 documentos variados
2. Reentrenar el modelo
3. Verificar calidad de PDFs
4. Revisar patrones de error

### ¿Por qué el OCR no funciona bien?

**Causas:**
- Tesseract no instalado correctamente
- Ruta incorrecta en .env
- PDF de muy baja calidad (< 150 DPI)
- Poppler no instalado

**Solución:**
```cmd
# Verificar Tesseract
tesseract --version

# Verificar ruta en .env
echo %TESSERACT_PATH%

# Reinstalar si es necesario
```

### ¿Por qué dice "Error de conexión MySQL"?

**Solución:**
```cmd
# 1. Verificar si MySQL está corriendo
sc query MySQL80

# 2. Iniciar si está detenido
net start MySQL80

# 3. Verificar credenciales en .env
# DB_HOST=localhost
# DB_USER=root
# DB_PASSWORD=tu-password

# 4. Probar conexión
mysql -u root -p
```

### ¿Por qué la aplicación está lenta?

**Causas:**
- Muchos documentos en cola
- Poca RAM disponible
- Base de datos sin índices
- PDFs muy pesados

**Solución:**
1. Procesar en lotes más pequeños
2. Cerrar aplicaciones innecesarias
3. Optimizar base de datos (añadir índices)
4. Comprimir PDFs antes de procesar

### ¿Por qué no puedo validar documentos?

**Verifica:**
- ¿Los documentos están en estado "classified"?
- ¿Hay tipos de documento disponibles?
- ¿La base de datos está actualizada?

**Solución:**
```sql
-- Verificar documento
SELECT id, status, document_type_id 
FROM documents 
WHERE id = TU_ID;

-- Verificar tipos
SELECT * FROM document_types;
```

### ¿Qué hago si se corrompe la base de datos?

**Recuperación:**
```cmd
# 1. Restaurar desde backup
mysql -u root -p pdf_classifier < backup.sql

# 2. Si no hay backup, recrear desde schema
mysql -u root -p
DROP DATABASE pdf_classifier;
CREATE DATABASE pdf_classifier;
source database/schema.sql
```

### ¿Cómo reinicio completamente el sistema?

**Reset completo:**
```cmd
# 1. Detener aplicación (Ctrl+C)

# 2. Limpiar base de datos
mysql -u root -p
DROP DATABASE pdf_classifier;
CREATE DATABASE pdf_classifier;
source database/schema.sql
exit

# 3. Limpiar archivos
rmdir /s /q uploads
rmdir /s /q models

# 4. Reinicializar
python init.py

# 5. Reiniciar
python app.py
```

---

## 💡 Tips y Trucos

### ¿Cómo proceso documentos más rápido?

**Optimizaciones:**
- Usa PDFs digitales (no escaneados) cuando sea posible
- Procesa en lotes de 10-20 documentos
- Aumenta RAM si procesas muchos PDFs grandes
- Usa SSD en lugar de HDD

### ¿Cómo organizo mejor mis documentos?

**Sugerencias:**
- Nombra los archivos descriptivamente
- Agrupa por mes: factura_202310_001.pdf
- Incluye proveedor en el nombre
- No uses caracteres especiales

### ¿Cómo hago backup efectivo?

**Estrategia:**
```cmd
# Diario - carpeta classified
xcopy /E /I /Y uploads\classified backup\%date%\classified

# Semanal - base de datos
mysqldump -u root -p pdf_classifier > backup\%date%_db.sql

# Mensual - todo el sistema
xcopy /E /I /Y c:\Clases\PP3\pdf-classifier backup\%date%\sistema
```

### ¿Cómo monitoreo el sistema?

**Panel rápido:**
```python
# Ver estadísticas rápidas
python -c "from app import app, db; from services.document_service import DocumentService; 
with app.app_context(): 
    service = DocumentService()
    stats = service.get_statistics()
    print(f'Total: {stats[\"total\"]}')
    print(f'Pendientes: {stats[\"pending\"]}')
    print(f'Validados: {stats[\"validated\"]}')"
```

---

## 📞 Soporte

### ¿Dónde encuentro más ayuda?

**Documentación:**
- README.md - Documentación técnica
- INSTALL.md - Guía de instalación
- GUIA_RAPIDA.md - Referencia rápida
- MEJORES_PRACTICAS.md - Optimización

**En el código:**
- Comentarios explicativos
- Docstrings en funciones
- Ejemplos en api_examples.py

### ¿Puedo contribuir al proyecto?
¡Sí! El proyecto es open source. Puedes:
- Reportar bugs
- Sugerir mejoras
- Aportar código
- Mejorar documentación

---

**¿No encuentras tu pregunta?** Revisa la documentación completa o consulta los archivos de ejemplo.

**Última actualización**: Octubre 2025  
**Versión**: 1.0.0
