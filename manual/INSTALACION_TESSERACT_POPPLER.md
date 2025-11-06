# Guía de Instalación - Tesseract OCR y Poppler

## 🔍 Tesseract OCR

### Instalación en Windows

1. Descargar el instalador desde: https://github.com/UB-Mannheim/tesseract/wiki
2. Ejecutar el instalador y seleccionar "Additional language data" → Spanish (spa)
3. Ruta por defecto: C:\Program Files\Tesseract-OCR

Verificar:
```cmd
"C:\Program Files\Tesseract-OCR\tesseract.exe" --version
```

## 📄 Poppler (para pdf2image)

1. Descargar desde: https://github.com/oschwartz10612/poppler-windows/releases/
2. Extraer y copiar a C:\Program Files\poppler (o similar)
3. Añadir `C:\Program Files\poppler\Library\bin` al PATH
