from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required
from models.models import Experience, Faculty
from app import db
from datetime import datetime

experience_bp = Blueprint('experience', __name__, url_prefix='/experience')


def _parse_date(val):
    if not val:
        return None
    try:
        return datetime.strptime(val, '%Y-%m-%d').date()
    except ValueError:
        return None


@experience_bp.route('/<int:faculty_id>')
@login_required
def index(faculty_id):
    fac  = Faculty.query.get_or_404(faculty_id)
    exps = Experience.query.filter_by(faculty_id=faculty_id).order_by(
        Experience.start_date.desc()).all()
    return render_template('experience/index.html', faculty=fac, experiences=exps)


@experience_bp.route('/<int:faculty_id>/add', methods=['POST'])
@login_required
def add(faculty_id):
    Faculty.query.get_or_404(faculty_id)
    exp = Experience(
        faculty_id          = faculty_id,
        organization_name   = request.form.get('organization_name', '').strip() or None,
        designation         = request.form.get('designation', '').strip() or None,
        start_date          = _parse_date(request.form.get('start_date')),
        end_date            = _parse_date(request.form.get('end_date')),
        years_of_experience = request.form.get('years_of_experience') or None,
    )
    db.session.add(exp)
    db.session.commit()
    flash('Experience record added.', 'success')
    return redirect(url_for('experience.index', faculty_id=faculty_id))


@experience_bp.route('/edit/<int:exp_id>', methods=['POST'])
@login_required
def edit(exp_id):
    exp = Experience.query.get_or_404(exp_id)
    exp.organization_name   = request.form.get('organization_name', '').strip() or None
    exp.designation         = request.form.get('designation', '').strip() or None
    exp.start_date          = _parse_date(request.form.get('start_date'))
    exp.end_date            = _parse_date(request.form.get('end_date'))
    exp.years_of_experience = request.form.get('years_of_experience') or None
    db.session.commit()
    flash('Experience updated.', 'success')
    return redirect(url_for('experience.index', faculty_id=exp.faculty_id))


@experience_bp.route('/delete/<int:exp_id>', methods=['POST'])
@login_required
def delete(exp_id):
    exp = Experience.query.get_or_404(exp_id)
    fid = exp.faculty_id
    db.session.delete(exp)
    db.session.commit()
    flash('Experience record deleted.', 'success')
    return redirect(url_for('experience.index', faculty_id=fid))
