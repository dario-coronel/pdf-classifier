from flask import Flask, render_template, jsonify, request, send_file, redirect, url_for, flash, send_from_directory
from flask_sqlalchemy import SQLAlchemy
import os
from datetime import datetime
from config import Config
from models import db
from models.document import Document, DocumentType
from services.document_service import DocumentService

app = Flask(__name__)
app.config.from_object(Config)


# Initialize database
db.init_app(app)

# Initialize services
document_service = DocumentService()

# Create tables and folders
with app.app_context():
    Config.init_app(app)
    db.create_all()






@app.route('/')
def index():
    """Main dashboard"""
    stats = document_service.get_statistics()
    recent_docs = Document.query.order_by(Document.created_at.desc()).limit(10).all()
    return render_template('dashboard.html', stats=stats, recent_docs=recent_docs)


# Ejemplo: notificación de error global (puedes usar flash en cualquier vista)
# flash('¡Bienvenido!','success')


@app.route('/api/documents')
def api_documents():
    """Get documents list with filters"""
    filters = {
        'document_type': request.args.get('type'),
        'status': request.args.get('status'),
        'date_from': request.args.get('date_from'),
        'date_to': request.args.get('date_to'),
        'cuit': request.args.get('cuit'),
        'provider': request.args.get('provider'),
        'limit': int(request.args.get('limit', 100))
    }
    
    # Remove None values
    filters = {k: v for k, v in filters.items() if v is not None}
    
    documents = document_service.search_documents(filters)
    
    return jsonify({
        'success': True,
        'documents': [doc.to_dict() for doc in documents]
    })


@app.route('/api/documents/<int:doc_id>')
def api_document_detail(doc_id):
    """Get document details"""
    doc = Document.query.get_or_404(doc_id)
    return jsonify({
        'success': True,
        'document': doc.to_dict()
    })


@app.route('/api/process', methods=['POST'])
def api_process_documents():
    """Process pending documents"""
    try:
        processed_ids = document_service.process_pending_documents()
        return jsonify({
            'success': True,
            'message': f'Processed {len(processed_ids)} documents',
            'document_ids': processed_ids
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/validate', methods=['POST'])
def api_validate_document():
    """Validate a document"""
    data = request.json
    doc_id = data.get('document_id')
    doc_type = data.get('document_type')
    user = data.get('user', 'system')
    
    if not doc_id or not doc_type:
        return jsonify({
            'success': False,
            'error': 'Missing document_id or document_type'
        }), 400
    
    success = document_service.validate_document(doc_id, doc_type, user)
    
    if success:
        return jsonify({
            'success': True,
            'message': 'Document validated successfully'
        })
    else:
        return jsonify({
            'success': False,
            'error': 'Validation failed'
        }), 500


@app.route('/api/validate-batch', methods=['POST'])
def api_validate_batch():
    """Validate multiple documents"""
    data = request.json
    validations = data.get('validations', [])
    
    if not validations:
        return jsonify({
            'success': False,
            'error': 'No validations provided'
        }), 400
    
    success_count = document_service.validate_batch(validations)
    
    return jsonify({
        'success': True,
        'message': f'Validated {success_count}/{len(validations)} documents',
        'validated_count': success_count
    })


@app.route('/api/statistics')
def api_statistics():
    """Get system statistics"""
    stats = document_service.get_statistics()
    return jsonify({
        'success': True,
        'statistics': stats
    })


@app.route('/api/document-types')
def api_document_types():
    """Get all document types"""
    doc_types = DocumentType.query.filter_by(is_active=True).all()
    return jsonify({
        'success': True,
        'document_types': [dt.to_dict() for dt in doc_types]
    })


@app.route('/documents/pending')
def pending_documents():
    """View pending documents for validation"""
    try:
        docs = Document.query.filter_by(status='classified', is_validated=False)\
                             .order_by(Document.created_at.desc()).all()
        doc_types = DocumentType.query.filter_by(is_active=True).all()
        if not docs:
            flash('No hay documentos pendientes para validar.', 'info')
        return render_template('pending.html', documents=docs, document_types=doc_types)
    except Exception as e:
        flash(f'Error al cargar documentos pendientes: {e}', 'danger')
        return render_template('pending.html', documents=[], document_types=[])


@app.route('/documents/search')
def search_documents():
    """Search documents page"""
    try:
        doc_types = DocumentType.query.filter_by(is_active=True).all()
        return render_template('search.html', document_types=doc_types)
    except Exception as e:
        flash(f'Error al cargar tipos de documento: {e}', 'danger')
        return render_template('search.html', document_types=[])


@app.route('/documents/view/<int:doc_id>')
def view_document(doc_id):
    """View document details"""
    try:
        doc = Document.query.get_or_404(doc_id)
        return render_template('document_detail.html', document=doc)
    except Exception as e:
        flash(f'Error al cargar el documento: {e}', 'danger')
        return redirect(url_for('search_documents'))


@app.route('/settings')
def settings():
    """Settings page"""
    try:
        doc_types = DocumentType.query.all()
        return render_template('settings.html', document_types=doc_types)
    except Exception as e:
        flash(f'Error al cargar configuración: {e}', 'danger')
        return render_template('settings.html', document_types=[])


@app.route('/api/retrain-model', methods=['POST'])
def api_retrain_model():
    """Retrain ML model"""
    try:
        success = document_service.retrain_model()
        if success:
            return jsonify({
                'success': True,
                'message': 'Model retrained successfully'
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Not enough training data or retraining failed'
            }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


# --- Endpoint para servir archivos PDF originales de forma segura ---
from flask import abort

@app.route('/uploads/<folder>/<path:filename>')
def serve_uploaded_file(folder, filename):
    """Sirve archivos PDF solo desde las carpetas permitidas de uploads."""
    allowed_folders = ['pending', 'classified', 'temp']
    if folder not in allowed_folders:
        abort(404)
    base_dir = os.path.join(app.root_path, 'uploads', folder)
    # Si es classified, puede haber subcarpetas por tipo
    file_path = os.path.join(base_dir, filename)
    if not os.path.isfile(file_path):
        abort(404)
    return send_from_directory(base_dir, filename)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
