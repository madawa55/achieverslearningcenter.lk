from django.contrib import admin
from .models import StudentBarcode, LiveClass, Attendance, AttendanceLog


@admin.register(StudentBarcode)
class StudentBarcodeAdmin(admin.ModelAdmin):
    list_display = ('student', 'status', 'issued_at')
    list_filter = ('status', 'issued_at')
    search_fields = ('student__user__first_name', 'student__user__last_name', 'barcode_data')


@admin.register(LiveClass)
class LiveClassAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'scheduled_at', 'duration_minutes', 'status')
    list_filter = ('status', 'scheduled_at')
    search_fields = ('title', 'course__title')


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('student', 'live_class', 'status', 'attendance_method', 'check_in_time')
    list_filter = ('status', 'attendance_method', 'check_in_time')
    search_fields = ('student__user__first_name', 'student__user__last_name', 'live_class__title')


@admin.register(AttendanceLog)
class AttendanceLogAdmin(admin.ModelAdmin):
    list_display = ('student', 'action', 'success', 'timestamp')
    list_filter = ('action', 'success', 'timestamp')
    search_fields = ('student__user__first_name', 'student__user__last_name')
