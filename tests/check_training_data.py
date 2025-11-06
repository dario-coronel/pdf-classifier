"""
Script para verificar el estado de los datos de entrenamiento
Muestra cuántos documentos validados hay por cada tipo
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app, db
from models.document import Document, DocumentType, MLTrainingData
from sqlalchemy import func

def check_training_data():
    """Verificar datos de entrenamiento disponibles"""
    with app.app_context():
        print("=" * 60)
        print("VERIFICACIÓN DE DATOS DE ENTRENAMIENTO")
        print("=" * 60)
        
        # 1. Documentos validados por tipo
        print("\n1. DOCUMENTOS VALIDADOS (disponibles para reentrenamiento):")
        print("-" * 60)
        
        validated_docs = db.session.query(
            DocumentType.name,
            func.count(Document.id).label('count')
        ).join(Document, Document.document_type_id == DocumentType.id)\
         .filter(Document.status == 'validated')\
         .group_by(DocumentType.name)\
         .all()
        
        total_validated = 0
        min_per_class = float('inf')
        classes_insufficient = []
        
        for doc_type, count in validated_docs:
            status = "✓" if count >= 2 else "✗"
            print(f"{status} {doc_type}: {count} documentos")
            total_validated += count
            if count < min_per_class:
                min_per_class = count
            if count < 2:
                classes_insufficient.append(doc_type)
        
        print(f"\nTotal documentos validados: {total_validated}")
        print(f"Mínimo por clase: {min_per_class}")
        
        # 2. Datos en tabla ml_training_data
        print("\n2. DATOS EN TABLA ML_TRAINING_DATA:")
        print("-" * 60)
        
        training_data_counts = db.session.query(
            DocumentType.name,
            func.count(MLTrainingData.id).label('count')
        ).join(DocumentType, MLTrainingData.correct_type_id == DocumentType.id)\
         .group_by(DocumentType.name)\
         .all()
        
        total_training = 0
        for doc_type, count in training_data_counts:
            status = "✓" if count >= 2 else "✗"
            print(f"{status} {doc_type}: {count} ejemplos")
            total_training += count
        
        print(f"\nTotal ejemplos de entrenamiento: {total_training}")
        
        # 3. Datos NO usados para entrenamiento
        print("\n3. DATOS NUEVOS (no usados aún para reentrenamiento):")
        print("-" * 60)
        
        unused_counts = db.session.query(
            DocumentType.name,
            func.count(MLTrainingData.id).label('count')
        ).join(DocumentType, MLTrainingData.correct_type_id == DocumentType.id)\
         .filter(MLTrainingData.used_for_training == False)\
         .group_by(DocumentType.name)\
         .all()
        
        total_unused = 0
        for doc_type, count in unused_counts:
            status = "✓" if count >= 2 else "✗"
            print(f"{status} {doc_type}: {count} ejemplos nuevos")
            total_unused += count
        
        print(f"\nTotal ejemplos nuevos: {total_unused}")
        
        # 4. Resumen y recomendaciones
        print("\n" + "=" * 60)
        print("RESUMEN Y RECOMENDACIONES:")
        print("=" * 60)
        
        if min_per_class >= 2 and total_validated >= 10:
            print("✓ Hay suficientes datos para reentrenar el modelo")
            print(f"  - Todas las clases tienen al menos 2 ejemplos")
            print(f"  - Total: {total_validated} documentos validados")
        else:
            print("✗ NO hay suficientes datos para reentrenar")
            print("\nProblemas detectados:")
            
            if min_per_class < 2:
                print(f"  - Algunas clases tienen menos de 2 ejemplos")
                if classes_insufficient:
                    print(f"  - Clases insuficientes: {', '.join(classes_insufficient)}")
            
            if total_validated < 10:
                print(f"  - Total de documentos validados ({total_validated}) es menor a 10")
            
            print("\nRecomendaciones:")
            print("  1. Valida más documentos en la sección 'Validar Documentos'")
            print("  2. Asegúrate de validar al menos 2 documentos de cada tipo:")
            print("     - Factura")
            print("     - Nota de Débito")
            print("     - Nota de Crédito")
            print("     - Remito")
            print("  3. Idealmente, valida al menos 5-10 documentos de cada tipo")
            print("     para obtener un modelo más robusto")
        
        # 5. Tipos de documento disponibles
        print("\n" + "=" * 60)
        print("TIPOS DE DOCUMENTO EN EL SISTEMA:")
        print("-" * 60)
        
        all_types = DocumentType.query.filter_by(is_active=True).all()
        for doc_type in all_types:
            print(f"  - {doc_type.name}")
        
        print("\n" + "=" * 60)

if __name__ == '__main__':
    check_training_data()
