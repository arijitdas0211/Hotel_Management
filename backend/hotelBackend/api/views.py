from .models import SuperUser
from .serializer import SuperUserSerializer, StaffTypeSerializer
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from email_validator import validate_email
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import json


# Create your views here.
# User Registration
@api_view(['POST'])
def createSuperUser(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            # Validate the email format
            valid_email = validate_email(data['email']).email

            if (
                len(data['name']) > 2 and 
                len(str(data['phone'])) == 10 and 
                valid_email == data['email'] and 
                len(data['username']) > 3 and 
                len(data['password']) > 3
            ):
                    # Check email existence
                    if SuperUser.objects.filter(email=data['email']).exists():
                        return Response({"error": "Email already exists!"}, status=status.HTTP_400_BAD_REQUEST)
                    
                    # Check phone existence
                    if SuperUser.objects.filter(phone=data['phone']).exists():
                        return Response({"error": "Phone number already exists!"}, status=status.HTTP_400_BAD_REQUEST)
                    
                    # Check username existence
                    if SuperUser.objects.filter(username=data['username']).exists():
                        return Response({"error": "Username already exists!"}, status=status.HTTP_400_BAD_REQUEST)

                    # Hash the password

                    full_name = data['name'].split(" ")
                    first_name = full_name[0]
                    last_name = " ".join(full_name[1:])
                    
                    user = User.objects.create_superuser(
                        first_name = first_name,
                        last_name = last_name,
                        email = data['email'],
                        username = data['username'],
                        password = data['password'],
                        is_active = True,
                        is_superuser = True
                    )
                    user.save()

                    data['user'] = user.id
                    data['password'] = make_password(data['password'])

                    serializer = SuperUserSerializer(data=data)

                    print(f"SuperUser Created: {user.get_full_name()} | {user.email}")

                    if serializer.is_valid():
                        serializer.save()
                        return Response(serializer.data, status=status.HTTP_201_CREATED)
                    else:
                        print(f"Serializer Error: {serializer.errors}")
                        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
            else:
                return Response({"error": "Please enter valid input!"}, status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as err:
            print(f"Invalid input: {err}")
            return Response({"error": "Server Error!"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# User Login
@api_view(['POST'])
def loginSuperUser(request):
    if request.method == 'POST':
        try:
            data = request.data
            username = data['username']
            password = data['password']

            if (not username) or (not password):
                return Response({"error": "Phone/Username and Password are required to Login."}, status=status.HTTP_400_BAD_REQUEST)

            try:
                user = User.objects.get(phone = username)
            except:
                try:
                    user = User.objects.get(username = username)
                except User.DoesNotExist:
                    return Response({"error": "User Not Found."}, status=status.HTTP_404_NOT_FOUND)
            
            if user and check_password(password, user.password):
                auth_user = authenticate(username=user.username, password=password)
                
            if auth_user and auth_user.is_authenticated:
                login(request, user)
                return Response({
                    "message": "Login Successful.",
                    "username": user.username,
                    "email": user.email,
                    "is_superuser": user.is_superuser
                }, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Incorrect Password."}, status=status.HTTP_401_UNAUTHORIZED)
            
        except Exception as err:
            print(f"Login Error: {err}")
            return Response({"error": "Server Error."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Add Staff Type
@api_view(['POST'])
@login_required
def createStaffType(request):
    if request.method == 'POST':
        try:
            data = request.data

            if not data['staff_type_name'] or not len(data['staff_type_name']) > 2:
                return Response({"error": "Invalid Staff Type."}, status=status.HTTP_400_BAD_REQUEST)
            
            try:
                serializer = StaffTypeSerializer(data=data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, {"message": "Staff type successfully created."}, status=status.HTTP_201_CREATED)
            except Exception as err:
                print(f"Serializer Error: {serializer.errors}")
                return Response(serializer.errors, {"error": "Error while creating staff."}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as err:
            print(f"Staff Type can't be added: {err}")
            return Response({"error": "Something went wrong."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


