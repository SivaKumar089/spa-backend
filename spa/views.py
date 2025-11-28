from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Service, Appointment
from .serializers import (
    ServiceSerializer,
    AppointmentSerializer,
    AppointmentDetailSerializer
)

# ---------------------------------
# SERVICE VIEWSET (NO AUTH REQUIRED)
# ---------------------------------
class ServiceViewSet(viewsets.ModelViewSet):
    """
    Anyone can GET, POST, PUT, DELETE services (NO AUTH)
    Only first 2 services shown on listing
    """
    queryset = Service.objects.filter(is_active=True)
    serializer_class = ServiceSerializer
    permission_classes = [permissions.AllowAny]

    def list(self, request, *args, **kwargs):
        services = Service.objects.filter(is_active=True)[:2]
        serializer = self.get_serializer(services, many=True)
        return Response(serializer.data)


# ---------------------------------
# APPOINTMENT VIEWSET (NO AUTH)
# ---------------------------------
class AppointmentViewSet(viewsets.ModelViewSet):
    """
    Anyone can create appointment
    Anyone can view all appointments
    Anyone can approve or reject
    (NO LOGIN REQUIRED)
    """
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.AllowAny]

    # ---------------------------
    # USER CAN CREATE APPOINTMENT
    # ---------------------------
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {
                "message": "Appointment request sent successfully!",
                "data": serializer.data,
            },
            status=status.HTTP_201_CREATED,
        )

    # ---------------------------
    # FILTER — PENDING
    # ---------------------------
    @action(detail=False, methods=["get"], permission_classes=[permissions.AllowAny])
    def pending(self, request):
        appointments = Appointment.objects.filter(status="pending")
        serializer = AppointmentDetailSerializer(appointments, many=True)
        return Response(serializer.data)

    # ---------------------------
    # FILTER — APPROVED
    # ---------------------------
    @action(detail=False, methods=["get"], permission_classes=[permissions.AllowAny])
    def approved(self, request):
        appointments = Appointment.objects.filter(status="approved")
        serializer = AppointmentDetailSerializer(appointments, many=True)
        return Response(serializer.data)

    # ---------------------------
    # FILTER — REJECTED
    # ---------------------------
    @action(detail=False, methods=["get"], permission_classes=[permissions.AllowAny])
    def rejected(self, request):
        appointments = Appointment.objects.filter(status="rejected")
        serializer = AppointmentDetailSerializer(appointments, many=True)
        return Response(serializer.data)

    # ---------------------------
    # APPROVE APPOINTMENT (NO AUTH)
    # ---------------------------
    @action(detail=True, methods=["post"], permission_classes=[permissions.AllowAny])
    def approve(self, request, pk=None):
        appointment = self.get_object()

        if appointment.status != "pending":
            return Response(
                {"error": "Only pending appointments can be approved"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        appointment.status = "approved"
        appointment.save()

        serializer = AppointmentDetailSerializer(appointment)
        return Response(
            {"message": "Appointment approved successfully", "data": serializer.data}
        )

    # ---------------------------
    # REJECT APPOINTMENT (NO AUTH)
    # ---------------------------
    @action(detail=True, methods=["post"], permission_classes=[permissions.AllowAny])
    def reject(self, request, pk=None):
        appointment = self.get_object()

        if appointment.status != "pending":
            return Response(
                {"error": "Only pending appointments can be rejected"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        notes = request.data.get("notes", "")

        appointment.status = "rejected"
        appointment.notes = notes
        appointment.save()

        serializer = AppointmentDetailSerializer(appointment)
        return Response(
            {"message": "Appointment rejected", "data": serializer.data}
        )
