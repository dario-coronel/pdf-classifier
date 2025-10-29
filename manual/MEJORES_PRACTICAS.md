# 🎯 Mejores Prácticas y Recomendaciones - PDF Classifier

## 📋 Índice
1. [Uso Óptimo del Sistema](#uso-óptimo-del-sistema)
2. [Mejorando la Precisión](#mejorando-la-precisión)
3. [Mantenimiento](#mantenimiento)
4. [Performance](#performance)
5. [Seguridad](#seguridad)
6. [Escalabilidad](#escalabilidad)
7. [Solución de Problemas Comunes](#solución-de-problemas-comunes)

---

## 🎯 Uso Óptimo del Sistema

### Calidad de los PDFs

✅ **RECOMENDADO**:
- PDFs generados digitalmente (mejor calidad de texto)
- Resolución mínima: 300 DPI para escaneos
- PDFs orientados correctamente
- Tamaño de archivo: < 10 MB por documento
- Formato: PDF/A para mejor compatibilidad

❌ **EVITAR**:
- Escaneos de mala calidad (< 150 DPI)
- PDFs protegidos con contraseña
- PDFs con páginas rotadas
- Archivos muy pesados (> 50 MB)
- Imágenes en formatos no estándar

### Organización de Archivos

```
✅ BIEN:
uploads/pending/
  ├── factura_empresa_a_001.pdf
  ├── factura_empresa_a_002.pdf
  └── remito_proveedor_b_001.pdf

❌ MAL:
uploads/pending/
  ├── documento.pdf
  ├── copia_de_documento.pdf
  └── final_definitivo_v3.pdf
```

### Nomenclatura Sugerida

```
{tipo}_{proveedor}_{numero}_{fecha}.pdf

Ejemplos:
- factura_empresa_sa_0001_20231015.pdf
- remito_proveedor_xyz_5678_20231016.pdf
- nota_credito_comercio_abc_0123_20231017.pdf
```

---

## 🎓 Mejorando la Precisión

### Fase de Entrenamiento Inicial

**Semana 1: Bootstrap**
- Procesar 20-30 documentos variados
- Validar TODOS manualmente
- Corregir clasificaciones incorrectas
- No confiar en clasificaciones automáticas todavía

**Semana 2: Primeros Ajustes**
- Procesar 30-50 documentos más
- Validar clasificaciones con confianza < 80%
- Primer reentrenamiento del modelo
- Empezar a confiar en confianza > 85%

**Mes 1: Consolidación**
- Procesar 100+ documentos
- Reentrenar cada 50 validaciones
- Monitorear mejora de precisión
- Documentar patrones de errores

### Validación Estratégica

**Prioridades de Validación:**

1. 🔴 **Alta Prioridad** (validar siempre):
   - Confianza < 60%
   - Tipo "Desconocido"
   - Primera vez que se ve un proveedor
   - Montos significativos

2. 🟡 **Media Prioridad** (revisar muestra):
   - Confianza 60-80%
   - Proveedores ocasionales
   - Tipos de documento menos comunes

3. 🟢 **Baja Prioridad** (validación aleatoria):
   - Confianza > 80%
   - Proveedores frecuentes
   - Facturas estándar

### Casos de Corrección

**Cuando corregir:**
```
Predicción: Factura (70%)
Correcto: Nota de Crédito
→ CORREGIR Y VALIDAR
```

**Cuando está bien:**
```
Predicción: Factura (95%)
Realidad: Factura Tipo A
→ VALIDAR COMO ESTÁ
```

---

## 🔧 Mantenimiento

### Rutinas Diarias

**Mañana (10 minutos):**
1. Revisar documentos pendientes
2. Procesar lote del día anterior
3. Validar documentos con baja confianza

**Tarde (5 minutos):**
1. Revisar errores de procesamiento
2. Verificar espacio en disco
3. Backup de documentos críticos

### Rutinas Semanales

**Lunes:**
- Reentrenar modelo si hay 50+ validaciones nuevas
- Revisar estadísticas de precisión
- Limpiar carpeta temporal

**Viernes:**
- Backup completo de base de datos
- Exportar estadísticas semanales
- Revisar logs de errores

### Rutinas Mensuales

- Backup completo del sistema
- Análisis de patrones de clasificación
- Actualizar tipos de documentos si es necesario
- Revisar y optimizar configuración
- Limpiar documentos antiguos si es necesario

### Comandos de Mantenimiento

```bash
# Backup de base de datos
mysqldump -u root -p pdf_classifier > backup_%date%.sql

# Limpiar archivos temporales
rmdir /s /q uploads\temp
mkdir uploads\temp

# Ver logs de procesamiento
python -c "from app import app, db; from models.document import ProcessingLog; 
with app.app_context(): 
    logs = ProcessingLog.query.order_by(ProcessingLog.created_at.desc()).limit(10).all()
    for log in logs: print(f'{log.action}: {log.details}')"
```

---

## ⚡ Performance

### Optimización de Procesamiento

**Lotes Óptimos:**
- 10-20 documentos: Procesamiento interactivo
- 50-100 documentos: Procesamiento nocturno
- 100+: Considerar procesamiento paralelo

**Recursos del Sistema:**
```
Mínimo:
- 4 GB RAM
- 2 CPU cores
- 10 GB disco libre

Recomendado:
- 8 GB RAM
- 4 CPU cores
- 50 GB disco libre (con margen)

Óptimo:
- 16 GB RAM
- 8 CPU cores
- 100 GB SSD
```

### Optimización de Base de Datos

**Índices Importantes:**
```sql
-- Verificar índices
SHOW INDEX FROM documents;

-- Añadir índice si falta
CREATE INDEX idx_document_date ON documents(document_date);
CREATE INDEX idx_status_validated ON documents(status, is_validated);
```

**Limpieza Periódica:**
```sql
-- Eliminar logs antiguos (> 6 meses)
DELETE FROM processing_logs 
WHERE created_at < DATE_SUB(NOW(), INTERVAL 6 MONTH);

-- Vaciar training data usado
DELETE FROM ml_training_data 
WHERE used_for_training = TRUE 
AND created_at < DATE_SUB(NOW(), INTERVAL 3 MONTH);
```

### Caché y Optimización

**Configuración Recomendada:**
```python
# config.py - Agregar
CACHE_TYPE = "simple"
CACHE_DEFAULT_TIMEOUT = 300

# Para producción, usar Redis
# CACHE_TYPE = "redis"
# CACHE_REDIS_URL = "redis://localhost:6379/0"
```

---

## 🔒 Seguridad

### Configuración Básica

**Variables de Entorno:**
```env
# ✅ BIEN - .env
SECRET_KEY=tu-clave-aleatoria-muy-larga-y-segura-aqui
DB_PASSWORD=password-fuerte-con-simbolos!123

# ❌ MAL - NO hacer esto
SECRET_KEY=123
DB_PASSWORD=admin
```

### Protección de Archivos

**Permisos de Carpetas:**
```bash
# Windows - Solo lectura para clasificados
icacls uploads\classified /grant Users:(R)

# Escritura solo en pending
icacls uploads\pending /grant Users:(W,R)
```

### Backup Seguro

**Estrategia 3-2-1:**
- 3 copias de datos
- 2 tipos de medios diferentes
- 1 copia offsite

```
Local:
├── Sistema en producción
└── Backup diario en disco externo

Remoto:
└── Backup semanal en la nube
```

### Acceso a la Aplicación

**Para Producción (NO incluido por defecto):**
```python
# Agregar autenticación con Flask-Login
# Agregar HTTPS con certificado SSL
# Agregar rate limiting
# Agregar logging de accesos
```

---

## 📈 Escalabilidad

### Cuando Escalar

**Señales de que necesitas escalar:**
- ⏱️ Procesamiento > 5 minutos para 10 documentos
- 💾 Base de datos > 10 GB
- 📊 > 10,000 documentos/mes
- 👥 Múltiples usuarios simultáneos
- 🌍 Necesidad de acceso remoto

### Opciones de Escalamiento

**Nivel 1: Optimización Local**
```
- Más RAM
- SSD más rápido
- Optimizar consultas SQL
- Caché con Redis
```

**Nivel 2: Procesamiento Distribuido**
```
- Celery para tareas asíncronas
- RabbitMQ o Redis como broker
- Workers en máquinas separadas
```

**Nivel 3: Arquitectura en la Nube**
```
- AWS/Azure/GCP
- Containers (Docker)
- Kubernetes para orquestación
- Base de datos administrada
- CDN para archivos estáticos
```

### Implementación con Docker

```dockerfile
# Dockerfile (ejemplo básico)
FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "app.py"]
```

---

## 🔍 Solución de Problemas Comunes

### Error: "No se puede conectar a MySQL"

**Diagnóstico:**
```cmd
# Verificar si MySQL está corriendo
sc query MySQL80

# Verificar puerto
netstat -an | find "3306"

# Probar conexión
mysql -u root -p -h localhost
```

**Solución:**
```cmd
# Iniciar servicio
net start MySQL80

# Verificar .env
# DB_HOST=localhost
# DB_PORT=3306
```

### Error: "Tesseract not found"

**Diagnóstico:**
```cmd
# Verificar instalación
tesseract --version

# Verificar PATH
echo %PATH% | find "Tesseract"
```

**Solución:**
```cmd
# Instalar Tesseract
# Descargar desde: https://github.com/UB-Mannheim/tesseract/wiki

# Actualizar .env
TESSERACT_PATH=C:/Program Files/Tesseract-OCR/tesseract.exe
```

### Error: "Out of Memory"

**Diagnóstico:**
```python
# Ver uso de memoria
import psutil
print(f"RAM: {psutil.virtual_memory().percent}%")
```

**Solución:**
```
