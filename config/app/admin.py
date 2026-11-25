from django.contrib import admin
from .models import UserFile

@admin.register(UserFile)
class UserFileAdmin(admin.ModelAdmin):
    list_display = ['title', 'owner', 'file_type', 'size_display', 'is_public', 'uploaded_at']
    list_filter = ['file_type', 'is_public', 'uploaded_at']
    search_fields = ['title', 'file', 'owner__username']
    readonly_fields = ['size', 'uploaded_at']
    date_hierarchy = 'uploaded_at'
