-- ═══════════════════════════════════════════════════════════════
--  Faculty Information System — Database Schema
--  MySQL 8.0+
-- ═══════════════════════════════════════════════════════════════

CREATE DATABASE IF NOT EXISTS faculty_db
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE faculty_db;

-- ── Admin users ───────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS admin_users (
    admin_id      INT          AUTO_INCREMENT PRIMARY KEY,
    username      VARCHAR(50)  UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at    TIMESTAMP    DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- ── Departments ───────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS departments (
    department_id   INT         AUTO_INCREMENT PRIMARY KEY,
    department_name VARCHAR(100) NOT NULL,
    department_code VARCHAR(20)  UNIQUE NOT NULL,
    hod_name        VARCHAR(100)
) ENGINE=InnoDB;

-- ── Faculty ───────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS faculty (
    faculty_id      INT          AUTO_INCREMENT PRIMARY KEY,
    employee_code   VARCHAR(20)  UNIQUE NOT NULL,
    first_name      VARCHAR(50)  NOT NULL,
    last_name       VARCHAR(50)  NOT NULL,
    gender          ENUM('Male','Female','Other'),
    date_of_birth   DATE,
    mobile_number   VARCHAR(15),
    email           VARCHAR(100) UNIQUE,
    address_line1   VARCHAR(255),
    address_line2   VARCHAR(255),
    city            VARCHAR(50),
    state           VARCHAR(50),
    pincode         VARCHAR(10),
    country         VARCHAR(50)  DEFAULT 'India',
    joining_date    DATE,
    designation     VARCHAR(100),
    employment_type VARCHAR(50)  DEFAULT 'Full-Time',
    department_id   INT,
    status          ENUM('Active','Inactive') DEFAULT 'Active',
    profile_image   VARCHAR(255),
    FOREIGN KEY (department_id) REFERENCES departments(department_id)
        ON DELETE SET NULL
) ENGINE=InnoDB;

-- ── Qualifications ────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS qualifications (
    qualification_id INT          AUTO_INCREMENT PRIMARY KEY,
    faculty_id       INT,
    degree_name      VARCHAR(100),
    institution_name VARCHAR(150),
    passing_year     YEAR,
    percentage       DECIMAL(5,2),
    FOREIGN KEY (faculty_id) REFERENCES faculty(faculty_id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- ── Experience ────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS experience (
    experience_id       INT          AUTO_INCREMENT PRIMARY KEY,
    faculty_id          INT,
    organization_name   VARCHAR(150),
    designation         VARCHAR(100),
    start_date          DATE,
    end_date            DATE,
    years_of_experience DECIMAL(4,2),
    FOREIGN KEY (faculty_id) REFERENCES faculty(faculty_id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- ── Documents ─────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS documents (
    document_id   INT          AUTO_INCREMENT PRIMARY KEY,
    faculty_id    INT,
    document_name VARCHAR(100),
    file_path     VARCHAR(255),
    upload_date   TIMESTAMP    DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (faculty_id) REFERENCES faculty(faculty_id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- ── Research publications ─────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS research_publications (
    publication_id   INT          AUTO_INCREMENT PRIMARY KEY,
    faculty_id       INT,
    title            VARCHAR(255),
    journal_name     VARCHAR(255),
    publication_year YEAR,
    FOREIGN KEY (faculty_id) REFERENCES faculty(faculty_id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- ── Performance reviews ───────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS performance_reviews (
    review_id   INT          AUTO_INCREMENT PRIMARY KEY,
    faculty_id  INT,
    review_year YEAR,
    rating      DECIMAL(3,2),
    remarks     TEXT,
    FOREIGN KEY (faculty_id) REFERENCES faculty(faculty_id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- ── Salary ────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS salary (
    salary_id     INT          AUTO_INCREMENT PRIMARY KEY,
    faculty_id    INT,
    basic_salary  DECIMAL(10,2),
    allowances    DECIMAL(10,2) DEFAULT 0,
    deductions    DECIMAL(10,2) DEFAULT 0,
    net_salary    DECIMAL(10,2) GENERATED ALWAYS AS
                    (basic_salary + allowances - deductions) STORED,
    payment_date  DATE,
    salary_month  VARCHAR(20),
    salary_status ENUM('Pending','Paid') DEFAULT 'Pending',
    FOREIGN KEY (faculty_id) REFERENCES faculty(faculty_id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- ── Attendance ────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS attendance (
    attendance_id   INT  AUTO_INCREMENT PRIMARY KEY,
    faculty_id      INT,
    attendance_date DATE,
    check_in_time   TIME,
    check_out_time  TIME,
    status          ENUM('Present','Absent','Leave') DEFAULT 'Present',
    UNIQUE KEY uq_faculty_date (faculty_id, attendance_date),
    FOREIGN KEY (faculty_id) REFERENCES faculty(faculty_id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- ── Leave requests ────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS leave_requests (
    leave_id        INT          AUTO_INCREMENT PRIMARY KEY,
    faculty_id      INT,
    leave_type      VARCHAR(50),
    from_date       DATE,
    to_date         DATE,
    reason          TEXT,
    approval_status ENUM('Pending','Approved','Rejected') DEFAULT 'Pending',
    reviewed_by     INT,
    reviewed_at     DATETIME,
    applied_at      TIMESTAMP    DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (faculty_id)  REFERENCES faculty(faculty_id)     ON DELETE CASCADE,
    FOREIGN KEY (reviewed_by) REFERENCES admin_users(admin_id)   ON DELETE SET NULL
) ENGINE=InnoDB;

-- ═══════════════════════════════════════════════════════════════
--  Sample seed data (optional — remove for production)
-- ═══════════════════════════════════════════════════════════════

INSERT IGNORE INTO departments (department_name, department_code, hod_name) VALUES
  ('Computer Science & Engineering', 'CSE',  'Dr. A. Sharma'),
  ('Electronics & Communication',   'ECE',  'Dr. B. Patel'),
  ('Mechanical Engineering',        'MECH', 'Dr. C. Verma'),
  ('Civil Engineering',             'CIVIL','Dr. D. Gupta'),
  ('Information Technology',        'IT',   'Dr. E. Khan');
