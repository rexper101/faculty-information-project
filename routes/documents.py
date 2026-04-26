import os
from flask import (Blueprint, render_template, redirect, url_for, request,
                   flash, current_app, send_from_directory, abort)
from flask_login import login_required
from werkzeug.utils import secure_filename
from models.models import Document, Faculty
from app import db

documents_bp = Blueprint('documents', __name__, url_prefix='/documents')

ALLOWED = {'pdf', 'png', 'jpg', 'jpeg', 'gif', 'doc', 'docx', 'txt'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED


@documents_bp.route('/<int:faculty_id>')
@login_required
def index(faculty_id):
    fac  = Faculty.query.get_or_404(faculty_id)
    docs = Document.query.filter_by(faculty_id=faculty_id).order_by(
        Document.upload_date.desc()).all()
    return render_template('documents/index.html', faculty=fac, documents=docs)


@documents_bp.route('/<int:faculty_id>/upload', methods=['POST'])
@login_required
def upload(faculty_id):
    Faculty.query.get_or_404(faculty_id)
    doc_name = request.form.get('document_name', '').strip()
    file = request.files.get('file')

    if not file or not file.filename:
        flash('Please select a file.', 'danger')
        return redirect(url_for('documents.index', faculty_id=faculty_id))

    if not allowed_file(file.filename):
        flash('File type not allowed.', 'danger')
        return redirect(url_for('documents.index', faculty_id=faculty_id))

    folder = os.path.join(current_app.config['UPLOAD_FOLDER'], f'faculty_{faculty_id}')
    os.makedirs(folder, exist_ok=True)
    filename = secure_filename(file.filename)
    # Avoid name collisions
    base, ext = os.path.splitext(filename)
    import time
    filename = f"{base}_{int(time.time())}{ext}"
    file.save(os.path.join(folder, filename))

    doc = Document(
        faculty_id    = faculty_id,
        document_name = doc_name or filename,
        file_path     = f'faculty_{faculty_id}/{filename}',
    )
    db.session.add(doc)
    db.session.commit()
    flash('Document uploaded successfully.', 'success')
    return redirect(url_for('documents.index', faculty_id=faculty_id))


@documents_bp.route('/download/<int:doc_id>')
@login_required
def download(doc_id):
    doc = Document.query.get_or_404(doc_id)
    folder  = current_app.config['UPLOAD_FOLDER']
    parts   = doc.file_path.split('/', 1)
    sub_dir = parts[0] if len(parts) == 2 else ''
    fname   = parts[-1]
    directory = os.path.join(folder, sub_dir) if sub_dir else folder
    return send_from_directory(directory, fname, as_attachment=True,
                               download_name=doc.document_name)


@documents_bp.route('/delete/<int:doc_id>', methods=['POST'])
@login_required
def delete(doc_id):
    doc = Document.query.get_or_404(doc_id)
    fid = doc.faculty_id
    # Delete physical file
    try:
        path = os.path.join(current_app.config['UPLOAD_FOLDER'], doc.file_path)
        if os.path.exists(path):
            os.remove(path)
    except Exception:
        pass
    db.session.delete(doc)
    db.session.commit()
    flash('Document deleted.', 'success')
    return redirect(url_for('documents.index', faculty_id=fid))
