# 🎓 Faculty Information System

A full-featured Faculty Information Management System built with **Flask + MySQL**, featuring a modern responsive dashboard for managing college/institute faculty data.

---

## 📋 Modules

| Module | Features |
|---|---|
| **Authentication** | Admin login/logout, hashed passwords, session management |
| **Dashboard** | KPI cards, bar/line/donut charts, recent activity |
| **Departments** | CRUD, search, faculty count display |
| **Faculty** | Full profiles, photo upload, search, filter, pagination, CSV export |
| **Qualifications** | Multiple degrees per faculty, inline add/edit/delete |
| **Experience** | Work history — organization, designation, dates |
| **Documents** | PDF/image upload, download, delete with validation |
| **Publications** | Research papers with journal/year tracking |
| **Performance** | Yearly ratings (0–5), analytics cards |
| **Salary** | Processing, net calculation, mark paid, printable slip |
| **Attendance** | Daily marking, monthly filter, Present/Absent/Leave |
| **Leave Management** | Apply, approve/reject, history, days auto-calc |

---

## 🛠 Tech Stack

- **Backend**: Python 3.10+ · Flask 3.x · Flask-Login · Flask-SQLAlchemy
- **Database**: MySQL 8.0+ via PyMySQL
- **Frontend**: Bootstrap 5.3 · Bootstrap Icons · Chart.js 4 · Google Fonts (Inter)
- **Auth**: Werkzeug PBKDF2-SHA256 hashing · Flask-Login sessions

---

## 🚀 Quick Start

### 1. Create & activate virtualenv
```bash
python -m venv venv
source venv/bin/activate       # Linux/macOS
venv\Scripts\activate          # Windows
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure environment
```bash
cp .env.example .env
# Edit .env with your MySQL credentials and SECRET_KEY
```

### 4. Create MySQL database
```sql
CREATE DATABASE faculty_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```
Import the schema:
```bash
mysql -u root -p faculty_db < schema.sql
```

### 5. Run the app
```bash
python app.py
```
Visit **http://localhost:5000** — then go to **/setup** to create your first admin account.

---

## 📁 Project Structure

```
faculty_system/
├── app.py              # Flask application factory
├── config.py           # Config (reads .env)
├── requirements.txt
├── .env                # Secrets (never commit)
├── .env.example
├── models/
│   └── models.py       # All SQLAlchemy models
├── routes/             # One Blueprint per module
│   ├── auth.py
│   ├── dashboard.py
│   ├── departments.py
│   ├── faculty.py
│   ├── qualifications.py
│   ├── experience.py
│   ├── documents.py
│   ├── publications.py
│   ├── performance.py
│   ├── salary.py
│   ├── attendance.py
│   └── leaves.py
├── templates/          # Jinja2 HTML templates
│   ├── base.html       # Sidebar + topbar layout
│   ├── login.html
│   ├── dashboard.html
│   ├── departments/
│   ├── faculty/
│   ├── qualifications/
│   ├── experience/
│   ├── documents/
│   ├── publications/
│   ├── performance/
│   ├── salary/
│   ├── attendance/
│   ├── leaves/
│   └── errors/         # 404, 500 pages
├── static/
│   ├── css/style.css   # Custom stylesheet
│   └── js/main.js      # Sidebar, sort, helpers
└── uploads/            # Uploaded documents + profile photos
```

---

## 🔐 Security Notes

- Passwords: **PBKDF2-SHA256** (Werkzeug)
- All routes protected via `@login_required`
- File uploads: extension + 16 MB size validated
- SQL injection: prevented via SQLAlchemy ORM
- **Production**: set `DEBUG=False`, strong `SECRET_KEY`, HTTPS

---

## 📄 License

MIT — free for personal and commercial use.
