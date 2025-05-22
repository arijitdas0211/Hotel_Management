from rest_framework.decorators import api_view, permission_classes
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from rest_framework.response import Response
from email_validator import validate_email, EmailNotValidError
from django.db.models import Q
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.utils import timezone
from datetime import timedelta, datetime
import traceback
# Models
from .models import MyUser, SuperUserProfile, StaffType, StaffProfile, CustomerProfile, Table, FoodCategory, Menu, Booking, Order, Billing
# Serializers
from .serializer import SuperUserSerializer, StaffTypeSerializer, StaffSerializer, CustomerSerializer, TableSerializer, FoodCategorySerializer, MenuSerializer, BookingSerializer, OrderSerializer, BillingSerializer

# API_VIEWS
from .apiViews.createSuperUser import createSuperUser
from .apiViews.loginUser import loginUser
from .apiViews.logoutUser import logoutUser
from .apiViews.staffType import staffType
from .apiViews.staff import staff

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

# Both SuperUser and Staff have access
@api_view(['POST', 'GET', 'PATCH', 'DELETE'])
def createTable(request):
    if request.method == 'POST':
        user = request.user
        if not (user.is_staff or user.is_superuser) or not user.is_active:
            return Response({"error": "Unauthorized access denied."}, status=status.HTTP_401_UNAUTHORIZED)
        
        try:
            data = request.data

            if (
                data.get('table_no') is not None and
                data.get('capacity') is not None
            ):
                if Table.objects.filter(table_no=data['table_no']).exists():
                    return Response({"error": "Duplicate entry. Table number already exists"}, status=status.HTTP_400_BAD_REQUEST)
                
                data['created_by_staff'] = user.id
                
                serializer = TableSerializer(data=data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(
                            {
                                "message": "Table Successfully Created",
                                "data": serializer.data,
                            },
                            status=status.HTTP_201_CREATED
                        )
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
            else:
                return Response({"error": "Please enter valid input."}, status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as err:
            traceback.print_exc()
            return Response({"error": "Server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    # GET Method
    if request.method == 'GET':
        return handleGetMethod(Table, "table", TableSerializer, request.user.id)


# Both SuperUser and Staff have access
@api_view(['POST', 'GET', 'PATCH', 'DELETE'])
def createFoodCategory(request):
    if request.method == 'POST':
        user = request.user
        if not (user.is_staff or user.is_superuser) or not user.is_active:
            return Response({"error": "Unauthorized access denied."}, status=status.HTTP_401_UNAUTHORIZED)
        
        try:
            data = request.data

            if (
                data['category_name'] is not None and
                data['food_type'] is not None and
                data['created_by_superuser'] is not None or
                data['created_by_staff'] is not None
            ):
                if FoodCategory.objects.filter(category_name=data['category_name']).exists():
                    return Response({"error": "Duplicate entry. Food Category already exists"}, status=status.HTTP_400_BAD_REQUEST)

                if user.is_staff:
                    data['created_by_staff'] = user.id

                if user.is_superuser:
                    data['created_by_superuser'] = user.id

                category_name = data['category_name']

                serializer = FoodCategorySerializer(data=data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(
                        {
                            "message": f"{category_name} is added into Food Category",
                            "data": serializer.data,
                        },
                        status=status.HTTP_201_CREATED
                    )
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
            return Response({"error": "Please enter valid input."}, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as err:
            traceback.print_exc()
            return Response({"error": "Server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    # GET Method
    if request.method == 'GET':
        return handleGetMethod(FoodCategory, "foodCategory", FoodCategorySerializer, request.user.id)


# Both SuperUser and Staff have access
@api_view(['POST', 'GET', 'PATCH', 'DELETE'])
def createMenu(request):
    if request.method == 'POST':
        user = request.user
        if not (user.is_staff or user.is_superuser) or not user.is_active:
            return Response({"error": "Unauthorized access denied."}, status=status.HTTP_401_UNAUTHORIZED)
        
        try:
            data = request.data

            if (
                data['item_name'] is not None and
                data['item_price'] is not None and data['item_price'] > 0 and
                data['food_type'] is not None and
                data['item_image'] is not None and
                data['food_category'] is not None
            ):
                if Menu.objects.filter(item_name=data['item_name']).exists():
                    return Response({"error": "Duplicate entry. Food Category already exists"}, status=status.HTTP_400_BAD_REQUEST)
                
                if user.is_staff:
                    data['created_by_staff'] = user.id

                if user.is_superuser:
                    data['created_by_superuser'] = user.id

                item_name = data['item_name']

                serializer = MenuSerializer(data=data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(
                        {
                            "message": f"{item_name} is added into Menu",
                            "data": serializer.data
                        },
                        status=status.HTTP_201_CREATED
                    )
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
            return Response({"error": "Please enter valid input."}, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as err:
            traceback.print_exc()
            return Response({"error": "Server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    # GET Method
    if request.method == 'GET':
        return handleGetMethod(Menu, "menu", MenuSerializer, request.user.id)


# Both Staff and User have access
@api_view(['POST', 'GET', 'PATCH', 'DELETE'])
def createBooking(request):
    if request.method == 'POST':
        user = request.user

        if not user.is_authenticated or not user.is_active:
            return Response({"error": "Unauthorized access denied."}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            data = request.data
            booking_date = data.get('booking_date')
            booking_time = data.get('booking_time')
            no_of_people = data.get('no_of_people')
            table = data.get('table')

            if not (booking_date and booking_time and no_of_people and table):
                return Response({"error": "Missing required fields."}, status=status.HTTP_400_BAD_REQUEST)

            if int(no_of_people) <= 0:
                return Response({"error": "Invalid number of people."}, status=status.HTTP_400_BAD_REQUEST)

            if user.is_staff:
                data['staff'] = user.id
            else:
                data['customer'] = user.id

            try:
                booking_datetime = datetime.strptime(f"{booking_date} {booking_time}", "%Y-%m-%d %H:%M:%S")
            except ValueError:
                try:
                    booking_datetime = datetime.strptime(f"{booking_date} {booking_time}", "%Y-%m-%d %H:%M")
                except ValueError:
                    return Response({"error": "Invalid date or time format."}, status=status.HTTP_400_BAD_REQUEST)

            start_time = booking_datetime - timedelta(hours=1)  # Checking for 1 hour before
            end_time = booking_datetime + timedelta(hours=1)  # Checking for 1 hour after

            conflicts_exists = Booking.objects.filter(
                booking_date=booking_date,
                table=table,
                booking_time__range=(start_time.time(), end_time.time())
            ).exists()

            if conflicts_exists:
                return Response({"error": "This time slot is already booked."}, status=status.HTTP_400_BAD_REQUEST)

            serializer = BookingSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    "message": "Booking created successfully.",
                    "data": serializer.data
                }, status=status.HTTP_201_CREATED)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception:
            traceback.print_exc()
            return Response({"error": "Server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    # GET Method
    if request.method == 'GET':
        return handleGetMethod(Booking, "booking", BookingSerializer, request.user.id)


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
        
    # GET Method
    if request.method == 'GET':
        return handleGetMethod(Order, "order", OrderSerializer, request.user.id)


# Both SuperUser and Staff have access
@api_view(['POST', 'GET', 'PATCH', 'DELETE'])
def createBilling(request):
    pass




#   ===================================
#   ----- Frontend User API Views -----
#   ===================================

