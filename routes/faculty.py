import os, csv, io
from flask import (Blueprint, render_template, redirect, url_for, request,
                   flash, current_app, send_file, make_response)
from flask_login import login_required
from werkzeug.utils import secure_filename
from models.models import Faculty, Department
from app import db
from datetime import datetime

faculty_bp = Blueprint('faculty', __name__, url_prefix='/faculty')

ALLOWED = {'png', 'jpg', 'jpeg', 'gif', 'webp'}


def allowed_image(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED


def save_profile_image(file, faculty_id):
    ext = file.filename.rsplit('.', 1)[1].lower()
    filename = secure_filename(f'profile_{faculty_id}.{ext}')
    folder = os.path.join(current_app.config['UPLOAD_FOLDER'], 'profiles')
    os.makedirs(folder, exist_ok=True)
    file.save(os.path.join(folder, filename))
    return f'profiles/{filename}'


@faculty_bp.route('/')
@login_required
def index():
    page    = request.args.get('page', 1, type=int)
    q       = request.args.get('q', '').strip()
    dept_id = request.args.get('department_id', '', type=str)
    status  = request.args.get('status', '')
    per_page = current_app.config.get('ITEMS_PER_PAGE', 10)

    query = Faculty.query
    if q:
        query = query.filter(
            db.or_(
                Faculty.first_name.ilike(f'%{q}%'),
                Faculty.last_name.ilike(f'%{q}%'),
                Faculty.employee_code.ilike(f'%{q}%'),
                Faculty.email.ilike(f'%{q}%'),
                Faculty.designation.ilike(f'%{q}%'),
            )
        )
    if dept_id:
        query = query.filter_by(department_id=int(dept_id))
    if status:
        query = query.filter_by(status=status)

    pagination = query.order_by(Faculty.first_name).paginate(
        page=page, per_page=per_page, error_out=False)
    departments = Department.query.order_by(Department.department_name).all()

    return render_template('faculty/index.html',
                           faculty_list=pagination.items,
                           pagination=pagination,
                           departments=departments,
                           q=q, dept_id=dept_id, status=status)


@faculty_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    departments = Department.query.order_by(Department.department_name).all()

    if request.method == 'POST':
        f = request.form
        # Basic validation
        if not f.get('first_name') or not f.get('last_name') or not f.get('employee_code'):
            flash('First name, last name and employee code are required.', 'danger')
            return render_template('faculty/form.html', action='Add', faculty=None,
                                   departments=departments)

        if Faculty.query.filter_by(employee_code=f['employee_code'].strip()).first():
            flash('Employee code already exists.', 'danger')
            return render_template('faculty/form.html', action='Add', faculty=None,
                                   departments=departments)

        fac = Faculty(
            employee_code   = f['employee_code'].strip(),
            first_name      = f['first_name'].strip(),
            last_name       = f['last_name'].strip(),
            gender          = f.get('gender') or None,
            date_of_birth   = _parse_date(f.get('date_of_birth')),
            mobile_number   = f.get('mobile_number', '').strip() or None,
            email           = f.get('email', '').strip() or None,
            address_line1   = f.get('address_line1', '').strip() or None,
            address_line2   = f.get('address_line2', '').strip() or None,
            city            = f.get('city', '').strip() or None,
            state           = f.get('state', '').strip() or None,
            pincode         = f.get('pincode', '').strip() or None,
            country         = f.get('country', 'India').strip() or 'India',
            joining_date    = _parse_date(f.get('joining_date')),
            designation     = f.get('designation', '').strip() or None,
            employment_type = f.get('employment_type', 'Full-Time'),
            department_id   = int(f['department_id']) if f.get('department_id') else None,
            status          = f.get('status', 'Active'),
        )
        db.session.add(fac)
        db.session.flush()  # get faculty_id before commit

        # Profile image
        img = request.files.get('profile_image')
        if img and img.filename and allowed_image(img.filename):
            fac.profile_image = save_profile_image(img, fac.faculty_id)

        db.session.commit()
        flash(f'Faculty "{fac.full_name}" added successfully.', 'success')
        return redirect(url_for('faculty.view', faculty_id=fac.faculty_id))

    return render_template('faculty/form.html', action='Add', faculty=None,
                           departments=departments)


@faculty_bp.route('/view/<int:faculty_id>')
@login_required
def view(faculty_id):
    fac = Faculty.query.get_or_404(faculty_id)
    return render_template('faculty/view.html', faculty=fac)


@faculty_bp.route('/edit/<int:faculty_id>', methods=['GET', 'POST'])
@login_required
def edit(faculty_id):
    fac = Faculty.query.get_or_404(faculty_id)
    departments = Department.query.order_by(Department.department_name).all()

    if request.method == 'POST':
        f = request.form
        if not f.get('first_name') or not f.get('last_name'):
            flash('First name and last name are required.', 'danger')
            return render_template('faculty/form.html', action='Edit', faculty=fac,
                                   departments=departments)

        code = f['employee_code'].strip()
        existing = Faculty.query.filter_by(employee_code=code).first()
        if existing and existing.faculty_id != faculty_id:
            flash('Employee code already exists.', 'danger')
            return render_template('faculty/form.html', action='Edit', faculty=fac,
                                   departments=departments)

        fac.employee_code   = code
        fac.first_name      = f['first_name'].strip()
        fac.last_name       = f['last_name'].strip()
        fac.gender          = f.get('gender') or None
        fac.date_of_birth   = _parse_date(f.get('date_of_birth'))
        fac.mobile_number   = f.get('mobile_number', '').strip() or None
        fac.email           = f.get('email', '').strip() or None
        fac.address_line1   = f.get('address_line1', '').strip() or None
        fac.address_line2   = f.get('address_line2', '').strip() or None
        fac.city            = f.get('city', '').strip() or None
        fac.state           = f.get('state', '').strip() or None
        fac.pincode         = f.get('pincode', '').strip() or None
        fac.country         = f.get('country', 'India').strip() or 'India'
        fac.joining_date    = _parse_date(f.get('joining_date'))
        fac.designation     = f.get('designation', '').strip() or None
        fac.employment_type = f.get('employment_type', 'Full-Time')
        fac.department_id   = int(f['department_id']) if f.get('department_id') else None
        fac.status          = f.get('status', 'Active')

        img = request.files.get('profile_image')
        if img and img.filename and allowed_image(img.filename):
            fac.profile_image = save_profile_image(img, fac.faculty_id)

        db.session.commit()
        flash(f'Faculty "{fac.full_name}" updated successfully.', 'success')
        return redirect(url_for('faculty.view', faculty_id=faculty_id))

    return render_template('faculty/form.html', action='Edit', faculty=fac,
                           departments=departments)


@faculty_bp.route('/delete/<int:faculty_id>', methods=['POST'])
@login_required
def delete(faculty_id):
    fac = Faculty.query.get_or_404(faculty_id)
    name = fac.full_name
    db.session.delete(fac)
    db.session.commit()
    flash(f'Faculty "{name}" deleted.', 'success')
    return redirect(url_for('faculty.index'))


@faculty_bp.route('/export/csv')
@login_required
def export_csv():
    faculty_list = Faculty.query.order_by(Faculty.first_name).all()
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['Employee Code', 'First Name', 'Last Name', 'Gender',
                     'Email', 'Mobile', 'Department', 'Designation',
                     'Employment Type', 'Status', 'Joining Date'])
    for fac in faculty_list:
        writer.writerow([
            fac.employee_code, fac.first_name, fac.last_name,
            fac.gender or '', fac.email or '', fac.mobile_number or '',
            fac.department.department_name if fac.department else '',
            fac.designation or '', fac.employment_type or '',
            fac.status, fac.joining_date or '',
        ])
    output.seek(0)
    response = make_response(output.getvalue())
    response.headers['Content-Disposition'] = 'attachment; filename=faculty_export.csv'
    response.headers['Content-Type'] = 'text/csv'
    return response


def _parse_date(value):
    if not value:
        return None
    try:
        return datetime.strptime(value, '%Y-%m-%d').date()
    except ValueError:
        return None
