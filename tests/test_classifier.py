"""
Script to test the classification system
"""

from services.classifier import DocumentClassifier

def test_classifier():
    """Test document classifier with sample texts"""
    
    classifier = DocumentClassifier()
    
    test_cases = [
        {
            'text': '''
            FACTURA TIPO A
            ORIGINAL
            Punto de Venta: 0001-00005678
            Fecha: 15/09/2023
            CUIT: 20-12345678-9
            Razón Social: EMPRESA SA
            IVA Responsable Inscripto
            Total: $50,000.00
            ''',
            'expected': 'Factura'
        },
        {
            'text': '''
            NOTA DE CREDITO C
            Número: 0002-00001234
            Fecha: 20/09/2023
            Por devolución de mercadería
            Bonificación aplicada
            Total: $5,000.00
            ''',
            'expected': 'Nota de Credito'
        },
        {
            'text': '''
            NOTA DE DEBITO
            Número: 0003-00000456
            Fecha: 25/09/2023
            Cargo por intereses
            Ajuste de factura original
            Total: $2,500.00
            ''',
            'expected': 'Nota de Debito'
        },
        {
            'text': '''
            REMITO
            Número: 0001-00012345
            Fecha: 30/09/2023
            Destinatario: CLIENTE XYZ
            Bultos: 5
            Transporte: Express SA
            Entrega de mercadería
            ''',
            'expected': 'Remito'
        },
        {
            'text': '''
            Este es un documento genérico sin formato
            específico que no coincide con ningún tipo
            conocido de documento fiscal.
            ''',
            'expected': 'Desconocido'
        }
    ]
    
    print("=" * 70)
    print("PDF Classifier - Classification Test")
    print("=" * 70)
    
    correct = 0
    total = len(test_cases)
    
    for i, test in enumerate(test_cases, 1):
        predicted_type, confidence = classifier.classify(test['text'])
        expected_type = test['expected']
        
        is_correct = predicted_type == expected_type
        if is_correct:
            correct += 1
        
        status = "✓ CORRECT" if is_correct else "✗ INCORRECT"
        
        print(f"\nTest {i}/{total}: {status}")
        print(f"Expected:  {expected_type}")
        print(f"Predicted: {predicted_type}")
        print(f"Confidence: {confidence:.2%}")
        print("-" * 70)
    
    accuracy = (correct / total) * 100
    print(f"\nAccuracy: {correct}/{total} ({accuracy:.1f}%)")
    print("=" * 70)

if __name__ == '__main__':
    test_classifier()
