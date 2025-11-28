from rest_framework import serializers
from .models import Service, Appointment
from django.utils import timezone
class ServiceSerializer(serializers.ModelSerializer):
    """Serializer for Service model"""
    
    class Meta:
        model = Service
        fields = [
            'id', 'name', 'description', 'duration', 
            'price', 'image_url', 'is_active'
        ]
        read_only_fields = ['id']


class AppointmentSerializer(serializers.ModelSerializer):
    """Serializer for creating appointments"""
    
    service_name = serializers.CharField(source='service.name', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = Appointment
        fields = [
            'id', 'name', 'email', 'phone', 'service', 'service_name',
            'appointment_date', 'appointment_time', 'message', 
            'status', 'status_display', 'created_at'
        ]
        read_only_fields = ['id', 'status', 'created_at']

    def validate_appointment_date(self, value):
        """Ensure appointment date is not in the past"""
        if value < timezone.now().date():
            raise serializers.ValidationError("Appointment date cannot be in the past")
        return value


class AppointmentDetailSerializer(serializers.ModelSerializer):
    """Detailed serializer for admin view"""
    
    service_details = ServiceSerializer(source='service', read_only=True)
    reviewed_by_username = serializers.CharField(
        source='reviewed_by.username', 
        read_only=True
    )
    
    class Meta:
        model = Appointment
        fields = '__all__'