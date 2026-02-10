from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Student, Teacher, Parent


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'role', 'status', 'is_staff')
    list_filter = ('role', 'status', 'is_staff', 'is_superuser')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('-created_at',)

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'phone', 'date_of_birth', 'address', 'profile_image')}),
        ('Role & Status', {'fields': ('role', 'status')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important Dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'role', 'password1', 'password2'),
        }),
    )


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('student_id_number', 'get_student_name', 'grade_level', 'get_parent_name', 'enrollment_date')
    list_filter = ('grade_level', 'enrollment_date')
    search_fields = ('student_id_number', 'user__first_name', 'user__last_name', 'user__email')
    raw_id_fields = ('user', 'parent')

    def get_student_name(self, obj):
        return obj.user.get_full_name()
    get_student_name.short_description = 'Student Name'

    def get_parent_name(self, obj):
        return obj.parent.get_full_name() if obj.parent else '-'
    get_parent_name.short_description = 'Parent Name'


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('get_teacher_name', 'experience_years', 'rating', 'is_verified', 'joined_date')
    list_filter = ('is_verified', 'joined_date')
    search_fields = ('user__first_name', 'user__last_name', 'user__email', 'subjects')
    raw_id_fields = ('user',)

    fieldsets = (
        ('Teacher Info', {'fields': ('user',)}),
        ('Qualifications', {'fields': ('qualifications', 'subjects', 'experience_years')}),
        ('Profile', {'fields': ('bio', 'rating', 'hourly_rate')}),
        ('Status', {'fields': ('is_verified',)}),
    )

    def get_teacher_name(self, obj):
        return obj.user.get_full_name()
    get_teacher_name.short_description = 'Teacher Name'


@admin.register(Parent)
class ParentAdmin(admin.ModelAdmin):
    list_display = ('get_parent_name', 'occupation', 'children_count', 'emergency_contact')
    search_fields = ('user__first_name', 'user__last_name', 'user__email')
    raw_id_fields = ('user',)

    def get_parent_name(self, obj):
        return obj.user.get_full_name()
    get_parent_name.short_description = 'Parent Name'
