# Achievers Learning Center - Education Platform

A comprehensive Learning Management System (LMS) built with Django for Grade 1-13 students and language courses (German & Japanese).

## Features

### ✅ Currently Working (Demo)
- **User Authentication**: Email-based login with django-allauth
- **Multi-Role System**: Students, Teachers, Parents, Admins
- **Professional Website**: Modern Bootstrap 5 responsive design
- **Django Admin Panel**: Full content management system
- **Database Models**: Complete data structure for LMS
  - User profiles (Student, Teacher, Parent)
  - Course management (Courses, Modules, Lessons, Enrollments)
  - Attendance system (Barcode models, Live Classes)

### ⏳ Under Development (Coming Soon)
- Online payment integration (PayHere, Stripe)
- Live class integration (Zoom API)
- Assignment creation and submission
- Quiz and exam system
- Barcode scanning functionality
- Student/Teacher/Admin dashboards
- Email/SMS notifications
- Advanced analytics and reporting

## Technology Stack

- **Backend**: Django 6.0+ (Python)
- **Database**: SQLite (dev) / PostgreSQL (production)
- **Frontend**: Bootstrap 5, Font Awesome
- **Authentication**: django-allauth
- **Deployment**: Railway (PaaS)
- **Static Files**: Whitenoise

## Local Development Setup

### Prerequisites
- Python 3.11+
- pip

### Installation

1. Clone the repository
```bash
cd d:\achieverslearningcenter.lk
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

3. Run migrations
```bash
python manage.py migrate
```

4. Create superuser
```bash
python create_superuser.py
```

5. Run development server
```bash
python manage.py runserver
```

6. Access the application
- Website: http://localhost:8000
- Admin Panel: http://localhost:8000/admin
- Login: admin@achievers.lk / admin123

## Deploying to Railway

### Step 1: Prepare Your Code

Ensure these files exist (already created):
- `Procfile` - Railway deployment configuration
- `railway.json` - Build settings
- `runtime.txt` - Python version
- `requirements-prod.txt` - Production dependencies with PostgreSQL

### Step 2: Initialize Git Repository

```bash
cd d:\achieverslearningcenter.lk
git init
git add .
git commit -m "Initial commit - Achievers Learning Center LMS"
```

### Step 3: Deploy to Railway

#### Option A: Using Railway CLI

1. Install Railway CLI
```bash
npm install -g @railway/cli
```

2. Login to Railway
```bash
railway login
```

3. Initialize and deploy
```bash
railway init
railway up
```

4. Add PostgreSQL database
```bash
railway add postgres
```

5. Set environment variables (Railway will auto-detect most)
```bash
railway variables set SECRET_KEY=your-secret-key-here
railway variables set DEBUG=False
railway variables set ALLOWED_HOSTS=.railway.app
```

#### Option B: Using Railway Web Dashboard

1. Go to [railway.app](https://railway.app)
2. Click "New Project"
3. Select "Deploy from GitHub repo" or "Deploy from local"
4. Connect your repository
5. Railway will auto-detect Django and deploy
6. Add PostgreSQL:
   - Click "New" → "Database" → "PostgreSQL"
   - Railway will automatically set DATABASE_URL
7. Set environment variables in Settings:
   - `SECRET_KEY` - Generate a secure key
   - `DEBUG` - False
   - `ALLOWED_HOSTS` - .railway.app

### Step 4: Run Migrations on Railway

```bash
railway run python manage.py migrate
railway run python create_superuser.py
```

Or use Railway's web terminal:
1. Open your project
2. Click on your service
3. Go to "Deployments"
4. Open terminal
5. Run:
```bash
python manage.py migrate
python create_superuser.py
```

### Step 5: Access Your Live Site

Railway will provide a URL like: `https://your-app-name.railway.app`

- Website: https://your-app-name.railway.app
- Admin: https://your-app-name.railway.app/admin
- Login: admin@achievers.lk / admin123

## Project Structure

```
achieverslearningcenter.lk/
├── apps/
│   ├── users/          # User models (User, Student, Teacher, Parent)
│   ├── courses/        # Course management
│   ├── attendance/     # Attendance & barcode system
│   ├── dashboard/      # User dashboards
│   └── core/           # Core views (home, about, contact)
├── config/             # Django settings and URLs
├── templates/          # HTML templates
│   ├── base.html
│   └── core/
├── static/             # Static files (CSS, JS, images)
├── media/              # User uploads
├── requirements.txt    # Development dependencies
├── requirements-prod.txt  # Production dependencies
├── Procfile            # Railway deployment
├── railway.json        # Railway configuration
├── runtime.txt         # Python version
└── manage.py           # Django management script
```

## Admin Panel Features

Access the admin panel to manage:

- **Users**: Create and manage students, teachers, parents, admins
- **Courses**: Add courses, modules, and lessons
- **Enrollments**: Enroll students in courses
- **Attendance**: Create live classes and manage attendance
- **Student Barcodes**: Generate QR codes for students

## Demo Credentials

After deployment, create admin user:
- Email: admin@achievers.lk
- Password: admin123

**Note**: Change these credentials in production!

## Environment Variables

Required environment variables for Railway:

- `SECRET_KEY` - Django secret key (generate a secure one)
- `DEBUG` - Set to `False` in production
- `ALLOWED_HOSTS` - Your Railway domain (e.g., `.railway.app`)
- `DATABASE_URL` - Auto-set by Railway PostgreSQL

## Next Steps for Development

1. **Implement Student/Teacher Dashboards**
   - Student dashboard with enrolled courses
   - Teacher dashboard with course management
   - Admin dashboard with analytics

2. **Add Payment Integration**
   - PayHere for Sri Lankan payments
   - Stripe for international payments
   - Automated enrollment after payment

3. **Implement Assignment & Quiz System**
   - Assignment creation and submission
   - Quiz builder with auto-grading
   - Results dashboard

4. **Barcode Attendance System**
   - QR code generation for students
   - Barcode scanning interface
   - Real-time attendance tracking
   - Parent notifications

5. **Live Classes**
   - Zoom API integration
   - Schedule live classes
   - Recording management

## Troubleshooting

### Issue: Static files not loading on Railway
**Solution**: Run `python manage.py collectstatic` during deployment (handled by Procfile)

### Issue: Database connection error
**Solution**: Ensure Railway PostgreSQL is added and DATABASE_URL is set

### Issue: Admin assets not loading
**Solution**: Whitenoise should handle this. Check STATIC_ROOT and STATICFILES_STORAGE in settings.py

### Issue: Migrations not applied
**Solution**: Run migrations using Railway CLI or web terminal:
```bash
railway run python manage.py migrate
```

## Support

For issues or questions:
- Email: info@achievers.lk
- Admin: access the admin panel at /admin/

## License

Copyright © 2026 Achievers Learning Center. All rights reserved.

---

**Built with Django** 🎓
**Deployed on Railway** 🚂
