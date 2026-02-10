from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    """Custom user manager for email-based authentication"""

    def create_user(self, email, password=None, **extra_fields):
        """Create and return a regular user with email"""
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        # Set username to email if not provided
        extra_fields.setdefault('username', email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Create and return a superuser with email"""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('role', 'super_admin')

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    """Extended user model with additional fields and role-based access"""

    ROLE_CHOICES = [
        ('super_admin', 'Super Admin'),
        ('admin', 'Admin'),
        ('teacher', 'Teacher'),
        ('student', 'Student'),
        ('parent', 'Parent'),
        ('guest', 'Guest'),
    ]

    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('suspended', 'Suspended'),
    ]

    # Override email to be unique and required
    email = models.EmailField(_('email address'), unique=True)

    # Additional fields
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')
    phone = models.CharField(max_length=15, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    address = models.TextField(blank=True)
    profile_image = models.ImageField(upload_to='profiles/', null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Use email as username
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    # Use custom manager
    objects = UserManager()

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return f"{self.get_full_name()} ({self.role})"

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}".strip() or self.email

    @property
    def is_student(self):
        return self.role == 'student'

    @property
    def is_teacher(self):
        return self.role == 'teacher'

    @property
    def is_parent_user(self):
        return self.role == 'parent'

    @property
    def is_admin_user(self):
        return self.role in ['admin', 'super_admin']


class Student(models.Model):
    """Student profile model"""

    GRADE_CHOICES = [
        ('grade_1', 'Grade 1'),
        ('grade_2', 'Grade 2'),
        ('grade_3', 'Grade 3'),
        ('grade_4', 'Grade 4'),
        ('grade_5', 'Grade 5'),
        ('grade_6', 'Grade 6'),
        ('grade_7', 'Grade 7'),
        ('grade_8', 'Grade 8'),
        ('grade_9', 'Grade 9'),
        ('grade_10', 'Grade 10'),
        ('grade_11', 'Grade 11'),
        ('grade_12', 'Grade 12'),
        ('grade_13', 'Grade 13'),
        ('language', 'Language Course'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    grade_level = models.CharField(max_length=15, choices=GRADE_CHOICES)
    parent = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='children',
        limit_choices_to={'role': 'parent'}
    )
    enrollment_date = models.DateField(auto_now_add=True)
    student_id_number = models.CharField(max_length=20, unique=True)

    class Meta:
        verbose_name = 'Student'
        verbose_name_plural = 'Students'

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.student_id_number}"

    def save(self, *args, **kwargs):
        # Auto-generate student ID if not provided
        if not self.student_id_number:
            # Generate ID like: STU2026001, STU2026002, etc.
            from datetime import datetime
            year = datetime.now().year
            last_student = Student.objects.filter(
                student_id_number__startswith=f'STU{year}'
            ).order_by('-student_id_number').first()

            if last_student:
                last_number = int(last_student.student_id_number[-3:])
                new_number = last_number + 1
            else:
                new_number = 1

            self.student_id_number = f'STU{year}{new_number:03d}'

        super().save(*args, **kwargs)


class Teacher(models.Model):
    """Teacher profile model"""

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='teacher_profile')
    qualifications = models.TextField(help_text="Educational qualifications and certifications")
    subjects = models.JSONField(default=list, help_text="List of subjects taught")
    bio = models.TextField(blank=True, help_text="Short biography")
    experience_years = models.IntegerField(default=0, help_text="Years of teaching experience")
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00, help_text="Teacher rating (0-5)")
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, help_text="Hourly rate in LKR")

    is_verified = models.BooleanField(default=False, help_text="Whether teacher is verified by admin")
    joined_date = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = 'Teacher'
        verbose_name_plural = 'Teachers'

    def __str__(self):
        return f"Teacher: {self.user.get_full_name()}"

    @property
    def subject_list(self):
        """Return comma-separated list of subjects"""
        return ", ".join(self.subjects) if self.subjects else "No subjects"


class Parent(models.Model):
    """Parent profile model"""

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='parent_profile')
    occupation = models.CharField(max_length=100, blank=True)
    emergency_contact = models.CharField(max_length=15, blank=True)

    class Meta:
        verbose_name = 'Parent'
        verbose_name_plural = 'Parents'

    def __str__(self):
        return f"Parent: {self.user.get_full_name()}"

    @property
    def children_count(self):
        """Return number of children"""
        return self.user.children.count()

    def get_children(self):
        """Return queryset of children"""
        return self.user.children.all()
