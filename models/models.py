from extensions import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime


# ── Authentication ────────────────────────────────────────────────────────────
class AdminUser(UserMixin, db.Model):
    __tablename__ = 'admin_users'

    admin_id      = db.Column(db.Integer, primary_key=True)
    username      = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at    = db.Column(db.DateTime, default=datetime.utcnow)

    @property
    def id(self):
        return self.admin_id

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<AdminUser {self.username}>'


# ── Department ────────────────────────────────────────────────────────────────
class Department(db.Model):
    __tablename__ = 'departments'

    department_id   = db.Column(db.Integer, primary_key=True)
    department_name = db.Column(db.String(100), nullable=False)
    department_code = db.Column(db.String(20), unique=True, nullable=False)
    hod_name        = db.Column(db.String(100))

    faculty = db.relationship('Faculty', backref='department', lazy=True)

    def __repr__(self):
        return f'<Department {self.department_name}>'


# ── Faculty ───────────────────────────────────────────────────────────────────
class Faculty(db.Model):
    __tablename__ = 'faculty'

    faculty_id      = db.Column(db.Integer, primary_key=True)
    employee_code   = db.Column(db.String(20), unique=True, nullable=False)
    first_name      = db.Column(db.String(50), nullable=False)
    last_name       = db.Column(db.String(50), nullable=False)
    gender          = db.Column(db.Enum('Male', 'Female', 'Other'))
    date_of_birth   = db.Column(db.Date)
    mobile_number   = db.Column(db.String(15))
    email           = db.Column(db.String(100), unique=True)
    address_line1   = db.Column(db.String(255))
    address_line2   = db.Column(db.String(255))
    city            = db.Column(db.String(50))
    state           = db.Column(db.String(50))
    pincode         = db.Column(db.String(10))
    country         = db.Column(db.String(50), default='India')
    joining_date    = db.Column(db.Date)
    designation     = db.Column(db.String(100))
    employment_type = db.Column(db.String(50), default='Full-Time')
    department_id   = db.Column(db.Integer, db.ForeignKey('departments.department_id'))
    status          = db.Column(db.Enum('Active', 'Inactive'), default='Active')
    profile_image   = db.Column(db.String(255))

    qualifications      = db.relationship('Qualification',       backref='faculty', lazy=True, cascade='all, delete-orphan')
    experiences         = db.relationship('Experience',          backref='faculty', lazy=True, cascade='all, delete-orphan')
    documents           = db.relationship('Document',            backref='faculty', lazy=True, cascade='all, delete-orphan')
    publications        = db.relationship('ResearchPublication',  backref='faculty', lazy=True, cascade='all, delete-orphan')
    performance_reviews = db.relationship('PerformanceReview',   backref='faculty', lazy=True, cascade='all, delete-orphan')
    salaries            = db.relationship('Salary',              backref='faculty', lazy=True, cascade='all, delete-orphan')
    attendances         = db.relationship('Attendance',          backref='faculty', lazy=True, cascade='all, delete-orphan')
    leave_requests      = db.relationship('LeaveRequest',        backref='faculty', lazy=True, cascade='all, delete-orphan')

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def __repr__(self):
        return f'<Faculty {self.full_name}>'


# ── Qualifications ────────────────────────────────────────────────────────────
class Qualification(db.Model):
    __tablename__ = 'qualifications'

    qualification_id = db.Column(db.Integer, primary_key=True)
    faculty_id       = db.Column(db.Integer, db.ForeignKey('faculty.faculty_id'))
    degree_name      = db.Column(db.String(100))
    institution_name = db.Column(db.String(150))
    passing_year     = db.Column(db.Integer)
    percentage       = db.Column(db.Numeric(5, 2))


# ── Experience ────────────────────────────────────────────────────────────────
class Experience(db.Model):
    __tablename__ = 'experience'

    experience_id       = db.Column(db.Integer, primary_key=True)
    faculty_id          = db.Column(db.Integer, db.ForeignKey('faculty.faculty_id'))
    organization_name   = db.Column(db.String(150))
    designation         = db.Column(db.String(100))
    start_date          = db.Column(db.Date)
    end_date            = db.Column(db.Date)
    years_of_experience = db.Column(db.Numeric(4, 2))


# ── Documents ─────────────────────────────────────────────────────────────────
class Document(db.Model):
    __tablename__ = 'documents'

    document_id   = db.Column(db.Integer, primary_key=True)
    faculty_id    = db.Column(db.Integer, db.ForeignKey('faculty.faculty_id'))
    document_name = db.Column(db.String(100))
    file_path     = db.Column(db.String(255))
    upload_date   = db.Column(db.DateTime, default=datetime.utcnow)


# ── Research Publications ─────────────────────────────────────────────────────
class ResearchPublication(db.Model):
    __tablename__ = 'research_publications'

    publication_id   = db.Column(db.Integer, primary_key=True)
    faculty_id       = db.Column(db.Integer, db.ForeignKey('faculty.faculty_id'))
    title            = db.Column(db.String(255))
    journal_name     = db.Column(db.String(255))
    publication_year = db.Column(db.Integer)


# ── Performance Reviews ───────────────────────────────────────────────────────
class PerformanceReview(db.Model):
    __tablename__ = 'performance_reviews'

    review_id   = db.Column(db.Integer, primary_key=True)
    faculty_id  = db.Column(db.Integer, db.ForeignKey('faculty.faculty_id'))
    review_year = db.Column(db.Integer)
    rating      = db.Column(db.Numeric(3, 2))
    remarks     = db.Column(db.Text)


# ── Salary ────────────────────────────────────────────────────────────────────
class Salary(db.Model):
    __tablename__ = 'salary'

    salary_id     = db.Column(db.Integer, primary_key=True)
    faculty_id    = db.Column(db.Integer, db.ForeignKey('faculty.faculty_id'))
    basic_salary  = db.Column(db.Numeric(10, 2))
    allowances    = db.Column(db.Numeric(10, 2), default=0)
    deductions    = db.Column(db.Numeric(10, 2), default=0)
    net_salary    = db.Column(db.Numeric(10, 2))
    payment_date  = db.Column(db.Date)
    salary_month  = db.Column(db.String(20))
    salary_status = db.Column(db.Enum('Pending', 'Paid'), default='Pending')


# ── Attendance ────────────────────────────────────────────────────────────────
class Attendance(db.Model):
    __tablename__ = 'attendance'

    attendance_id   = db.Column(db.Integer, primary_key=True)
    faculty_id      = db.Column(db.Integer, db.ForeignKey('faculty.faculty_id'))
    attendance_date = db.Column(db.Date)
    check_in_time   = db.Column(db.Time)
    check_out_time  = db.Column(db.Time)
    status          = db.Column(db.Enum('Present', 'Absent', 'Leave'), default='Present')


# ── Leave Requests ────────────────────────────────────────────────────────────
class LeaveRequest(db.Model):
    __tablename__ = 'leave_requests'

    leave_id        = db.Column(db.Integer, primary_key=True)
    faculty_id      = db.Column(db.Integer, db.ForeignKey('faculty.faculty_id'))
    leave_type      = db.Column(db.String(50))
    from_date       = db.Column(db.Date)
    to_date         = db.Column(db.Date)
    reason          = db.Column(db.Text)
    approval_status = db.Column(db.Enum('Pending', 'Approved', 'Rejected'), default='Pending')
    reviewed_by     = db.Column(db.Integer, db.ForeignKey('admin_users.admin_id'))
    reviewed_at     = db.Column(db.DateTime)
    applied_at      = db.Column(db.DateTime, default=datetime.utcnow)

    reviewer = db.relationship('AdminUser', backref='reviewed_leaves')