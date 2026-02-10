# High-Level Design Document
## Achievers Learning Center - Education Platform

**Version:** 1.0
**Date:** February 10, 2026
**Status:** Draft

---

## 1. Executive Summary

### 1.1 Project Overview
Achievers Learning Center is a comprehensive online education platform designed to deliver hybrid learning experiences for students from Grade 1 to Grade 13, along with specialized language courses (German and Japanese). The platform combines physical classroom management, live online classes, and recorded course delivery with integrated student/teacher dashboards, assessment systems, and flexible payment options.

### 1.2 Business Objectives
- Provide seamless learning experiences across physical, online, and hybrid modes
- Enable efficient course management and student progress tracking
- Support multiple revenue streams through flexible enrollment and payment options
- Scale to accommodate growing student base and course offerings
- Establish a modern, attractive brand presence in the education sector

### 1.3 Target Audience
- **Primary Students** (Grade 1-5): Foundation subjects with engaging, interactive content
- **Middle School Students** (Grade 6-9): Advanced curriculum with multimedia resources
- **High School Students** (Grade 10-13): O/L and A/L exam preparation
- **Language Learners**: German and Japanese language courses for all ages
- **Parents**: Monitoring student progress and managing enrollments
- **Teachers**: Course delivery, assessment, and student management

---

## 2. System Architecture

### 2.1 High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      Client Layer                            │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │  Web App │  │  Mobile  │  │  Admin   │  │  Teacher │   │
│  │ (Student)│  │   App    │  │  Panel   │  │  Portal  │   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │
└─────────────────────────────────────────────────────────────┘
                            ↕ HTTPS/WSS
┌─────────────────────────────────────────────────────────────┐
│                    API Gateway / Load Balancer               │
└─────────────────────────────────────────────────────────────┘
                            ↕
┌─────────────────────────────────────────────────────────────┐
│                   Application Layer                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │ Auth Service │  │Course Service│  │ User Service │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │Video Service │  │Payment Service│  │Quiz Service  │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │Notification  │  │Analytics Svc │  │Schedule Svc  │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└─────────────────────────────────────────────────────────────┘
                            ↕
┌─────────────────────────────────────────────────────────────┐
│                     Data Layer                               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │   Database   │  │   File/Video │  │   Cache      │     │
│  │  (PostgreSQL)│  │   Storage    │  │   (Redis)    │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└─────────────────────────────────────────────────────────────┘
                            ↕
┌─────────────────────────────────────────────────────────────┐
│                  External Services                           │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │Payment Gateway│  │Video Platform│  │Email/SMS API │     │
│  │(PayHere/Stripe)│  │(Zoom/Custom) │  │              │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└─────────────────────────────────────────────────────────────┘
```

### 2.2 Architecture Principles
- **Microservices-oriented**: Modular services for scalability and maintainability
- **API-first design**: RESTful APIs with GraphQL for complex queries
- **Cloud-native**: Containerized deployment (Docker/Kubernetes)
- **Responsive design**: Mobile-first, progressive web app approach
- **Security-first**: End-to-end encryption, OAuth2/JWT authentication
- **Real-time capabilities**: WebSocket for live classes and notifications

---

## 3. User Roles and Permissions

### 3.1 User Roles

| Role | Description | Key Permissions |
|------|-------------|-----------------|
| **Super Admin** | System administrator | Full system access, user management, system configuration |
| **Admin** | Center manager | Course management, enrollment approval, financial reports |
| **Teacher** | Course instructor | Course content creation, grading, student interaction |
| **Student** | Enrolled learner | Course access, assignment submission, exam participation |
| **Parent** | Guardian | View child progress, payment management, communication |
| **Guest** | Visitor | Browse courses, view public content, registration |

### 3.2 User Personas

**Persona 1: Student (Kavinda - Grade 11)**
- Needs: Access recorded lessons, submit assignments, take online exams, join live classes
- Pain points: Internet connectivity issues, finding study materials quickly
- Goals: Prepare for A/L exams, track progress

**Persona 2: Teacher (Ms. Perera - Mathematics Teacher)**
- Needs: Upload course materials, create quizzes, monitor student performance, conduct live classes
- Pain points: Time-consuming manual grading, difficulty tracking multiple classes
- Goals: Efficient course delivery, improved student engagement

**Persona 3: Parent (Mrs. Silva)**
- Needs: Monitor children's progress, manage payments, communicate with teachers
- Pain points: Lack of visibility into child's learning, payment tracking
- Goals: Ensure child's academic success, transparent communication

---

## 4. Core Features and Modules

### 4.1 Public Website (Marketing Site)

#### 4.1.1 Homepage
- **Hero Section**: Eye-catching banner with CTA (Enroll Now, Free Trial)
- **Course Categories**: Visual cards for Primary, Middle, High School, Languages
- **Success Stories**: Student testimonials, results showcase
- **Teacher Profiles**: Featured educators with qualifications
- **Statistics Counter**: Students enrolled, success rate, courses available
- **Blog Section**: Educational articles, tips, news
- **Live Class Schedule**: Upcoming classes preview
- **Pricing Plans**: Transparent fee structure

#### 4.1.2 Course Catalog
- **Filter & Search**: By grade, subject, teacher, mode (online/physical)
- **Course Cards**: Title, description, teacher, duration, price, ratings
- **Course Detail Page**:
  - Comprehensive syllabus
  - Learning outcomes
  - Teacher bio
  - Student reviews
  - Sample lessons
  - Enrollment options (online payment or inquiry)

#### 4.1.3 About & Contact
- **About Us**: Center history, mission, vision
- **Location Map**: Physical center locations (Google Maps integration)
- **Contact Form**: Inquiry submission with auto-response
- **FAQ Section**: Common questions answered

### 4.2 Student Dashboard (Learning Management System)

#### 4.2.1 Dashboard Overview
- **Welcome Screen**: Personalized greeting, progress overview
- **Active Courses**: Quick access to enrolled courses
- **Upcoming Classes**: Schedule for live sessions
- **Pending Assignments**: Due dates and submission status
- **Recent Announcements**: Important updates from teachers/admin
- **Performance Analytics**: Visual charts showing progress

#### 4.2.2 My Courses
- **Course List**: All enrolled courses with progress bars
- **Course Player**:
  - Video player with playback controls
  - Chapter navigation
  - Note-taking feature
  - Bookmarking lessons
  - Download study materials (PDFs, slides)
  - Discussion forum per lesson

#### 4.2.3 Live Classes
- **Join Virtual Classroom**:
  - Integrated video conferencing (Zoom API or custom WebRTC)
  - Screen sharing
  - Interactive whiteboard
  - Chat functionality
  - Raise hand feature
  - Recording access for missed classes
- **Class Schedule**: Calendar view of upcoming live sessions
- **Attendance Tracking**: Automatic attendance marking

#### 4.2.4 Assignments
- **Assignment List**: Filter by subject, due date, status
- **Submission Interface**:
  - File upload (documents, images)
  - Text editor for written answers
  - Submission confirmation
- **Feedback View**: Teacher comments, grades, suggestions

#### 4.2.5 Exams & Quizzes
- **Exam Calendar**: Scheduled assessments
- **Take Exam Interface**:
  - Timer countdown
  - Multiple question types (MCQ, short answer, essay)
  - Auto-save progress
  - Submit and review
- **Results Dashboard**:
  - Score breakdown
  - Correct answers review
  - Performance analytics
  - Percentile ranking

#### 4.2.6 Progress Reports
- **Academic Performance**: Subject-wise grades and trends
- **Attendance Report**: Class participation statistics
- **Time Spent**: Learning hours per subject
- **Downloadable Reports**: PDF generation for printing

#### 4.2.7 Profile & Settings
- **Personal Information**: Edit profile, change password
- **Notification Preferences**: Email, SMS, push notifications
- **Learning Preferences**: Subtitle language, video quality
- **Parent Access**: Share progress with guardian account

### 4.3 Teacher Portal

#### 4.3.1 Teacher Dashboard
- **Overview**: Total students, active courses, pending tasks
- **Quick Actions**: Create assignment, schedule class, grade submissions
- **Student Performance**: Class average, top performers, at-risk students
- **Upcoming Schedule**: Calendar view of classes

#### 4.3.2 Course Management
- **Create/Edit Courses**:
  - Course metadata (title, description, syllabus)
  - Chapter organization
  - Upload video lessons
  - Attach study materials
  - Set prerequisites
- **Content Library**: Reusable content repository
- **Course Publishing**: Draft, preview, publish workflow

#### 4.3.3 Assignment Creation
- **Assignment Builder**:
  - Title, description, instructions
  - Due date and late submission policy
  - File upload requirements
  - Point allocation
  - Rubric creation
- **Bulk Assignment**: Assign to multiple classes

#### 4.3.4 Grading Center
- **Submission Queue**: Pending assignments to grade
- **Grading Interface**:
  - View student submission
  - Inline commenting
  - Score assignment
  - Feedback text
- **Grade Book**: Comprehensive student grades overview
- **Export Grades**: CSV/Excel export

#### 4.3.5 Quiz & Exam Builder
- **Question Bank**: Store reusable questions by topic
- **Create Assessment**:
  - Question types: MCQ, true/false, short answer, essay, fill-in-blank
  - Random question selection
  - Time limits
  - Passing score criteria
  - Auto-grading setup
- **Proctoring Options**: Camera monitoring, tab-switching detection

#### 4.3.6 Live Class Management
- **Schedule Classes**: Date, time, duration, recurring options
- **Virtual Classroom**: Host live sessions with teaching tools
- **Attendance Management**: Mark/edit attendance
- **Recording Management**: Access and share class recordings

#### 4.3.7 Student Analytics
- **Individual Student View**: Detailed performance, attendance, engagement
- **Class Analytics**: Average scores, completion rates, problem areas
- **Export Reports**: Generate custom reports

#### 4.3.8 Communication Tools
- **Announcements**: Post updates to specific classes or all students
- **Messaging**: Direct messaging with students/parents
- **Discussion Forums**: Facilitate class discussions

### 4.4 Admin Panel

#### 4.4.1 Admin Dashboard
- **Key Metrics**:
  - Total students, teachers, courses
  - Revenue statistics
  - Enrollment trends
  - System health status
- **Recent Activities**: Latest enrollments, payments, issues
- **Quick Actions**: Approve enrollments, manage users, system settings

#### 4.4.2 User Management
- **Student Management**:
  - Add/edit/deactivate students
  - Bulk import (CSV)
  - View enrollments and payments
  - Password reset
- **Teacher Management**:
  - Onboard teachers
  - Assign courses
  - Performance tracking
  - Payroll integration
- **Parent Accounts**: Link parents to students
- **Role Management**: Assign and modify permissions

#### 4.4.3 Course Management
- **Course Approval**: Review and publish teacher-created courses
- **Course Catalog**: Overview of all courses, status
- **Category Management**: Create/edit grade levels, subjects
- **Pricing Management**: Set course fees, discounts, bundles

#### 4.4.4 Enrollment Management
- **Manual Enrollment**: Enroll students in courses
- **Enrollment Requests**: Approve/reject online requests
- **Bulk Enrollment**: Batch operations
- **Waitlist Management**: Handle course capacity

#### 4.4.5 Payment & Financial Management
- **Payment Gateway Configuration**: Setup PayHere, Stripe, bank transfer
- **Transaction History**: All payment records
- **Revenue Reports**: Daily, monthly, yearly analytics
- **Invoice Generation**: Automatic receipt creation
- **Payment Reminders**: Auto-notification for pending payments
- **Refund Management**: Process refund requests
- **Discount Codes**: Create promotional offers

#### 4.4.6 Content Management (CMS)
- **Page Editor**: Edit homepage, about, contact pages
- **Blog Management**: Create/edit articles
- **Media Library**: Manage images, videos, documents
- **SEO Settings**: Meta tags, keywords per page

#### 4.4.7 Communication Center
- **Email Campaigns**: Bulk email to segments (students, teachers, leads)
- **SMS Gateway**: Send SMS notifications
- **Push Notifications**: App notifications
- **Template Management**: Email/SMS templates

#### 4.4.8 Reports & Analytics
- **Student Analytics**: Enrollment trends, completion rates, demographics
- **Financial Reports**: Revenue, expenses, profit margins
- **Course Performance**: Popular courses, ratings, feedback
- **Teacher Performance**: Student satisfaction, course completions
- **System Usage**: Peak hours, bandwidth usage, errors
- **Custom Reports**: Build reports with filters and exports

#### 4.4.9 System Settings
- **General Settings**: Site name, logo, contact info, time zone
- **Email Configuration**: SMTP settings, sender details
- **Payment Settings**: Gateway credentials, currency
- **Notification Settings**: Enable/disable notification types
- **Security Settings**: Password policies, session timeout
- **Backup & Restore**: Database backup management
- **API Management**: API keys, rate limiting

### 4.5 Additional Features

#### 4.5.1 Mobile Application
- **Native Apps**: iOS and Android apps (React Native/Flutter)
- **Feature Parity**: All web features available on mobile
- **Offline Mode**: Download courses for offline viewing
- **Push Notifications**: Real-time alerts

#### 4.5.2 Parent Portal
- **Child Progress Dashboard**: View multiple children
- **Payment Management**: Pay fees, view invoices
- **Teacher Communication**: Direct messaging
- **Attendance Alerts**: Notifications for absences

#### 4.5.3 Discussion Forums
- **Subject-wise Forums**: Community discussions
- **Q&A Section**: Peer-to-peer help
- **Teacher Moderation**: Monitor and guide discussions

#### 4.5.4 Gamification
- **Points System**: Earn points for completing lessons, assignments
- **Badges & Achievements**: Unlock rewards for milestones
- **Leaderboards**: Class and global rankings
- **Certificates**: Digital certificates upon course completion

#### 4.5.5 Barcode-Based Attendance System

**Overview:**
A modern, contactless attendance tracking system using QR codes and barcodes for both physical and online classes.

**Features:**

**Student ID Cards:**
- **Unique Barcode/QR Code**: Each student gets a unique barcode linked to their student ID
- **Digital Card**: Downloadable digital student ID card with QR code
- **Physical Card**: Printable student ID cards with barcode
- **Barcode Format**: Code 128 or QR Code with encrypted student ID

**Physical Class Attendance:**
- **Scanner Setup**: Barcode scanners at classroom entry points
- **Mobile App Scanning**: Teachers can scan using mobile app camera
- **Quick Check-in**: Students scan ID card at class entry
- **Auto-timestamp**: Automatic attendance marking with exact time
- **Late Detection**: Flag late arrivals based on class start time
- **Exit Scanning (Optional)**: Track class exit for duration calculation

**Online Class Attendance:**
- **QR Code Display**: Teacher generates unique QR code for each live session
- **Student Scan**: Students scan the displayed QR code to mark attendance
- **Time-limited Codes**: QR codes expire after class time
- **Location Verification (Optional)**: GPS-based verification for hybrid classes
- **Screen Capture Prevention**: QR codes rotate every 5-10 minutes

**Admin/Teacher Interface:**
- **Generate Student Barcodes**: Bulk generation of student ID barcodes
- **Print ID Cards**: Print-ready student ID card templates
- **Real-time Dashboard**: Live view of who's checked in
- **Attendance Reports**: Daily, weekly, monthly attendance summaries
- **Export Data**: CSV/Excel export of attendance records
- **Anomaly Detection**: Flag duplicate scans, suspicious patterns

**Parent Portal:**
- **Real-time Notifications**: SMS/email when child checks in/out
- **Attendance History**: View child's attendance records
- **Absence Alerts**: Automatic notification if child misses class

**Mobile App Features:**
- **Digital Wallet**: Store student ID in mobile app
- **Quick Scan**: One-tap QR code display for scanning
- **Attendance History**: View personal attendance records
- **Offline Mode**: Cache attendance, sync when online

**Hardware Requirements:**
- **Barcode Scanners**: USB barcode scanners for physical locations
- **Tablet/iPad Stands**: Mounted devices at entry points
- **Printer**: For printing physical student ID cards

**Security Features:**
- **Encrypted Barcodes**: Student IDs encrypted in QR codes
- **Anti-spoofing**: Prevent screenshot sharing of QR codes
- **Rate Limiting**: Prevent rapid multiple scans
- **Audit Logs**: Track all attendance modifications

**Technical Implementation:**
- **QR Code Generation**: Library like `qrcode.js` or `node-qrcode`
- **Barcode Generation**: `JsBarcode` or `bwip-js`
- **Mobile Scanning**: React Native Camera or ML Kit
- **Database**: Real-time attendance logging
- **API Endpoints**: POST /attendance/checkin, GET /attendance/reports

#### 4.5.6 Integration Features
- **Calendar Sync**: Google Calendar, Apple Calendar integration
- **Google Classroom**: Import/export courses
- **Zoom Integration**: Seamless live class hosting
- **Payment Gateways**: PayHere (Sri Lanka), Stripe (international)
- **SMS Gateway**: Dialog, Mobitel for notifications
- **Email Service**: SendGrid, AWS SES

---

## 5. Technical Stack Recommendation

### 5.1 Frontend

**Web Application:**
- **Framework**: Next.js 15 (React 19)
- **UI Library**: Tailwind CSS + shadcn/ui components
- **State Management**: Zustand or Redux Toolkit
- **Form Handling**: React Hook Form + Zod validation
- **API Client**: TanStack Query (React Query)
- **Video Player**: Video.js or Plyr
- **WebRTC**: SimpleWebRTC or Daily.co for live classes
- **Charts**: Recharts or Chart.js
- **Animations**: Framer Motion

**Mobile Application:**
- **Framework**: React Native (Expo) or Flutter
- **UI**: Native Base or Flutter Material
- **Barcode/QR Scanner**: React Native Camera, expo-barcode-scanner, or ML Kit
- **QR Code Display**: react-native-qrcode-svg

### 5.2 Backend

**Application Server:**
- **Framework**: Node.js with Express.js or Nest.js (TypeScript)
- **Alternative**: Django (Python) or Spring Boot (Java)
- **API Style**: RESTful + GraphQL (Apollo Server)
- **Authentication**: JWT + OAuth2 (Google, Facebook login)
- **Real-time**: Socket.io or WebSockets
- **File Upload**: Multer with cloud storage
- **Barcode/QR Generation**: `qrcode`, `jsbarcode`, `bwip-js` (Node.js libraries)
- **Barcode Reading**: `@zxing/library` or `quagga2` for web-based scanning

**Microservices (Optional for scale):**
- **API Gateway**: Kong or AWS API Gateway
- **Service Mesh**: Istio (for Kubernetes)

### 5.3 Database

**Primary Database:**
- **Relational**: PostgreSQL 15+ (student, course, enrollment data)

**Caching:**
- **Cache Layer**: Redis (session management, frequently accessed data)

**Search Engine:**
- **Full-text Search**: Elasticsearch or Meilisearch (course search)

**File Storage:**
- **Cloud Storage**: AWS S3, Cloudinary (videos, images, documents)
- **CDN**: CloudFlare or AWS CloudFront

### 5.4 Video & Streaming

**Live Classes:**
- **Option 1**: Zoom API integration (easiest)
- **Option 2**: Agora.io (custom video solution)
- **Option 3**: WebRTC + Jitsi Meet (self-hosted)

**Recorded Videos:**
- **Hosting**: AWS S3 + CloudFront or Vimeo/Wistia
- **Encoding**: AWS MediaConvert or FFmpeg
- **Adaptive Streaming**: HLS or DASH

### 5.5 Infrastructure

**Hosting:**
- **Cloud Provider**: AWS, Google Cloud, or DigitalOcean
- **Deployment**: Docker containers + Kubernetes or AWS ECS
- **CI/CD**: GitHub Actions, GitLab CI, or Jenkins
- **Monitoring**: Datadog, New Relic, or Prometheus + Grafana
- **Logging**: ELK Stack (Elasticsearch, Logstash, Kibana)

**Domain & SSL:**
- **Domain**: achieverslearningcenter.lk
- **SSL**: Let's Encrypt or Cloudflare SSL

### 5.6 Third-Party Integrations

**Payment:**
- **Local**: PayHere (Sri Lanka)
- **International**: Stripe, PayPal

**Communication:**
- **Email**: SendGrid, AWS SES, or Mailgun
- **SMS**: Dialog SMS API, Twilio

**Analytics:**
- **Web Analytics**: Google Analytics 4, Mixpanel
- **Heatmaps**: Hotjar

**Security:**
- **WAF**: Cloudflare, AWS WAF
- **DDoS Protection**: Cloudflare
- **Vulnerability Scanning**: Snyk, OWASP ZAP

---

## 6. Database Schema (Key Entities)

### 6.1 Core Tables

```
users
- id (PK)
- email (unique)
- password_hash
- role (admin, teacher, student, parent)
- first_name
- last_name
- phone
- date_of_birth
- address
- profile_image
- status (active, inactive, suspended)
- created_at
- updated_at

students
- id (PK)
- user_id (FK to users)
- grade_level
- parent_id (FK to users)
- enrollment_date
- student_id_number (unique)

teachers
- id (PK)
- user_id (FK to users)
- qualifications
- subjects
- bio
- experience_years
- rating
- hourly_rate

courses
- id (PK)
- title
- slug (unique)
- description
- grade_level
- subject
- teacher_id (FK to teachers)
- course_type (physical, online_live, recorded, hybrid)
- language (english, sinhala, tamil)
- duration_weeks
- price
- thumbnail_url
- syllabus
- prerequisites
- status (draft, published, archived)
- enrollment_limit
- created_at
- updated_at

course_modules
- id (PK)
- course_id (FK to courses)
- title
- description
- order_index
- created_at

lessons
- id (PK)
- module_id (FK to course_modules)
- title
- content_type (video, article, quiz)
- video_url
- duration_minutes
- order_index
- is_free_preview
- created_at

enrollments
- id (PK)
- student_id (FK to students)
- course_id (FK to courses)
- enrollment_date
- status (pending, active, completed, cancelled)
- payment_status (unpaid, partial, paid)
- completion_percentage
- grade
- certificate_issued

payments
- id (PK)
- user_id (FK to users)
- enrollment_id (FK to enrollments)
- amount
- currency
- payment_method (online, bank_transfer, cash)
- payment_gateway_id
- transaction_id
- status (pending, completed, failed, refunded)
- created_at

assignments
- id (PK)
- course_id (FK to courses)
- teacher_id (FK to teachers)
- title
- description
- due_date
- max_points
- created_at

assignment_submissions
- id (PK)
- assignment_id (FK to assignments)
- student_id (FK to students)
- submission_text
- file_urls (JSON)
- submitted_at
- grade
- feedback
- graded_at

quizzes
- id (PK)
- course_id (FK to courses)
- lesson_id (FK to lessons, nullable)
- title
- duration_minutes
- passing_score
- max_attempts
- created_at

questions
- id (PK)
- quiz_id (FK to quizzes)
- question_text
- question_type (mcq, true_false, short_answer, essay)
- options (JSON)
- correct_answer
- points
- order_index

quiz_attempts
- id (PK)
- quiz_id (FK to quizzes)
- student_id (FK to students)
- score
- total_points
- passed (boolean)
- started_at
- completed_at

live_classes
- id (PK)
- course_id (FK to courses)
- teacher_id (FK to teachers)
- title
- scheduled_at
- duration_minutes
- meeting_url (Zoom link)
- meeting_id
- password
- recording_url
- status (scheduled, ongoing, completed, cancelled)

attendance
- id (PK)
- live_class_id (FK to live_classes)
- student_id (FK to students)
- status (present, absent, late)
- attendance_method (manual, barcode_scan, qr_scan, auto_online)
- check_in_time
- check_out_time
- location_lat (for geo-verification)
- location_lng (for geo-verification)
- device_info (scanner ID or mobile device)
- created_at

student_barcodes
- id (PK)
- student_id (FK to students)
- barcode_data (encrypted unique identifier)
- barcode_image_url
- qr_code_image_url
- issued_at
- expires_at (optional)
- status (active, expired, revoked)

attendance_sessions
- id (PK)
- class_id (FK to live_classes or course_id)
- session_qr_code (dynamic QR for online classes)
- qr_generated_at
- qr_expires_at
- location_required (boolean)
- allowed_radius_meters (for geo-fencing)
- created_at

attendance_logs
- id (PK)
- student_id (FK to students)
- attendance_id (FK to attendance)
- action (check_in, check_out, scan_attempt)
- timestamp
- success (boolean)
- failure_reason (duplicate, expired, invalid)
- ip_address
- device_id

notifications
- id (PK)
- user_id (FK to users)
- title
- message
- type (info, warning, success, error)
- is_read
- created_at

announcements
- id (PK)
- author_id (FK to users)
- course_id (FK to courses, nullable)
- title
- content
- target_audience (all, students, teachers)
- created_at

messages
- id (PK)
- sender_id (FK to users)
- receiver_id (FK to users)
- subject
- message
- is_read
- created_at

certificates
- id (PK)
- student_id (FK to students)
- course_id (FK to courses)
- certificate_url
- issued_at

progress_tracking
- id (PK)
- student_id (FK to students)
- lesson_id (FK to lessons)
- status (not_started, in_progress, completed)
- time_spent_minutes
- last_accessed_at
- completed_at
```

---

## 7. Security & Compliance

### 7.1 Security Measures

**Authentication & Authorization:**
- JWT-based authentication with refresh tokens
- Role-based access control (RBAC)
- Multi-factor authentication (2FA) for admin accounts
- OAuth2 integration (Google, Facebook login)
- Password policies: minimum 8 characters, complexity requirements
- Account lockout after failed login attempts

**Data Protection:**
- Encryption at rest (AES-256)
- Encryption in transit (TLS 1.3)
- Database field-level encryption for sensitive data (PII)
- Regular security audits
- Secure file upload validation (file type, size, malware scanning)

**Application Security:**
- Input validation and sanitization
- SQL injection prevention (parameterized queries)
- XSS protection (Content Security Policy)
- CSRF tokens for state-changing operations
- Rate limiting on APIs
- DDoS protection (Cloudflare)
- Regular dependency updates and vulnerability scanning

**Privacy & Compliance:**
- GDPR-compliant data handling (if serving EU users)
- Privacy policy and terms of service
- Cookie consent management
- Data retention policies
- Right to erasure (delete account functionality)
- Data export functionality

### 7.2 Backup & Disaster Recovery

- **Database Backups**: Daily automated backups with 30-day retention
- **Incremental Backups**: Hourly transaction logs
- **Off-site Storage**: Backups stored in separate region
- **Recovery Testing**: Monthly DR drills
- **RTO**: 4 hours (Recovery Time Objective)
- **RPO**: 1 hour (Recovery Point Objective)

---

## 8. UI/UX Design Principles

### 8.1 Design Philosophy

**Modern & Attractive:**
- Clean, minimalist interface with plenty of white space
- Vibrant color scheme: Primary (Blue), Secondary (Orange/Yellow), Accent (Green for success)
- Consistent typography: Modern sans-serif fonts (Inter, Poppins)
- High-quality imagery and illustrations
- Subtle animations and transitions

**User-Centric:**
- Intuitive navigation with breadcrumbs
- Quick access to frequently used features
- Contextual help and tooltips
- Progressive disclosure (don't overwhelm users)
- Accessibility: WCAG 2.1 AA compliance

**Responsive Design:**
- Mobile-first approach
- Breakpoints: Mobile (<768px), Tablet (768-1024px), Desktop (>1024px)
- Touch-friendly UI elements
- Adaptive layouts

### 8.2 Key UI Components

**Navigation:**
- **Top Navigation**: Logo, main menu, user profile dropdown, notifications
- **Sidebar**: Dashboard quick links (collapsible on mobile)
- **Breadcrumbs**: Current page hierarchy

**Dashboard Widgets:**
- **Cards**: Course cards, stat cards with icons
- **Progress Bars**: Visual completion tracking
- **Charts**: Line charts (progress over time), pie charts (subject distribution)
- **Calendar**: Interactive schedule view

**Course Player:**
- **Video Player**: Custom controls, playback speed, quality selector
- **Side Panel**: Chapter navigation, notes, resources
- **Bottom Bar**: Next lesson, previous lesson buttons

**Forms:**
- **Inline Validation**: Real-time error feedback
- **Clear Labels**: Descriptive form fields
- **Help Text**: Guidance for complex fields
- **Multi-step Forms**: Progress indicator for enrollments

### 8.3 Color Scheme (Example)

```
Primary: #2563EB (Blue) - CTA buttons, links, active states
Secondary: #F59E0B (Amber) - Highlights, badges, warnings
Success: #10B981 (Green) - Completed tasks, success messages
Error: #EF4444 (Red) - Errors, delete actions
Neutral: #6B7280 (Gray) - Text, borders
Background: #F9FAFB (Light Gray) - Page backgrounds
```

---

## 9. Non-Functional Requirements

### 9.1 Performance

- **Page Load Time**: < 2 seconds for initial load
- **Video Buffering**: < 1 second start time
- **API Response Time**: < 200ms for 95% of requests
- **Concurrent Users**: Support 1000+ simultaneous users
- **Database Queries**: Optimized with indexing, < 100ms average

### 9.2 Scalability

- **Horizontal Scaling**: Add more application servers as needed
- **Database Scaling**: Read replicas for read-heavy operations
- **CDN**: Distribute static assets globally
- **Load Balancing**: Distribute traffic across servers
- **Auto-scaling**: Automatic scaling based on traffic

### 9.3 Availability

- **Uptime SLA**: 99.9% (< 9 hours downtime per year)
- **Monitoring**: 24/7 system monitoring with alerts
- **Failover**: Automatic failover to backup systems
- **Maintenance Windows**: Scheduled during low-traffic hours

### 9.4 Usability

- **Onboarding**: Interactive tutorials for new users
- **Help Documentation**: Comprehensive user guides
- **Multi-language Support**: English, Sinhala, Tamil
- **Accessibility**: Screen reader support, keyboard navigation

---

## 10. Development Phases

### Phase 1: MVP (Minimum Viable Product) - 8-12 weeks

**Core Features:**
- Public website with course catalog
- User registration and authentication
- Student dashboard with basic course viewing
- Teacher portal for content upload
- Admin panel for user and course management
- Basic enrollment and payment (manual processing)

**Deliverables:**
- Functional website and dashboards
- Database setup
- Basic hosting infrastructure

### Phase 2: Enhanced Features - 6-8 weeks

**Additional Features:**
- Online payment integration (PayHere, Stripe)
- Quiz and assignment system
- Live class scheduling (Zoom integration)
- Progress tracking and analytics
- Email and SMS notifications
- Mobile-responsive enhancements
- **Barcode-based attendance system** (QR code generation, scanning, real-time tracking)

**Deliverables:**
- Complete LMS functionality
- Payment gateway integration
- Notification system
- Attendance tracking with barcode/QR code system

### Phase 3: Advanced Features - 6-8 weeks

**Advanced Capabilities:**
- Mobile applications (iOS & Android)
- Advanced analytics and reporting
- Gamification (points, badges, leaderboards)
- Discussion forums
- Parent portal
- Advanced video features (adaptive streaming)

**Deliverables:**
- Native mobile apps
- Comprehensive analytics
- Community features

### Phase 4: Optimization & Scaling - 4-6 weeks

**Enhancements:**
- Performance optimization
- SEO improvements
- Marketing automation
- A/B testing implementation
- Advanced security features
- Load testing and scaling

**Deliverables:**
- Optimized, production-ready platform
- Comprehensive documentation
- Training materials

---

## 11. Project Estimates

### 11.1 Team Composition

**Core Team:**
- Project Manager: 1
- UI/UX Designer: 1-2
- Frontend Developers: 2-3
- Backend Developers: 2-3
- Mobile Developers: 1-2 (Phase 3)
- DevOps Engineer: 1
- QA Engineer: 1-2
- Content Writer: 1 (part-time)

### 11.2 Timeline

- **Phase 1 (MVP)**: 8-12 weeks
- **Phase 2 (Enhanced)**: 6-8 weeks
- **Phase 3 (Advanced)**: 6-8 weeks
- **Phase 4 (Optimization)**: 4-6 weeks
- **Total**: 24-34 weeks (6-8 months)

### 11.3 Infrastructure Costs (Monthly Estimates)

**Software & Services:**
- **Cloud Hosting** (AWS/GCP): $200-500
- **Database**: $100-200
- **CDN & Storage**: $50-150
- **Video Hosting/Streaming**: $100-300
- **Email/SMS Services**: $50-100
- **Monitoring & Security**: $50-100
- **Payment Gateway Fees**: 2-3% per transaction
- **Total Monthly**: $550-1,350 + transaction fees

**Hardware (One-time Costs):**
- **Barcode Scanners**: $50-150 per scanner × number of classrooms
- **Tablets/iPads for Scanning**: $200-400 per device (optional)
- **Student ID Card Printer**: $300-800 (one-time)
- **ID Card Materials**: $0.50-1 per card
- **Estimated Initial Hardware**: $1,000-3,000 (depending on number of locations)

---

## 12. Risks & Mitigation

### 12.1 Technical Risks

| Risk | Impact | Mitigation Strategy |
|------|--------|---------------------|
| Video streaming scalability | High | Use CDN, adaptive bitrate streaming, third-party platforms |
| Payment gateway integration | Medium | Test thoroughly in sandbox, have backup gateway |
| Data security breach | High | Regular audits, encryption, security best practices |
| System downtime | High | Load balancing, auto-scaling, monitoring, backups |
| Poor user adoption | Medium | User testing, feedback loops, training materials |

### 12.2 Business Risks

| Risk | Impact | Mitigation Strategy |
|------|--------|---------------------|
| Competition from established players | Medium | Differentiate with superior UX, local focus |
| Low initial enrollment | Medium | Marketing campaign, free trials, referral programs |
| Teacher resistance to platform | Medium | Comprehensive training, support, teacher feedback |
| Cash flow issues | High | Phase payments, flexible pricing, multiple revenue streams |

---

## 13. Success Metrics (KPIs)

### 13.1 Business Metrics

- **Student Enrollment**: Target 500+ students in first 6 months
- **Course Completion Rate**: > 70%
- **Student Retention**: > 80% semester-to-semester
- **Revenue Growth**: 20% month-over-month
- **Net Promoter Score (NPS)**: > 50

### 13.2 Technical Metrics

- **System Uptime**: > 99.9%
- **Page Load Time**: < 2 seconds
- **API Response Time**: < 200ms
- **Error Rate**: < 0.1%
- **Mobile App Rating**: > 4.5 stars

### 13.3 User Engagement Metrics

- **Daily Active Users**: Track DAU/MAU ratio
- **Average Session Duration**: > 20 minutes
- **Course Completion Rate**: > 70%
- **Assignment Submission Rate**: > 85%
- **Live Class Attendance**: > 80%

---

## 14. Future Enhancements (Post-Launch)

### 14.1 AI & Machine Learning

- **Personalized Learning Paths**: AI-recommended courses based on performance
- **Intelligent Tutoring**: Chatbot for instant doubt resolution
- **Automated Grading**: AI-powered essay grading
- **Predictive Analytics**: Identify at-risk students early

### 14.2 Advanced Features

- **Virtual Reality Classes**: Immersive learning experiences
- **Peer-to-Peer Learning**: Study groups, collaborative projects
- **Marketplace**: Allow external teachers to create and sell courses
- **Scholarship Portal**: Application and management system
- **Alumni Network**: Connect graduates, job board

### 14.3 Geographic Expansion

- **Multi-branch Support**: Manage multiple physical locations
- **Franchise Management**: Enable franchise operations
- **International Courses**: Partner with global educators
- **Multi-currency**: Support international payments

---

## 15. Technical Documentation Requirements

### 15.1 Documentation Deliverables

- **API Documentation**: OpenAPI/Swagger specs
- **Database Schema**: ER diagrams, data dictionary
- **Deployment Guide**: Step-by-step deployment instructions
- **Admin Manual**: System administration guide
- **User Manuals**: Guides for students, teachers, parents
- **Developer Onboarding**: Setup guide for new developers
- **Testing Documentation**: Test plans, test cases

### 15.2 Code Standards

- **Naming Conventions**: Consistent variable, function naming
- **Code Comments**: Inline documentation for complex logic
- **Version Control**: Git workflow (feature branches, PRs)
- **Code Reviews**: Mandatory peer reviews before merge
- **Linting**: ESLint, Prettier for code consistency

---

## 16. Quality Assurance

### 16.1 Testing Strategy

**Unit Testing:**
- Test individual functions and components
- Target: > 80% code coverage

**Integration Testing:**
- Test API endpoints, database interactions
- Test third-party integrations (payments, video)

**End-to-End Testing:**
- Simulate user workflows (enrollment, course completion)
- Tools: Cypress, Playwright

**Performance Testing:**
- Load testing with 1000+ concurrent users
- Tools: JMeter, LoadRunner

**Security Testing:**
- Penetration testing
- Vulnerability scanning
- OWASP compliance

**User Acceptance Testing (UAT):**
- Beta testing with real students and teachers
- Gather feedback and iterate

### 16.2 Testing Environments

- **Development**: For active development
- **Staging**: Mirror of production for testing
- **Production**: Live environment

---

## 17. Conclusion

This High-Level Design document outlines a comprehensive, modern, and scalable education platform for Achievers Learning Center. The platform is designed to:

✅ Support multiple learning modes (physical, online live, recorded, hybrid)
✅ Serve students from Grade 1-13 plus language courses
✅ Provide robust teacher and admin tools
✅ Enable flexible enrollment and payment options
✅ Scale to thousands of users
✅ Deliver an attractive, user-friendly experience

**Next Steps:**
1. Review and approve this HLD
2. Create detailed technical specifications
3. Design UI/UX mockups and prototypes
4. Set up development environment
5. Begin Phase 1 development (MVP)

**Questions or Clarifications:**
Please review this document and provide feedback. Areas that may need further discussion:
- Specific video platform preference (Zoom vs custom solution)
- Budget allocation for infrastructure
- Launch timeline and priority features
- Marketing and go-to-market strategy

---

**Document Control:**
- **Version**: 1.0
- **Last Updated**: February 10, 2026
- **Status**: Draft - Awaiting Approval
- **Next Review**: Upon stakeholder feedback

---

*This document is confidential and intended for internal use by Achievers Learning Center.*
