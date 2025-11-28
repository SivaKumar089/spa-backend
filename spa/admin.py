from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.utils.html import format_html
from .models import Service, Appointment


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    """Admin interface for Service model"""
    
    list_display = ['name', 'price', 'duration', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    list_editable = ['is_active']


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    """Admin interface for Appointment model"""
    
    list_display = [
        'name', 'service', 'appointment_date', 
        'appointment_time', 'status_badge', 'created_at'
    ]
    list_filter = ['status', 'appointment_date', 'created_at']
    search_fields = ['name', 'email', 'phone']
    readonly_fields = ['created_at', 'updated_at', 'reviewed_at']
    
    fieldsets = (
        ('Customer Information', {
            'fields': ('name', 'email', 'phone')
        }),
        ('Appointment Details', {
            'fields': ('service', 'appointment_date', 'appointment_time', 'message')
        }),
        ('Status', {
            'fields': ('status', 'reviewed_by', 'reviewed_at', 'admin_notes')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def status_badge(self, obj):
        """Display colored status badge"""
        colors = {
            'pending': 'orange',
            'approved': 'green',
            'rejected': 'red'
        }
        return format_html(
            '<span style="background-color: {}; color: white; padding: 5px 10px; '
            'border-radius: 5px;">{}</span>',
            colors.get(obj.status, 'gray'),
            obj.get_status_display()
        )
    status_badge.short_description = 'Status'

    actions = ['approve_appointments', 'reject_appointments']

    def approve_appointments(self, request, queryset):
        """Bulk approve appointments"""
        count = 0
        for appointment in queryset.filter(status='pending'):
            appointment.approve(request.user)
            count += 1
        self.message_user(request, f'{count} appointment(s) approved successfully')
    approve_appointments.short_description = 'Approve selected appointments'

    def reject_appointments(self, request, queryset):
        """Bulk reject appointments"""
        count = 0
        for appointment in queryset.filter(status='pending'):
            appointment.reject(request.user)
            count += 1
        self.message_user(request, f'{count} appointment(s) rejected')
    reject_appointments.short_description = 'Reject selected appointments'
