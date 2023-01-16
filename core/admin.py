from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from core.models import *


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """
    Custom User Admin to handle user creation in line with the custom User model.
    """
    model = User
    list_display = ('email', 'company_name', 'is_staff', 'is_active',)
    list_filter = ('email', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('email', 'password', 'company_name', 'address', 'industry',
                           'phone_number', 'user_type', 'website')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email', 'company_name',)
    ordering = ('email',)


admin.site.register(Supplier)
admin.site.register(Contractor)
admin.site.register(Bids)
admin.site.register(Tender)

