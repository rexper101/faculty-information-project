from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify
from flask_login import login_required
from models.models import Department, Faculty
from app import db

departments_bp = Blueprint('departments', __name__, url_prefix='/departments')


@departments_bp.route('/')
@login_required
def index():
    q = request.args.get('q', '').strip()
    query = Department.query
    if q:
        query = query.filter(
            db.or_(
                Department.department_name.ilike(f'%{q}%'),
                Department.department_code.ilike(f'%{q}%'),
                Department.hod_name.ilike(f'%{q}%'),
            )
        )
    departments = query.order_by(Department.department_name).all()
    return render_template('departments/index.html', departments=departments, q=q)


@departments_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    if request.method == 'POST':
        name = request.form.get('department_name', '').strip()
        code = request.form.get('department_code', '').strip().upper()
        hod  = request.form.get('hod_name', '').strip()

        if not name or not code:
            flash('Department name and code are required.', 'danger')
            return render_template('departments/form.html', action='Add', dept=None)

        if Department.query.filter_by(department_code=code).first():
            flash('Department code already exists.', 'danger')
            return render_template('departments/form.html', action='Add', dept=None)

        dept = Department(department_name=name, department_code=code, hod_name=hod)
        db.session.add(dept)
        db.session.commit()
        flash(f'Department "{name}" added successfully.', 'success')
        return redirect(url_for('departments.index'))

    return render_template('departments/form.html', action='Add', dept=None)


@departments_bp.route('/edit/<int:dept_id>', methods=['GET', 'POST'])
@login_required
def edit(dept_id):
    dept = Department.query.get_or_404(dept_id)

    if request.method == 'POST':
        name = request.form.get('department_name', '').strip()
        code = request.form.get('department_code', '').strip().upper()
        hod  = request.form.get('hod_name', '').strip()

        if not name or not code:
            flash('Department name and code are required.', 'danger')
            return render_template('departments/form.html', action='Edit', dept=dept)

        existing = Department.query.filter_by(department_code=code).first()
        if existing and existing.department_id != dept_id:
            flash('Department code already exists.', 'danger')
            return render_template('departments/form.html', action='Edit', dept=dept)

        dept.department_name = name
        dept.department_code = code
        dept.hod_name        = hod
        db.session.commit()
        flash(f'Department "{name}" updated successfully.', 'success')
        return redirect(url_for('departments.index'))

    return render_template('departments/form.html', action='Edit', dept=dept)


@departments_bp.route('/delete/<int:dept_id>', methods=['POST'])
@login_required
def delete(dept_id):
    dept = Department.query.get_or_404(dept_id)
    if Faculty.query.filter_by(department_id=dept_id).count() > 0:
        flash('Cannot delete: faculty members are assigned to this department.', 'danger')
        return redirect(url_for('departments.index'))
    db.session.delete(dept)
    db.session.commit()
    flash(f'Department "{dept.department_name}" deleted.', 'success')
    return redirect(url_for('departments.index'))
