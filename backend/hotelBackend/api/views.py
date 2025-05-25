from rest_framework.decorators import api_view, permission_classes
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from rest_framework.response import Response
import traceback
# from email_validator import validate_email, EmailNotValidError
# from django.db.models import Q
# from django.contrib.auth.hashers import make_password
# from django.contrib.auth import authenticate, login, logout
# from django.utils import timezone
# from datetime import timedelta, datetime
# # Models
from .models import MyUser, SuperUserProfile, StaffType, StaffProfile, CustomerProfile, Table, FoodCategory, Menu, Booking, Order, Billing
# # Serializers
from .serializer import SuperUserSerializer, StaffTypeSerializer, StaffSerializer, CustomerSerializer, TableSerializer, FoodCategorySerializer, MenuSerializer, BookingSerializer, OrderSerializer, BillingSerializer

# API_VIEWS
from .apiViews.createSuperUser import createSuperUser
from .apiViews.loginUser import loginUser
from .apiViews.logoutUser import logoutUser
from .apiViews.staffType import staffType
from .apiViews.staff import staff
from .apiViews.table import table
from .apiViews.foodCategory import foodCategory
from .apiViews.menu import menu
from .apiViews.booking import booking

#   ===================================
#   ----- Backend User API Views ------
#   ===================================
# Register SuperUser
createSuperUser

# Login SuperUser, Staff and Customer
loginUser

# Logout SuperUser, Staff and Customer
logoutUser

# Create, Get, Update and Delete Staff Type
staffType

# Create, Get, Update and Delete Staff
staff

# Create, Get, Update and Delete Table
table

# Create, Get, Update and Delete Food Category
foodCategory

# Create, Get, Update and Delete Menu
menu

# Create, Get, Update Booking
booking

# Create, Get, Update Table
# Both SuperUser and Staff have access
@api_view(['POST', 'GET', 'PATCH', 'DELETE'])
def createOrder(request):
    if request.method == 'POST':
        user = request.user

        if not user.is_authenticated or not user.is_active:
            return Response({"error": "Unauthorized access denied."}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            data = request.data

            items = data.get('items')

            if not items:
                return Response({"error": "Items are required to create an order."}, status=status.HTTP_400_BAD_REQUEST)

            if user.is_staff:
                data['staff'] = user.id
            else:
                data['customer'] = user.id

            serializer = OrderSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    "message": "Order is created successfully.",
                    "data": serializer.data
                }, status=status.HTTP_201_CREATED)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as err:
            traceback.print_exc()
            return Response({"error": "Server error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Both SuperUser and Staff have access
@api_view(['POST', 'GET', 'PATCH', 'DELETE'])
def createBilling(request):
    pass



#   ===================================
#   ----- Frontend User API Views -----
#   ===================================

