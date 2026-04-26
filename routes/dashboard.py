from flask import Blueprint, render_template
from flask_login import login_required
from models.models import (Faculty, Department, LeaveRequest, Salary,
                            Attendance, PerformanceReview)
from app import db
from sqlalchemy import func
from datetime import date, timedelta
import json

dashboard_bp = Blueprint('dashboard', __name__)


@dashboard_bp.route('/dashboard')
@login_required
def index():
    # ── Summary cards ─────────────────────────────────────────────────────────
    total_faculty     = Faculty.query.filter_by(status='Active').count()
    total_departments = Department.query.count()
    pending_leaves    = LeaveRequest.query.filter_by(approval_status='Pending').count()
    salary_processed  = (db.session.query(func.coalesce(func.sum(Salary.net_salary), 0))
                         .filter_by(salary_status='Paid').scalar()) or 0

    # ── Attendance summary (last 30 days) ─────────────────────────────────────
    thirty_days_ago = date.today() - timedelta(days=30)
    att_present = Attendance.query.filter(
        Attendance.attendance_date >= thirty_days_ago,
        Attendance.status == 'Present'
    ).count()
    att_absent = Attendance.query.filter(
        Attendance.attendance_date >= thirty_days_ago,
        Attendance.status == 'Absent'
    ).count()
    att_leave = Attendance.query.filter(
        Attendance.attendance_date >= thirty_days_ago,
        Attendance.status == 'Leave'
    ).count()

    # ── Performance stats ─────────────────────────────────────────────────────
    avg_rating = (db.session.query(func.avg(PerformanceReview.rating)).scalar()) or 0
    avg_rating = round(float(avg_rating), 2)

    # ── Department-wise faculty count (for chart) ─────────────────────────────
    dept_data = (db.session.query(Department.department_name,
                                  func.count(Faculty.faculty_id))
                 .outerjoin(Faculty, Faculty.department_id == Department.department_id)
                 .group_by(Department.department_id)
                 .all())
    dept_labels = [d[0] for d in dept_data]
    dept_counts = [d[1] for d in dept_data]

    # ── Monthly salary payout (last 6 months) ─────────────────────────────────
    salary_data = (db.session.query(Salary.salary_month,
                                    func.sum(Salary.net_salary))
                   .filter_by(salary_status='Paid')
                   .group_by(Salary.salary_month)
                   .order_by(Salary.salary_month.desc())
                   .limit(6)
                   .all())
    salary_months = [s[0] for s in reversed(salary_data)]
    salary_totals = [float(s[1]) for s in reversed(salary_data)]

    # ── Recent leaves ─────────────────────────────────────────────────────────
    recent_leaves = (LeaveRequest.query
                     .order_by(LeaveRequest.applied_at.desc())
                     .limit(5).all())

    # ── Recent faculty ────────────────────────────────────────────────────────
    recent_faculty = (Faculty.query
                      .order_by(Faculty.faculty_id.desc())
                      .limit(5).all())

    return render_template(
        'dashboard.html',
        total_faculty=total_faculty,
        total_departments=total_departments,
        pending_leaves=pending_leaves,
        salary_processed=salary_processed,
        att_present=att_present,
        att_absent=att_absent,
        att_leave=att_leave,
        avg_rating=avg_rating,
        dept_labels=json.dumps(dept_labels),
        dept_counts=json.dumps(dept_counts),
        salary_months=json.dumps(salary_months),
        salary_totals=json.dumps(salary_totals),
        recent_leaves=recent_leaves,
        recent_faculty=recent_faculty,
    )
