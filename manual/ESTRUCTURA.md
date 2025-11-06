# 📁 Estructura del Proyecto PDF Classifier

```
pdf-classifier/
│
├── README.md
├── INSTALL.md
├── GUIA_RAPIDA.md
├── requirements.txt
├── .env.example
├── .env
├── .gitignore
│
├── app.py
├── config.py
├── init.py
├── test_classifier.py
├── process_batch.py
├── api_examples.py
│
├── start.bat
├── run.bat
│
├── database/
│   └── schema.sql
│
├── models/
│   ├── __init__.py
│   └── document.py
│
├── services/
│   ├── __init__.py
│   ├── pdf_processor.py
│   ├── classifier.py
│   └── document_service.py
│
├── templates/
│   ├── base.html
│   ├── dashboard.html
│   ├── pending.html
│   ├── search.html
│   ├── document_detail.html
│   └── settings.html
│
├── uploads/
│   ├── pending/
│   ├── classified/
│   │   ├── Factura/
│   │   ├── Nota de Credito/
│   │   ├── Nota de Debito/
│   │   ├── Remito/
│   │   └── Desconocido/
│   └── temp/
│
└── models/
    ├── classifier_model.pkl
    ├── vectorizer.pkl
    └── classifier_model_labels.pkl

---

Última actualización: Octubre 2025
