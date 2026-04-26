from flask import (Blueprint, render_template, redirect, url_for, request,
                   flash, make_response)
from flask_login import login_required, current_user
from models.models import Salary, Faculty
from app import db
from datetime import date, datetime
from sqlalchemy import func

salary_bp = Blueprint('salary', __name__, url_prefix='/salary')


@salary_bp.route('/')
@login_required
def index():
    q           = request.args.get('q', '').strip()
    status_f    = request.args.get('status', '')
    month_f     = request.args.get('month', '')

    query = (db.session.query(Salary)
             .join(Faculty, Salary.faculty_id == Faculty.faculty_id))

    if q:
        query = query.filter(
            db.or_(Faculty.first_name.ilike(f'%{q}%'),
                   Faculty.last_name.ilike(f'%{q}%'),
                   Faculty.employee_code.ilike(f'%{q}%'))
        )
    if status_f:
        query = query.filter(Salary.salary_status == status_f)
    if month_f:
        query = query.filter(Salary.salary_month == month_f)

    salaries = query.order_by(Salary.salary_id.desc()).all()
    faculty_list = Faculty.query.filter_by(status='Active').order_by(Faculty.first_name).all()

    total_paid = (db.session.query(func.coalesce(func.sum(Salary.net_salary), 0))
                  .filter_by(salary_status='Paid').scalar()) or 0
    pending_count = Salary.query.filter_by(salary_status='Pending').count()

    return render_template('salary/index.html',
                           salaries=salaries,
                           faculty_list=faculty_list,
                           total_paid=total_paid,
                           pending_count=pending_count,
                           q=q, status_f=status_f, month_f=month_f)


@salary_bp.route('/add', methods=['POST'])
@login_required
def add():
    basic      = float(request.form.get('basic_salary', 0) or 0)
    allowances = float(request.form.get('allowances', 0) or 0)
    deductions = float(request.form.get('deductions', 0) or 0)
    net        = basic + allowances - deductions

    sal = Salary(
        faculty_id    = request.form.get('faculty_id'),
        basic_salary  = basic,
        allowances    = allowances,
        deductions    = deductions,
        net_salary    = net,
        payment_date  = _parse_date(request.form.get('payment_date')),
        salary_month  = request.form.get('salary_month', '').strip() or None,
        salary_status = request.form.get('salary_status', 'Pending'),
    )
    db.session.add(sal)
    db.session.commit()
    flash('Salary record added.', 'success')
    return redirect(url_for('salary.index'))


@salary_bp.route('/mark-paid/<int:sal_id>', methods=['POST'])
@login_required
def mark_paid(sal_id):
    sal = Salary.query.get_or_404(sal_id)
    sal.salary_status = 'Paid'
    sal.payment_date  = date.today()
    db.session.commit()
    flash('Salary marked as Paid.', 'success')
    return redirect(url_for('salary.index'))


@salary_bp.route('/delete/<int:sal_id>', methods=['POST'])
@login_required
def delete(sal_id):
    sal = Salary.query.get_or_404(sal_id)
    db.session.delete(sal)
    db.session.commit()
    flash('Salary record deleted.', 'success')
    return redirect(url_for('salary.index'))


@salary_bp.route('/slip/<int:sal_id>')
@login_required
def slip(sal_id):
    sal = Salary.query.get_or_404(sal_id)
    return render_template('salary/slip.html', salary=sal, faculty=sal.faculty)


def _parse_date(val):
    if not val:
        return None
    try:
        return datetime.strptime(val, '%Y-%m-%d').date()
    except ValueError:
        return None
