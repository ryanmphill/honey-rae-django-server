from django.contrib import admin
from django.conf.urls import include
from django.urls import path
from rest_framework import routers
from repairsapi.views import CustomerView, EmployeeView, TicketView
from repairsapi.views import register_user, login_user

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'customers', CustomerView, 'customer')
router.register(r'employees', EmployeeView, 'employee')
router.register(r'serviceTickets', TicketView, 'serviceTicket')

# The trailing_slash=False tells the router to accept /customers instead of /customers/.
# It’s a very annoying error to come across, when your server is not responding and the code looks right, 
# the only issue is your fetch url is missing a / at the end.

# The next line is what sets up the /customers resource. The first parameter, r'customers, 
# is setting up the URL. The second CustomerView is telling the server which view to 
# use when it sees that url.

# The third, customer, is called the base name. You’ll only see the base name if you get an 
# error in the server. It acts as a nickname for the resource and is usually the singular 
# version of the URL.

urlpatterns = [
    path('register', register_user),
    path('login', login_user),
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
]