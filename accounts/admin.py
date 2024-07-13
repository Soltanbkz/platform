from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Student, Parent

class UserAdmin(BaseUserAdmin):
    list_display = [
        "get_full_name",
        "username",
        "email",
        "is_active",
        "is_student",
        "is_lecturer",
        "is_parent",
        "is_staff",
    ]
    search_fields = [
        "username",
        "first_name",
        "last_name",
        "email",
        "is_active",
        "is_lecturer",
        "is_parent",
        "is_staff",
    ]

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser',
                                    'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
        ('Additional info', {'fields': ('is_student', 'is_lecturer', 'is_parent', 'is_dep_head', 'gender', 'phone', 'address', 'picture')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2'),
        }),
    )
    ordering = ('username',)
    filter_horizontal = ('groups', 'user_permissions',)

    class Meta:
        managed = True
        verbose_name = "User"
        verbose_name_plural = "Users"

admin.site.register(User, UserAdmin)
admin.site.register(Student)
admin.site.register(Parent)
