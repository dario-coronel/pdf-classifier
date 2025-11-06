import sys
from pathlib import Path
# Ensure project root is on sys.path so 'services' package can be imported when running tests
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from services import rules


def expect(label, text):
    detected, where, kind = rules.detect_document_keyword(text)
    ok = detected == label
    print(f"Text: {text!r}\n -> Detected: {detected} (where={where}, kind={kind}) Expected: {label} -> {'OK' if ok else 'FAIL'}\n")
    return ok


def run():
    tests = [
        ("Factura", "FACTURA\nNumero: 123\nFecha: 2025-10-30\nTotal: $1000"),
        ("Remito", "Remito de entrega\nBultos: 3\nDestino: Cliente"),
        ("Nota de Credito", "Nota de crédito por devolución\nMotivo: mercadería"),
        ("Nota de Debito", "Documento: Nota debito por ajuste\nReferencia: factura 45"),
        (None, "Documento sin palabras clave relevantes. Texto genérico.")
    ]

    failures = 0
    for expected, text in tests:
        ok = expect(expected, text)
        if not ok:
            failures += 1

    if failures:
        print(f"\n{failures} tests failed")
        raise SystemExit(1)
    else:
        print("\nAll tests passed")


if __name__ == '__main__':
    run()
