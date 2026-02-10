from django.db import models
from django.utils.text import slugify
from apps.users.models import Teacher, Student


class Course(models.Model):
    """Course model"""

    COURSE_TYPE_CHOICES = [
        ('physical', 'Physical'),
        ('online_live', 'Online Live'),
        ('recorded', 'Recorded'),
        ('hybrid', 'Hybrid'),
    ]

    LANGUAGE_CHOICES = [
        ('english', 'English'),
        ('sinhala', 'Sinhala'),
        ('tamil', 'Tamil'),
    ]

    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('archived', 'Archived'),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()
    grade_level = models.CharField(max_length=15)
    subject = models.CharField(max_length=100)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='courses')
    course_type = models.CharField(max_length=20, choices=COURSE_TYPE_CHOICES, default='recorded')
    language = models.CharField(max_length=10, choices=LANGUAGE_CHOICES, default='english')
    duration_weeks = models.IntegerField(default=12)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    thumbnail = models.ImageField(upload_to='course_thumbnails/', blank=True, null=True)
    syllabus = models.TextField(blank=True)
    prerequisites = models.TextField(blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    enrollment_limit = models.IntegerField(null=True, blank=True, help_text="Maximum students (leave blank for unlimited)")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Course'
        verbose_name_plural = 'Courses'
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
            # Ensure uniqueness
            original_slug = self.slug
            counter = 1
            while Course.objects.filter(slug=self.slug).exists():
                self.slug = f"{original_slug}-{counter}"
                counter += 1
        super().save(*args, **kwargs)

    @property
    def enrollment_count(self):
        """Return number of enrolled students"""
        return self.enrollments.filter(status='active').count()

    @property
    def is_full(self):
        """Check if course has reached enrollment limit"""
        if self.enrollment_limit:
            return self.enrollment_count >= self.enrollment_limit
        return False


class CourseModule(models.Model):
    """Course module/chapter"""

    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='modules')
    title = models.CharField(max_length=200)
    description = models.TextField()
    order_index = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Course Module'
        verbose_name_plural = 'Course Modules'
        ordering = ['order_index']

    def __str__(self):
        return f"{self.course.title} - Module {self.order_index}: {self.title}"


class Lesson(models.Model):
    """Individual lesson within a module"""

    CONTENT_TYPE_CHOICES = [
        ('video', 'Video'),
        ('article', 'Article'),
        ('quiz', 'Quiz'),
        ('file', 'File/Document'),
    ]

    module = models.ForeignKey(CourseModule, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=200)
    content_type = models.CharField(max_length=10, choices=CONTENT_TYPE_CHOICES, default='video')
    video_url = models.URLField(blank=True, help_text="YouTube or video URL")
    article_content = models.TextField(blank=True, help_text="Article text content")
    file_attachment = models.FileField(upload_to='lesson_files/', blank=True, null=True)
    duration_minutes = models.IntegerField(default=0, help_text="Lesson duration in minutes")
    order_index = models.IntegerField(default=0)
    is_free_preview = models.BooleanField(default=False, help_text="Allow non-enrolled students to view")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Lesson'
        verbose_name_plural = 'Lessons'
        ordering = ['order_index']

    def __str__(self):
        return f"{self.module.course.title} - {self.title}"


class Enrollment(models.Model):
    """Student enrollment in a course"""

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    PAYMENT_STATUS_CHOICES = [
        ('unpaid', 'Unpaid'),
        ('partial', 'Partially Paid'),
        ('paid', 'Paid'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    enrollment_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    payment_status = models.CharField(max_length=10, choices=PAYMENT_STATUS_CHOICES, default='unpaid')
    completion_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    grade = models.CharField(max_length=5, blank=True, help_text="Final grade (A, B, C, etc.)")

    class Meta:
        verbose_name = 'Enrollment'
        verbose_name_plural = 'Enrollments'
        unique_together = ['student', 'course']
        ordering = ['-enrollment_date']

    def __str__(self):
        return f"{self.student.user.get_full_name()} enrolled in {self.course.title}"


class LessonProgress(models.Model):
    """Track student progress for each lesson"""

    STATUS_CHOICES = [
        ('not_started', 'Not Started'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]

    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE, related_name='lesson_progress')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='not_started')
    time_spent_minutes = models.IntegerField(default=0)
    last_accessed_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = 'Lesson Progress'
        verbose_name_plural = 'Lesson Progress'
        unique_together = ['enrollment', 'lesson']

    def __str__(self):
        return f"{self.enrollment.student.user.get_full_name()} - {self.lesson.title}: {self.status}"
