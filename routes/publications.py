from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required
from models.models import ResearchPublication, Faculty
from app import db

publications_bp = Blueprint('publications', __name__, url_prefix='/publications')


@publications_bp.route('/<int:faculty_id>')
@login_required
def index(faculty_id):
    fac  = Faculty.query.get_or_404(faculty_id)
    pubs = ResearchPublication.query.filter_by(faculty_id=faculty_id).order_by(
        ResearchPublication.publication_year.desc()).all()
    return render_template('publications/index.html', faculty=fac, publications=pubs)


@publications_bp.route('/<int:faculty_id>/add', methods=['POST'])
@login_required
def add(faculty_id):
    Faculty.query.get_or_404(faculty_id)
    pub = ResearchPublication(
        faculty_id       = faculty_id,
        title            = request.form.get('title', '').strip() or None,
        journal_name     = request.form.get('journal_name', '').strip() or None,
        publication_year = request.form.get('publication_year') or None,
    )
    db.session.add(pub)
    db.session.commit()
    flash('Publication added.', 'success')
    return redirect(url_for('publications.index', faculty_id=faculty_id))


@publications_bp.route('/edit/<int:pub_id>', methods=['POST'])
@login_required
def edit(pub_id):
    pub = ResearchPublication.query.get_or_404(pub_id)
    pub.title            = request.form.get('title', '').strip() or None
    pub.journal_name     = request.form.get('journal_name', '').strip() or None
    pub.publication_year = request.form.get('publication_year') or None
    db.session.commit()
    flash('Publication updated.', 'success')
    return redirect(url_for('publications.index', faculty_id=pub.faculty_id))


@publications_bp.route('/delete/<int:pub_id>', methods=['POST'])
@login_required
def delete(pub_id):
    pub = ResearchPublication.query.get_or_404(pub_id)
    fid = pub.faculty_id
    db.session.delete(pub)
    db.session.commit()
    flash('Publication deleted.', 'success')
    return redirect(url_for('publications.index', faculty_id=fid))
