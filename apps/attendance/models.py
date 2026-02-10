from django.db import models
from apps.users.models import Student
from apps.courses.models import Course


class StudentBarcode(models.Model):
    """Student barcode/QR code for attendance"""

    STATUS_CHOICES = [
        ('active', 'Active'),
        ('expired', 'Expired'),
        ('revoked', 'Revoked'),
    ]

    student = models.OneToOneField(Student, on_delete=models.CASCADE, related_name='barcode')
    barcode_data = models.CharField(max_length=255, unique=True, help_text="Encrypted student ID")
    barcode_image = models.ImageField(upload_to='student_ids/barcodes/', blank=True)
    qr_code_image = models.ImageField(upload_to='student_ids/qrcodes/', blank=True)
    issued_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')

    class Meta:
        verbose_name = 'Student Barcode'
        verbose_name_plural = 'Student Barcodes'

    def __str__(self):
        return f"Barcode for {self.student.user.get_full_name()}"


class LiveClass(models.Model):
    """Live class session"""

    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='live_classes')
    title = models.CharField(max_length=200)
    scheduled_at = models.DateTimeField()
    duration_minutes = models.IntegerField(default=60)
    meeting_url = models.URLField(blank=True, help_text="Zoom or meeting URL")
    meeting_id = models.CharField(max_length=50, blank=True)
    meeting_password = models.CharField(max_length=50, blank=True)
    recording_url = models.URLField(blank=True)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='scheduled')

    class Meta:
        verbose_name = 'Live Class'
        verbose_name_plural = 'Live Classes'
        ordering = ['-scheduled_at']

    def __str__(self):
        return f"{self.course.title} - {self.title}"


class Attendance(models.Model):
    """Attendance record for live classes"""

    STATUS_CHOICES = [
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('late', 'Late'),
    ]

    METHOD_CHOICES = [
        ('manual', 'Manual'),
        ('barcode_scan', 'Barcode Scan'),
        ('qr_scan', 'QR Scan'),
        ('auto_online', 'Auto Online'),
    ]

    live_class = models.ForeignKey(LiveClass, on_delete=models.CASCADE, related_name='attendances')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='attendances')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='present')
    attendance_method = models.CharField(max_length=15, choices=METHOD_CHOICES, default='manual')
    check_in_time = models.DateTimeField(null=True, blank=True)
    check_out_time = models.DateTimeField(null=True, blank=True)
    location_lat = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    location_lng = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    device_info = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Attendance'
        verbose_name_plural = 'Attendance Records'
        unique_together = ['live_class', 'student']

    def __str__(self):
        return f"{self.student.user.get_full_name()} - {self.live_class.title}: {self.status}"


class AttendanceLog(models.Model):
    """Audit log for attendance actions"""

    ACTION_CHOICES = [
        ('check_in', 'Check In'),
        ('check_out', 'Check Out'),
        ('scan_attempt', 'Scan Attempt'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    attendance = models.ForeignKey(Attendance, on_delete=models.CASCADE, null=True, blank=True)
    action = models.CharField(max_length=15, choices=ACTION_CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)
    success = models.BooleanField()
    failure_reason = models.CharField(max_length=100, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    device_id = models.CharField(max_length=100, blank=True)

    class Meta:
        verbose_name = 'Attendance Log'
        verbose_name_plural = 'Attendance Logs'
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.student.user.get_full_name()} - {self.action} at {self.timestamp}"
