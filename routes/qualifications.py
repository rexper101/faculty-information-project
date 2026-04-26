from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required
from models.models import Qualification, Faculty
from app import db
from datetime import datetime

qualifications_bp = Blueprint('qualifications', __name__, url_prefix='/qualifications')


@qualifications_bp.route('/<int:faculty_id>')
@login_required
def index(faculty_id):
    fac  = Faculty.query.get_or_404(faculty_id)
    quals = Qualification.query.filter_by(faculty_id=faculty_id).order_by(
        Qualification.passing_year.desc()).all()
    return render_template('qualifications/index.html', faculty=fac, quals=quals)


@qualifications_bp.route('/<int:faculty_id>/add', methods=['POST'])
@login_required
def add(faculty_id):
    Faculty.query.get_or_404(faculty_id)
    q = Qualification(
        faculty_id       = faculty_id,
        degree_name      = request.form.get('degree_name', '').strip() or None,
        institution_name = request.form.get('institution_name', '').strip() or None,
        passing_year     = request.form.get('passing_year') or None,
        percentage       = request.form.get('percentage') or None,
    )
    db.session.add(q)
    db.session.commit()
    flash('Qualification added.', 'success')
    return redirect(url_for('qualifications.index', faculty_id=faculty_id))


@qualifications_bp.route('/edit/<int:qual_id>', methods=['POST'])
@login_required
def edit(qual_id):
    q = Qualification.query.get_or_404(qual_id)
    q.degree_name      = request.form.get('degree_name', '').strip() or None
    q.institution_name = request.form.get('institution_name', '').strip() or None
    q.passing_year     = request.form.get('passing_year') or None
    q.percentage       = request.form.get('percentage') or None
    db.session.commit()
    flash('Qualification updated.', 'success')
    return redirect(url_for('qualifications.index', faculty_id=q.faculty_id))


@qualifications_bp.route('/delete/<int:qual_id>', methods=['POST'])
@login_required
def delete(qual_id):
    q = Qualification.query.get_or_404(qual_id)
    fid = q.faculty_id
    db.session.delete(q)
    db.session.commit()
    flash('Qualification deleted.', 'success')
    return redirect(url_for('qualifications.index', faculty_id=fid))
