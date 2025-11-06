import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from services import rules

examples = [
    'Factura\nNumero: 100\nTotal: $1200',
    'Remito\nBultos: 2',
    'Nota de credito\nDetalle: devolucion',
    'Nota debito por ajuste\nReferencia: factura 23'
]

for e in examples:
    print('TEXT:', e)
    print('DETECT:', rules.detect_document_keyword(e))
    print('---')
