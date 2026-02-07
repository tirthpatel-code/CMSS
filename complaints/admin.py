from django.contrib import admin
from .models import Complaint, ComplaintCategory, ComplaintComment, ComplaintHistory


@admin.register(ComplaintCategory)
class ComplaintCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'created_at']
    search_fields = ['name']


@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    list_display = ['ticket_number', 'title', 'status', 'priority', 'created_by', 'assigned_to', 'created_at']
    list_filter = ['status', 'priority', 'category', 'created_at']
    search_fields = ['ticket_number', 'title', 'description']
    readonly_fields = ['ticket_number', 'created_at', 'updated_at']
    fieldsets = (
        ('Basic Information', {
            'fields': ('ticket_number', 'title', 'description', 'category', 'status', 'priority')
        }),
        ('User Information', {
            'fields': ('created_by', 'assigned_to', 'contact_email', 'contact_phone', 'location')
        }),
        ('Resolution', {
            'fields': ('resolution_notes', 'resolved_at')
        }),
        ('Attachments', {
            'fields': ('attachment',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )


@admin.register(ComplaintComment)
class ComplaintCommentAdmin(admin.ModelAdmin):
    list_display = ['complaint', 'user', 'created_at', 'is_internal']
    list_filter = ['is_internal', 'created_at']
    search_fields = ['comment', 'complaint__ticket_number']


@admin.register(ComplaintHistory)
class ComplaintHistoryAdmin(admin.ModelAdmin):
    list_display = ['complaint', 'field_name', 'old_value', 'new_value', 'changed_by', 'changed_at']
    list_filter = ['field_name', 'changed_at']
    readonly_fields = ['complaint', 'changed_by', 'field_name', 'old_value', 'new_value', 'changed_at']
