import os
import re
from datetime import datetime
from typing import Dict, Optional, Tuple
import PyPDF2
import pdfplumber
from PIL import Image
import pytesseract
from pdf2image import convert_from_path
from config import Config


class PDFProcessor:
    """Handles PDF text extraction and OCR processing"""
    
    def __init__(self):
        if Config.TESSERACT_PATH and os.path.exists(Config.TESSERACT_PATH):
            pytesseract.pytesseract.tesseract_cmd = Config.TESSERACT_PATH
        
        # Set Poppler path for pdf2image
        self.poppler_path = os.path.join(Config.BASE_DIR, 'poppler-24.08.0', 'Library', 'bin')
    
    def extract_text(self, pdf_path: str) -> Tuple[str, bool]:
        """
        Extract text from PDF using multiple methods
        Returns: (extracted_text, is_from_ocr)
        """
        # First try extracting text directly
        text = self._extract_text_direct(pdf_path)
        
        # If text is too short or empty, use OCR
        if len(text.strip()) < 50:
            print(f"Direct extraction insufficient ({len(text)} chars), using OCR...")
            ocr_text = self._extract_text_ocr(pdf_path)
            if len(ocr_text) > len(text):
                return ocr_text, True
        
        return text, False
    
    def _extract_text_direct(self, pdf_path: str) -> str:
        """Extract text directly from PDF (for searchable PDFs)"""
        text = ""
        
        # Try with pdfplumber first (better for tables and layout)
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
        except Exception as e:
            print(f"pdfplumber extraction failed: {e}")
        
        # If pdfplumber didn't work well, try PyPDF2
        if len(text.strip()) < 50:
            try:
                with open(pdf_path, 'rb') as file:
                    pdf_reader = PyPDF2.PdfReader(file)
                    for page in pdf_reader.pages:
                        page_text = page.extract_text()
                        if page_text:
                            text += page_text + "\n"
            except Exception as e:
                print(f"PyPDF2 extraction failed: {e}")
        
        return text.strip()
    
    def _extract_text_ocr(self, pdf_path: str) -> str:
        """Extract text using OCR (for scanned PDFs)"""
        text = ""
        
        try:
            # Convert PDF to images with Poppler path
            images = convert_from_path(
                pdf_path, 
                dpi=300, 
                first_page=1, 
                last_page=5,
                poppler_path=self.poppler_path
            )
            
            # Process each page with OCR
            for i, image in enumerate(images):
                print(f"Processing page {i+1} with OCR...")
                page_text = pytesseract.image_to_string(image, lang='spa+eng')
                text += page_text + "\n"
        
        except Exception as e:
            print(f"OCR extraction failed: {e}")
            # Try alternative OCR method
            try:
                text = self._ocr_alternative(pdf_path)
            except Exception as e2:
                print(f"Alternative OCR failed: {e2}")
        
        return text.strip()
    
    def _ocr_alternative(self, pdf_path: str) -> str:
        """Alternative OCR method using PIL directly"""
        # This is a fallback - implementation can be expanded
        return ""
    
    def extract_metadata(self, text: str) -> Dict[str, Optional[str]]:
        """Extract metadata from document text"""
        metadata = {
            'cuit': self._extract_cuit(text),
            'provider': self._extract_provider(text),
            'document_date': self._extract_date(text),
            'document_number': self._extract_document_number(text),
            'total_amount': self._extract_amount(text)
        }
        return metadata
    
    def _extract_cuit(self, text: str) -> Optional[str]:
        """Extract CUIT from text"""
        patterns = [
            r'CUIT[:\s]*(\d{2}[-\s]?\d{8}[-\s]?\d{1})',
            r'C\.U\.I\.T[:\s]*(\d{2}[-\s]?\d{8}[-\s]?\d{1})',
            r'(\d{2}[-\s]\d{8}[-\s]\d{1})',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                cuit = match.group(1).replace(' ', '').replace('-', '')
                if len(cuit) == 11 and cuit.isdigit():
                    return f"{cuit[:2]}-{cuit[2:10]}-{cuit[10]}"
        
        return None
    
    def _extract_provider(self, text: str) -> Optional[str]:
        """Extract provider/company name from text"""
        # Look for common patterns
        patterns = [
            r'Razón Social[:\s]+([A-ZÁÉÍÓÚ][A-Za-zÁÉÍÓÚáéíóú\s\.]+)',
            r'Proveedor[:\s]+([A-ZÁÉÍÓÚ][A-Za-zÁÉÍÓÚáéíóú\s\.]+)',
            r'Empresa[:\s]+([A-ZÁÉÍÓÚ][A-Za-zÁÉÍÓÚáéíóú\s\.]+)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                provider = match.group(1).strip()
                if 3 < len(provider) < 100:
                    return provider
        
        # Extract from first lines as fallback
        lines = text.split('\n')
        for line in lines[:10]:
            line = line.strip()
            if len(line) > 5 and len(line) < 100 and not any(kw in line.lower() for kw in ['factura', 'nota', 'remito', 'cuit']):
                if re.match(r'^[A-ZÁÉÍÓÚ]', line):
                    return line
        
        return None
    
    def _extract_date(self, text: str) -> Optional[str]:
        """Extract document date"""
        patterns = [
            r'Fecha[:\s]+(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})',
            r'(\d{1,2}[/-]\d{1,2}[/-]\d{4})',
            r'(\d{4}[/-]\d{1,2}[/-]\d{1,2})',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                date_str = match.group(1)
                try:
                    # Try different date formats
                    for fmt in ['%d/%m/%Y', '%d-%m-%Y', '%Y/%m/%d', '%Y-%m-%d', '%d/%m/%y']:
                        try:
                            date_obj = datetime.strptime(date_str, fmt)
                            return date_obj.strftime('%Y-%m-%d')
                        except ValueError:
                            continue
                except Exception:
                    pass
        
        return None
    
    def _extract_document_number(self, text: str) -> Optional[str]:
        """Extract document number"""
        patterns = [
            r'N[°º]\s*(\d{4}-\d{8})',
            r'Número[:\s]+(\d{4}-\d{8})',
            r'Nro[:\s]+(\d{4}-\d{8})',
            r'(\d{4}-\d{8})',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1)
        
        return None
    
    def _extract_amount(self, text: str) -> Optional[str]:
        """Extract total amount"""
        patterns = [
            r'Total[:\s]+\$?\s*(\d{1,3}(?:[.,]\d{3})*[.,]\d{2})',
            r'Importe Total[:\s]+\$?\s*(\d{1,3}(?:[.,]\d{3})*[.,]\d{2})',
            r'Total a Pagar[:\s]+\$?\s*(\d{1,3}(?:[.,]\d{3})*[.,]\d{2})',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                amount = match.group(1).replace('.', '').replace(',', '.')
                try:
                    return str(float(amount))
                except ValueError:
                    pass
        
        return None
