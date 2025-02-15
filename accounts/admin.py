from django.contrib import admin
from .models import UserProfile

# Register your models here.

class UserProfileAdmin(admin.ModelAdmin):
    # Correct way to display related user fields
    list_display = ('user', 'get_first_name', 'get_last_name', 'get_email', 'mobile_number', 'dob', 'gender', )

    # Add search fields & filters
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'user__email', 'mobile_number')
    list_filter = ('gender', 'dob')

    # Methods to fetch related User fields
    def get_first_name(self, obj):
        return obj.user.first_name  # Assuming User model has 'first_name'
    get_first_name.short_description = 'First Name'  # Set column name

    def get_last_name(self, obj):
        return obj.user.last_name  # Assuming User model has 'last_name'
    get_last_name.short_description = 'Last Name'

    def get_email(self, obj):
        return obj.user.email  # Assuming User model has 'email'
    get_email.short_description = 'Email'

admin.site.register(UserProfile, UserProfileAdmin)
