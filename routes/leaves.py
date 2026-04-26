from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from models.models import LeaveRequest, Faculty
from app import db
from datetime import datetime

leaves_bp = Blueprint('leaves', __name__, url_prefix='/leaves')


def _parse_date(val):
    if not val:
        return None
    try:
        return datetime.strptime(val, '%Y-%m-%d').date()
    except ValueError:
        return None


@leaves_bp.route('/')
@login_required
def index():
    status_f     = request.args.get('status', '')
    faculty_list = Faculty.query.filter_by(status='Active').order_by(Faculty.first_name).all()

    query = LeaveRequest.query
    if status_f:
        query = query.filter_by(approval_status=status_f)
    leaves = query.order_by(LeaveRequest.applied_at.desc()).all()

    pending_count  = LeaveRequest.query.filter_by(approval_status='Pending').count()
    approved_count = LeaveRequest.query.filter_by(approval_status='Approved').count()
    rejected_count = LeaveRequest.query.filter_by(approval_status='Rejected').count()

    return render_template('leaves/index.html',
                           leaves=leaves,
                           faculty_list=faculty_list,
                           status_f=status_f,
                           pending_count=pending_count,
                           approved_count=approved_count,
                           rejected_count=rejected_count)


@leaves_bp.route('/apply', methods=['POST'])
@login_required
def apply():
    lr = LeaveRequest(
        faculty_id  = request.form.get('faculty_id'),
        leave_type  = request.form.get('leave_type', '').strip() or None,
        from_date   = _parse_date(request.form.get('from_date')),
        to_date     = _parse_date(request.form.get('to_date')),
        reason      = request.form.get('reason', '').strip() or None,
    )
    db.session.add(lr)
    db.session.commit()
    flash('Leave application submitted.', 'success')
    return redirect(url_for('leaves.index'))


@leaves_bp.route('/review/<int:leave_id>', methods=['POST'])
@login_required
def review(leave_id):
    lr     = LeaveRequest.query.get_or_404(leave_id)
    action = request.form.get('action')   # 'approve' or 'reject'

    if action == 'approve':
        lr.approval_status = 'Approved'
        flash('Leave request approved.', 'success')
    elif action == 'reject':
        lr.approval_status = 'Rejected'
        flash('Leave request rejected.', 'warning')
    else:
        flash('Invalid action.', 'danger')
        return redirect(url_for('leaves.index'))

    lr.reviewed_by = current_user.admin_id
    lr.reviewed_at = datetime.utcnow()
    db.session.commit()
    return redirect(url_for('leaves.index'))


@leaves_bp.route('/delete/<int:leave_id>', methods=['POST'])
@login_required
def delete(leave_id):
    lr = LeaveRequest.query.get_or_404(leave_id)
    db.session.delete(lr)
    db.session.commit()
    flash('Leave request deleted.', 'success')
    return redirect(url_for('leaves.index'))
