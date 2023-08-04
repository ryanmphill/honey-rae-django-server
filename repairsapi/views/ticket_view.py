"""View module for handling requests for ticket data"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from repairsapi.models import ServiceTicket, Employee, Customer


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

            if "status" in request.query_params:
                if request.query_params['status'] == "done":
                    tickets = tickets.filter(date_completed__isnull=False)

                if request.query_params['status'] == "all":
                    pass

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
    
    def create(self, request):
            """Handle POST requests for service tickets

            Returns:
                Response: JSON serialized representation of newly created service ticket
            """
            new_ticket = ServiceTicket()
            new_ticket.customer = Customer.objects.get(user=request.auth.user)
            new_ticket.description = request.data['description']
            new_ticket.emergency = request.data['emergency']
            new_ticket.save()

            serialized = TicketSerializer(new_ticket, many=False)

            return Response(serialized.data, status=status.HTTP_201_CREATED)
    
    def update(self, request, pk=None):
        """Handle put requests for single customer

        Returns:
              Response -- no response body, just 204 status code
        """

        # Select the targeted ticket using pk
        ticket = ServiceTicket.objects.get(pk=pk)

        # Get employee id from the client request
        employee_id = request.data['employee']

        # Select the employee from the database using that id
        assigned_employee = Employee.objects.get(pk=employee_id)

        # Assign that employee instance to the employee property of the ticket
        ticket.employee = assigned_employee

        # Save the updated ticket
        ticket.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
    def destroy(self, request, pk=None):
        """Handle delete requests for single customer

        Returns:
              Response -- no response body, just 204 status code
        """

        # Select the targeted ticket using pk
        ticket = ServiceTicket.objects.get(pk=pk)

        # Remove the targeted ticket from the database
        ticket.delete()

        return Response(None, status=status.HTTP_204_NO_CONTENT)

class TicketEmployeeSerializer(serializers.ModelSerializer):
    """JSON serializer for full_name on employee"""

    class Meta:
        model = Employee
        fields = ('id', 'user', 'specialty', 'full_name')

class TicketCustomerSerializer(serializers.ModelSerializer):
    """JSON serializer for full_name on customer"""

    class Meta:
        model = Customer
        fields = ('id', 'user', 'address', 'full_name')

class TicketSerializer(serializers.ModelSerializer):
    """JSON serializer for tickets"""
    
    employee = TicketEmployeeSerializer(many=False)
    customer = TicketCustomerSerializer(many=False)

    class Meta:
        model = ServiceTicket
        fields = ('id', 'customer', 'employee', 'description', 'emergency', 'date_completed')
        depth = 1
