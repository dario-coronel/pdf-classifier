
# 📄 PDF Classifier

Sistema avanzado de clasificación automática de documentos PDF usando Machine Learning, OCR y extracción inteligente de datos. Ejecuta SIEMPRE con Docker Compose.

## 🚀 Características

- Clasificación automática de Facturas, Notas de Crédito, Notas de Débito, Remitos y Documentos Desconocidos
- OCR integrado (Tesseract) para procesar documentos escaneados
- Extracción automática de CUIT, proveedor, fecha, número y monto
- Dashboard web moderno, búsqueda avanzada y visualizaciones
- Aprendizaje continuo: el sistema mejora con cada validación
- Base de datos MySQL lista para producción

## 📋 Resumen Ejecutivo

**PDF Classifier** es un sistema inteligente que automatiza la clasificación y organización de documentos PDF empresariales, integrando Machine Learning y OCR en un entorno seguro y reproducible con Docker.

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

---

## � Ejecución rápida (SOLO con Docker Compose)

> ⚠️ **IMPORTANTE:** El proyecto debe ejecutarse SIEMPRE usando Docker Compose. No se soporta la ejecución directa fuera de Docker. Todas las dependencias (incluyendo Poppler y Tesseract) se instalan automáticamente en el contenedor.

1. Clona el repositorio:
   ```sh
   git clone https://github.com/dario-coronel/pdf-classifier.git
   cd pdf-classifier
   ```

2. Copia el archivo `.env.example` a `.env` y ajusta los valores si es necesario:
   ```sh
   cp .env.example .env
   ```

3. Levanta la app y la base de datos:
   ```sh
   docker-compose up --build
   ```

4. Accede a la aplicación en: [http://localhost:5000](http://localhost:5000)

- La base de datos se inicializa automáticamente con usuario `root` y contraseña `root`.
- Los datos se guardan en el volumen `db_data` (persistente entre reinicios).

**¡Listo! Tu entorno de desarrollo/pruebas está aislado y listo para usar SOLO con Docker.**

---






## 🎯 Flujo de Trabajo

1. Sube tus archivos PDF a la carpeta `uploads/pending` (puedes hacerlo desde el host o montando un volumen en Docker).
2. Accede al dashboard web en [http://localhost:5000](http://localhost:5000).
3. Procesa documentos, valida clasificaciones y utiliza las funciones de búsqueda y exportación desde la interfaz.
4. Reentrena el modelo desde el dashboard o usando la API:
   ```sh
   curl -X POST http://localhost:5000/api/retrain-model
   ```

## ⚙️ Variables de Entorno

Copia `.env.example` a `.env` y ajusta los valores si es necesario. Por defecto, los valores funcionan con Docker Compose.


## 📂 Estructura del Proyecto

```
├── app.py                  # App principal Flask
├── config.py               # Configuración
├── models/                 # Modelos de base de datos y ML
├── services/               # Lógica de negocio y procesamiento
├── templates/              # Vistas HTML (Jinja2)
├── uploads/                # PDFs subidos y procesados
├── database/schema.sql     # Esquema de base de datos
├── requirements.txt        # Dependencias Python
├── .env.example            # Ejemplo de configuración
├── docker-compose.yml      # Orquestación de contenedores
├── Dockerfile              # Imagen de la app
└── README.md
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
- **¿Puedo usar otra base de datos?**
   - El sistema está optimizado para MySQL, pero puedes adaptar los modelos para otros motores compatibles con SQLAlchemy.


## 🛠️ Ejemplos de API

- Obtener lista de documentos:
   ```sh
   curl http://localhost:5000/api/documents
   ```
- Validar un documento:
   ```sh
   curl -X POST -H "Content-Type: application/json" \
      -d '{"document_id": 1, "document_type": "Factura", "user": "admin"}' \
      http://localhost:5000/api/validate
   ```
- Reentrenar modelo:
   ```sh
   curl -X POST http://localhost:5000/api/retrain-model
   ```




## 🤝 Soporte y Contacto

¿Tienes dudas, sugerencias o encontraste un bug? Abre un issue en GitHub o contacta a dario.coronel [at] email.com

---


¡Gracias por usar PDF Classifier! Si te resulta útil, dale una estrella ⭐ en GitHub.
