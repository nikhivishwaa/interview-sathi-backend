from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from accounts.models import User
from accounts.forms import CustomUserCreationForm, CustomUserChangeForm, ProfileEditForm

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = ('email', 'first_name', 'last_name', 
                    'gender', 'phone','verified', 'is_staff')
    list_filter = ('email', 'phone', 'is_staff', 'suspended', 'first_name')
    readonly_fields = ('date_joined', 'last_login','email_verified_at', 'phone_verified_at')
    fieldsets = (
                 (None, {'fields':('email', 'password')}),
                 ('Profile Settings', {'fields': ('profile_pic', 'verified')}),
                 ('Personal info', {'fields': ('first_name', 'last_name','phone',
                                               'dob', 'gender')}),
                 ('Account Activity', {'fields': ('date_joined', 'last_login')}),
                 ('Permissions', {'fields':('is_staff', 'is_active', 'suspended')}))

    add_fieldsets = (
            (
            None, {
            'classes':('wide',), 
            'fields':('email', 'password1', 'password2', 'is_staff', 'is_active')
            }),
            (
            'Personal Information', {
            'classes':('wide',), 
            'fields':('phone', 'first_name', 'last_name', 'dob', 'gender')
            }),
        )

    search_fields = ('email', 'first_name', 'last_name', 'phone', 'gender')

    ordering = ('date_joined',)


admin.site.register(User, CustomUserAdmin)

admin.site.site_title = "Interview Sathi Admin Panel"
admin.site.site_header = "Interview Sathi Administration"
admin.site.index_title = "Administration"
