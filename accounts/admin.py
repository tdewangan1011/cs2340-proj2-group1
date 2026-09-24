from django.contrib import admin
from .models import Profile

# Register your models here.

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'user__first_name', 'user__last_name','role', 'location', 'profile_public')
    list_filter = ('role', 'profile_public')
    search_fields = ('user__username', 'user__email', 'user__first_name', 'user__last_name')

