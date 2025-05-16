from rest_framework.decorators import api_view, permission_classes
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from email_validator import validate_email, EmailNotValidError
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.utils import timezone
import traceback
from datetime import timedelta, datetime

from .models import SuperUser, StaffType, Staff, Table, FoodCategory, Menu, Booking, Order, Billing
from .serializer import SuperUserSerializer, StaffTypeSerializer, StaffSerializer, TableSerializer, FoodCategorySerializer, MenuSerializer, BookingSerializer, OrderSerializer, BillingSerializer
# GET, PATCH, PUT, DELETE
from .controller import handleGetMethod, handlePatchMethod, handleDeleteMethod

#   ===================================
#   ----- Backend User API Views -----
#   ===================================
# SuperUser Registration
@api_view(['POST'])
def createSuperUser(request):
    try:
        data = request.data

        valid_email = validate_email(data['email']).email

        if (
            len(data['name']) > 2 and 
            len(str(data['phone'])) == 10 and 
            valid_email == data['email'] and 
            len(data['username']) > 3 and 
            len(data['password']) > 3
        ):
            if SuperUser.objects.filter(email=data['email']).exists():
                return Response({"error": "Email already exists!"}, status=status.HTTP_400_BAD_REQUEST)

            if SuperUser.objects.filter(phone=data['phone']).exists():
                return Response({"error": "Phone number already exists!"}, status=status.HTTP_400_BAD_REQUEST)

            if SuperUser.objects.filter(username=data['username']).exists():
                return Response({"error": "Username already exists!"}, status=status.HTTP_400_BAD_REQUEST)

            full_name = data['name'].split(" ")
            first_name = full_name[0]
            last_name = " ".join(full_name[1:])

            user = User.objects.create_superuser(
                first_name=first_name,
                last_name=last_name,
                email=data['email'],
                username=data['username'],
                password=data['password']
            )

            data['user'] = user.id
            data['password'] = make_password(data['password'])

            serializer = SuperUserSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response({"error": "Please enter valid input!"}, status=status.HTTP_400_BAD_REQUEST)

    except EmailNotValidError as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as err:
        traceback.print_exc()
        return Response({"error": "Server Error!"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# SuperUser, Staff Login (by phone, email, or username)
@api_view(['POST', 'GET'])
def loginUser(request):
    if request.method == 'POST':
        try:
            data = request.data
            username = data['username']
            password = data['password']

            if not username or not password:
                return Response({"error": "Phone/Username and Password are required."}, status=status.HTTP_400_BAD_REQUEST)

            try:
                user = (
                    SuperUser.objects.filter(phone=username).first() or
                    Staff.objects.filter(phone=username).first() or
                    User.objects.filter(username=username).first() or
                    User.objects.filter(email=username).first()
                )

                if not user:
                    return Response({"error": "User Not Found."}, status=status.HTTP_404_NOT_FOUND)

                # myUser = user.id
                auth_user = authenticate(username=user.username, password=password)

                if auth_user and auth_user.is_authenticated and user.is_active:
                    login(request, user)
                    user.last_login = timezone.now()
                    user.save()
                    return Response({
                        "message": "Login Successful.",
                        "username": user.username,
                        "email": user.email,
                        "is_staff": user.is_staff,
                        "is_superuser": user.is_superuser
                    }, status=status.HTTP_200_OK)
                else:
                    return Response({"error": "Incorrect Password."}, status=status.HTTP_401_UNAUTHORIZED)

            except SuperUser.DoesNotExist:
                return Response({"error": "User Not Found."}, status=status.HTTP_404_NOT_FOUND)

        except Exception as err:
            traceback.print_exc()
            return Response({"error": "Server Error."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    # GET Method
    if request.method == 'GET':
        try:
            return handleGetMethod(SuperUser, "superuser", SuperUserSerializer, request.user.id)
        except:
            return handleGetMethod(Staff, "staff", StaffSerializer, request.user.id)


@api_view(['POST'])
def logoutUser(request):
    user = request.user
    logout(request)
    return Response({"message": "Login Successful."}, status=status.HTTP_200_OK)


# Create Staff Type
@api_view(['POST', 'GET', 'PATCH', 'DELETE'])
def createStaffType(request):
    user = request.user
    if not user.is_superuser or not user.is_active:
        return Response({"error": "Unauthorized Access Denied."}, status=status.HTTP_403_FORBIDDEN)
    
    # POST Method
    if request.method == 'POST':
        try:
            data = request.data
            if not data['staff_type_name'] or len(data['staff_type_name']) < 3:
                return Response({"error": "Invalid Staff Type."}, status=status.HTTP_400_BAD_REQUEST)

            if StaffType.objects.filter(staff_type_name=data['staff_type_name']).exists():
                return Response({"error": "Staff type already exists."}, status=status.HTTP_400_BAD_REQUEST)
            
            data['created_by'] = user.id

            serializer = StaffTypeSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    "message": "Staff type successfully created.",
                    "data": serializer.data
                }, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as err:
            traceback.print_exc()
            return Response({"error": "Something went wrong."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    # GET Method
    if request.method == 'GET':
        return handleGetMethod(StaffType, "staffType", StaffTypeSerializer, request.user.id)


# Create Staff
@api_view(['POST', 'GET', 'PATCH', 'DELETE'])
def createStaff(request):
    if request.method == 'POST':
        user = request.user
        if not user.is_superuser or not user.is_active:
            return Response({"error": "Unauthorized Access Denied."}, status=status.HTTP_403_FORBIDDEN)

        try:
            data = request.data

            if data['email']:
                try:
                    valid_email = validate_email(data['email']).email
                    if valid_email != data['email']:
                        return Response({"error": "Invalid email."}, status=status.HTTP_400_BAD_REQUEST)
                except EmailNotValidError as e:
                    return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

            if (
                len(data['name']) > 2 and
                len(str(data['phone'])) == 10 and
                len(data['username']) > 3 and
                len(data['password']) > 3
            ):
                if Staff.objects.filter(email=data['email']).exists():
                    return Response({"error": "Email already exists!"}, status=status.HTTP_400_BAD_REQUEST)

                if Staff.objects.filter(phone=data['phone']).exists():
                    return Response({"error": "Phone number already exists!"}, status=status.HTTP_400_BAD_REQUEST)

                if Staff.objects.filter(username=data['username']).exists():
                    return Response({"error": "Username already exists!"}, status=status.HTTP_400_BAD_REQUEST)

                full_name = data['name'].split(" ")
                first_name = full_name[0]
                last_name = " ".join(full_name[1:])

                staffUser = User.objects.create_user(
                    first_name=first_name,
                    last_name=last_name,
                    email=data['email'],
                    username=data['username'],
                    password=data['password'],
                    is_active=data.get('is_active', True),
                    is_superuser=data.get('is_superuser', False)
                )

                data['user'] = staffUser.id
                data['superuser'] = user.id
                data['password'] = make_password(data['password'])

                serializer = StaffSerializer(data=data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            return Response({"error": "Please enter valid input!"}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as err:
            traceback.print_exc()
            return Response({"error": "Server Error!"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    # GET Method
    if request.method == 'GET':
        return handleGetMethod(Staff, "staff", StaffSerializer, request.user.id)


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

