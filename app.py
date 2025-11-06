from flask import Flask, render_template, jsonify, request, send_file, redirect, url_for, flash, send_from_directory
from flask_sqlalchemy import SQLAlchemy
import os
import unicodedata
from datetime import datetime
from config import Config
from models import db
from models.document import Document, DocumentType
from services.document_service import DocumentService
import subprocess
import sys

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
                'message': 'Modelo reentrenado exitosamente'
            })
        else:
            return jsonify({
                'success': False,
                'error': 'No hay suficientes datos de entrenamiento. Asegúrate de validar al menos 2 documentos de cada tipo (Factura, Nota de Débito, Nota de Crédito, Remito).'
            }), 400
    except Exception as e:
        error_msg = str(e)
        if 'least populated class' in error_msg or 'less than 2' in error_msg:
            return jsonify({
                'success': False,
                'error': 'Algunas categorías tienen muy pocos ejemplos. Valida al menos 2 documentos de cada tipo antes de reentrenar.'
            }), 400
        return jsonify({
            'success': False,
            'error': f'Error al reentrenar: {error_msg}'
        }), 500

@app.route('/api/open-folder', methods=['POST'])
def api_open_folder():
    """Open a server-side folder in the OS file explorer (development only)."""
    if not app.debug:
        return jsonify({'success': False, 'error': 'Operation disabled in production'}), 403

    data = request.get_json(silent=True) or {}
    folder_key = data.get('folder')
    subfolder = data.get('subfolder')
    if not folder_key:
        return jsonify({'success': False, 'error': 'Missing folder parameter'}), 400

    # Only allow specific named folders to avoid arbitrary path execution
    if folder_key == 'pending':
        path = app.config.get('UPLOAD_FOLDER')
    elif folder_key == 'classified':
        path = app.config.get('CLASSIFIED_FOLDER')
        # If requesting a specific classified subfolder, validate against known types
        if subfolder:
            # Use Config.DOCUMENT_TYPES as whitelist to avoid arbitrary paths
            if subfolder not in Config.DOCUMENT_TYPES:
                return jsonify({'success': False, 'error': 'Invalid subfolder type'}), 400
            path = os.path.join(path, subfolder)
    else:
        return jsonify({'success': False, 'error': 'Invalid folder'}), 400

    if not path or not os.path.exists(path):
        return jsonify({'success': False, 'error': f'Path does not exist: {path}'}), 400

    try:
        if os.name == 'nt':
            # Windows
            os.startfile(path)
        elif sys.platform == 'darwin':
            subprocess.Popen(['open', path])
        else:
            subprocess.Popen(['xdg-open', path])
        return jsonify({'success': True, 'message': f'Abriendo carpeta: {path}'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


# --- Endpoint para servir archivos PDF originales de forma segura ---
from flask import abort

def normalize_filename(name):
    """Normalize filename: keep only letters, numbers, spaces and dot; lowercase; remove accents"""
    if not name:
        return ''
    import re
    # Replace underscores and hyphens with spaces
    name = name.replace('_', ' ').replace('-', ' ')
    # Remove accents
    name = ''.join(
        c for c in unicodedata.normalize('NFD', name)
        if unicodedata.category(c) != 'Mn'
    )
    # Lowercase
    name = name.lower()
    # Remove all non-alphanumeric characters except space and dot
    name = re.sub(r'[^a-z0-9. ]', '', name)
    # Remove multiple spaces
    name = ' '.join(name.split())
    return name

@app.route('/uploads/<folder>/<path:filename>')
def serve_uploaded_file(folder, filename):
    """Serve uploaded PDF files with flexible filename matching"""
    # 1. Buscar en carpeta original (pending o classified)
    search_dirs = []
    uploads_root = os.path.join(app.root_path, 'uploads')
    if folder == 'pending':
        search_dirs.append(os.path.join(uploads_root, 'pending'))
    elif folder == 'classified':
        # Buscar en todas las subcarpetas de classified
        classified_dir = os.path.join(uploads_root, 'classified')
        # Si la URL incluye subcarpeta (tipo), buscar ahí primero
        tipo = os.path.dirname(filename)
        file_only = os.path.basename(filename)
        if tipo:
            search_dirs.append(os.path.join(classified_dir, tipo))
        # Luego buscar en todas las subcarpetas de classified
        for subfolder in os.listdir(classified_dir):
            subdir_path = os.path.join(classified_dir, subfolder)
            if os.path.isdir(subdir_path) and subdir_path not in search_dirs:
                search_dirs.append(subdir_path)
        filename = file_only
    else:
        # Carpeta desconocida, buscar solo ahí
        search_dirs.append(os.path.join(uploads_root, folder))

    # 2. Buscar en cada carpeta
    for uploads_dir in search_dirs:
        if not os.path.isdir(uploads_dir):
            continue
        print(f"DEBUG: Buscando archivo: {filename}")
        print(f"DEBUG: En directorio: {uploads_dir}")
        files_in_dir = os.listdir(uploads_dir)
        # Exact match
        for f in files_in_dir:
            if f.lower() == filename.lower():
                print(f"DEBUG: Archivo encontrado (match exacto): {f}")
                return send_from_directory(uploads_dir, f)
        # Normalized match
        norm_requested = normalize_filename(filename)
        print(f"DEBUG: Buscando versión normalizada: {norm_requested}")
        for f in files_in_dir:
            norm_f = normalize_filename(f)
            print(f"DEBUG: Comparando '{norm_requested}' con '{norm_f}' (archivo: {f})")
            if norm_f == norm_requested:
                print(f"DEBUG: Archivo encontrado (match normalizado): {f}")
                return send_from_directory(uploads_dir, f)
        print(f"DEBUG: Archivo NO encontrado en {uploads_dir}")
    print(f"DEBUG: Archivo NO encontrado en ninguna carpeta: {search_dirs}")
    abort(404)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
