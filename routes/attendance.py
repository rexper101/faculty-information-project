from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required
from models.models import Attendance, Faculty
from app import db
from datetime import date, datetime

attendance_bp = Blueprint('attendance', __name__, url_prefix='/attendance')


def _parse_date(val):
    if not val:
        return None
    try:
        return datetime.strptime(val, '%Y-%m-%d').date()
    except ValueError:
        return None


def _parse_time(val):
    if not val:
        return None
    try:
        return datetime.strptime(val, '%H:%M').time()
    except ValueError:
        return None


@attendance_bp.route('/')
@login_required
def index():
    faculty_list = Faculty.query.filter_by(status='Active').order_by(Faculty.first_name).all()
    month    = request.args.get('month', date.today().strftime('%Y-%m'))
    fac_id   = request.args.get('faculty_id', '', type=str)

    query = Attendance.query
    if month:
        try:
            yr, mo = month.split('-')
            query = query.filter(
                db.extract('year',  Attendance.attendance_date) == int(yr),
                db.extract('month', Attendance.attendance_date) == int(mo),
            )
        except Exception:
            pass
    if fac_id:
        query = query.filter_by(faculty_id=int(fac_id))

    records = query.order_by(Attendance.attendance_date.desc()).all()

    # Stats
    present_count = sum(1 for r in records if r.status == 'Present')
    absent_count  = sum(1 for r in records if r.status == 'Absent')
    leave_count   = sum(1 for r in records if r.status == 'Leave')

    return render_template('attendance/index.html',
                           records=records,
                           faculty_list=faculty_list,
                           month=month,
                           fac_id=fac_id,
                           present_count=present_count,
                           absent_count=absent_count,
                           leave_count=leave_count)


@attendance_bp.route('/mark', methods=['POST'])
@login_required
def mark():
    att = Attendance(
        faculty_id      = request.form.get('faculty_id'),
        attendance_date = _parse_date(request.form.get('attendance_date')) or date.today(),
        check_in_time   = _parse_time(request.form.get('check_in_time')),
        check_out_time  = _parse_time(request.form.get('check_out_time')),
        status          = request.form.get('status', 'Present'),
    )
    db.session.add(att)
    try:
        db.session.commit()
        flash('Attendance marked.', 'success')
    except Exception:
        db.session.rollback()
        flash('Error marking attendance (duplicate entry?).', 'danger')
    return redirect(url_for('attendance.index'))


@attendance_bp.route('/delete/<int:att_id>', methods=['POST'])
@login_required
def delete(att_id):
    att = Attendance.query.get_or_404(att_id)
    db.session.delete(att)
    db.session.commit()
    flash('Attendance record deleted.', 'success')
    return redirect(url_for('attendance.index'))
