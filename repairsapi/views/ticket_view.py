"""View module for handling requests for ticket data"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from repairsapi.models import ServiceTicket, Employee


class TicketView(ViewSet):
    """Honey Rae API tickets view"""

    def list(self, request):
        """Handle GET requests to get all tickets

        Returns:
            Response -- JSON serialized list of tickets
        """
        tickets = []

        if request.auth.user.is_staff:
            tickets = ServiceTicket.objects.all()
        else:
            tickets = ServiceTicket.objects.filter(customer__user=request.auth.user)

        serialized = TicketSerializer(tickets, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single ticket

        Returns:
            Response -- JSON serialized ticket record
        """

        ticket = ServiceTicket.objects.get(pk=pk)
        serialized = TicketSerializer(ticket, context={'request': request})
        return Response(serialized.data, status=status.HTTP_200_OK)

class TicketEmployeeSerializer(serializers.ModelSerializer):
    """JSON serializer for full_name on employee"""

    class Meta:
        model = Employee
        fields = ('id', 'user', 'specialty', 'full_name')

class TicketSerializer(serializers.ModelSerializer):
    """JSON serializer for tickets"""
    
    employee = TicketEmployeeSerializer(many=False)

    class Meta:
        model = ServiceTicket
        fields = ('id', 'customer', 'employee', 'description', 'emergency', 'date_completed')
        depth = 1
