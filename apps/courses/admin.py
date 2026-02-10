from django.contrib import admin
from .models import Course, CourseModule, Lesson, Enrollment, LessonProgress


class CourseModuleInline(admin.TabularInline):
    model = CourseModule
    extra = 1


class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 1


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'teacher', 'course_type', 'grade_level', 'price', 'status', 'enrollment_count')
    list_filter = ('status', 'course_type', 'grade_level')
    search_fields = ('title', 'description', 'teacher__user__first_name', 'teacher__user__last_name')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [CourseModuleInline]


@admin.register(CourseModule)
class CourseModuleAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'order_index')
    list_filter = ('course',)
    inlines = [LessonInline]


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'module', 'content_type', 'duration_minutes', 'is_free_preview')
    list_filter = ('content_type', 'is_free_preview')


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'status', 'payment_status', 'enrollment_date', 'completion_percentage')
    list_filter = ('status', 'payment_status', 'enrollment_date')
    search_fields = ('student__user__first_name', 'student__user__last_name', 'course__title')


@admin.register(LessonProgress)
class LessonProgressAdmin(admin.ModelAdmin):
    list_display = ('enrollment', 'lesson', 'status', 'time_spent_minutes', 'completed_at')
    list_filter = ('status',)
