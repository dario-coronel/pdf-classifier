# 🎯 Mejores Prácticas y Recomendaciones - PDF Classifier

> ⚠️ **IMPORTANTE:** PDF Classifier se ejecuta exclusivamente con Docker Compose. No es necesario instalar dependencias manualmente ni configurar entornos virtuales. Todas las recomendaciones aquí asumen el uso de Docker.

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

### Mantenimiento con Docker

```sh
# Backup de base de datos (desde el contenedor)
docker exec pdf-classifier-db-1 mysqldump -u root -proot pdf_classifier > backup_$(date +%F).sql

# Limpiar archivos temporales
docker exec pdf-classifier-app-1 rm -rf uploads/temp/*
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

El proyecto ya incluye un `Dockerfile` y `docker-compose.yml` listos para usar. Solo debes ejecutar:
```sh
docker-compose up --build
```

---

## 🔍 Solución de Problemas Comunes


### Error: "No se puede conectar a MySQL"

**Diagnóstico y solución:**
1. Asegúrate de que ambos servicios (app y db) estén corriendo con Docker Compose.
2. Verifica que el contenedor de base de datos esté levantado: `docker ps`.
3. Revisa el archivo `.env` y `docker-compose.yml` para que los puertos y credenciales coincidan.


### Error: "Tesseract not found"

**Solución:**
No es necesario instalar Tesseract manualmente. El contenedor Docker ya incluye Tesseract y Poppler. Si ves este error, asegúrate de estar ejecutando la app solo con Docker Compose.


### Error: "Out of Memory"

**Solución:**
- Procesar en lotes más pequeños
- Aumentar recursos asignados al contenedor Docker
- Optimizar procesamiento de imágenes


### Error: "Classification accuracy is low"

**Solución:**
1. Validar más documentos (mínimo 50)
2. Asegurar variedad de tipos
3. Reentrenar el modelo desde el dashboard o la API
4. Revisar calidad de PDFs
5. Ajustar MIN_CONFIDENCE en `.env` si es necesario


### Error: "Slow processing"

**Solución:**
- Optimizar consultas SQL (añadir índices)
- Limitar páginas procesadas por PDF
- Procesar en background con Celery (opcional, requiere modificar el Dockerfile y docker-compose.yml)

---

## 📊 Métricas de Éxito

### KPIs Recomendados

**Precisión del Sistema:**
- Accuracy > 85% en clasificación
- Confianza promedio > 75%
- Tasa de error < 5%

**Eficiencia Operativa:**
- Tiempo de procesamiento < 30s/documento
- Documentos validados/día > 50
- Tiempo de validación < 1 min/documento

**Calidad de Datos:**
- % documentos con metadata completa > 70%
- % CUIT identificados correctamente > 80%
- % fechas extraídas correctamente > 85%

### Dashboard de Monitoreo

```sql
-- Query para dashboard de métricas
SELECT 
    DATE(created_at) as fecha,
    COUNT(*) as total,
    AVG(confidence_score) as confianza_promedio,
    SUM(CASE WHEN is_validated THEN 1 ELSE 0 END) as validados,
    SUM(CASE WHEN status = 'error' THEN 1 ELSE 0 END) as errores
FROM documents
WHERE created_at >= DATE_SUB(NOW(), INTERVAL 7 DAY)
GROUP BY DATE(created_at)
ORDER BY fecha DESC;
```

---

## 📚 Recursos Adicionales


### Documentación Oficial
- Flask: https://flask.palletsprojects.com/
- scikit-learn: https://scikit-learn.org/
- Tesseract: https://github.com/tesseract-ocr/tesseract
- MySQL: https://dev.mysql.com/doc/

### Comunidad y Soporte

- Issues en GitHub (si aplica)
- Stack Overflow tags: python, flask, ocr, ml
- Documentación interna del proyecto

---

**Última actualización**: Octubre 2025  
**Versión**: 1.0.0
