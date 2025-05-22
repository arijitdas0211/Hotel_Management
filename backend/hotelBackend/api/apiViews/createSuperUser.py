from .imports import *

@api_view(['POST'])
def createSuperUser(request):
    try:
        data = request.data

        # Email validation
        try:
            validate_email(data['email']).email
        except:
            return Response({"error": "Invalid email format"}, status=status.HTTP_400_BAD_REQUEST)

        # Extract safely
        name = str(data.get('name', '')).strip()
        email = str(data.get('email', '')).strip()
        username = str(data.get('username', '')).strip()
        phone = str(data.get('phone', '')).strip()
        password = str(data.get('password', '')).strip()

        # Validating each fields
        if len(name) <= 2:
            return Response({"error": "Name must be at least 3 characters long."}, status=status.HTTP_400_BAD_REQUEST)
        if not phone.isdigit or len(phone) != 10:
            return Response({"error": "Phone number must be exactly 10 digits."}, status=status.HTTP_400_BAD_REQUEST)
        if len(username) < 3:
            return Response({"error": "Username must be at least 3 characters long."}, status=status.HTTP_400_BAD_REQUEST)
        if len(password) < 4:
            return Response({"error": "Password must be at least 4 characters long."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Uniqueness checks
        if SuperUserProfile.objects.filter(email=email).exists():
            return Response({"error": "Email already exists!"}, status=status.HTTP_400_BAD_REQUEST)
        if MyUser.objects.filter(username=username).exists():
            return Response({"error": "Username already exists!"}, status=status.HTTP_400_BAD_REQUEST)
        if SuperUserProfile.objects.filter(phone=phone).exists():
            return Response({"error": "Phone number already exists!"}, status=status.HTTP_400_BAD_REQUEST)

        # Name split
        full_name = name.split()
        first_name = full_name[0]
        last_name = " ".join(full_name[1:]) if len(full_name) > 1 else "None"

        # Create user
        try:
            user = MyUser.objects.create_user(
                username = username,
                password = password,
                is_active = True,
                is_staff = True,
                is_superuser = True,
                user_type = "superuser"
            )
        except Exception as e:
            print("User creation error:", e)
            return Response({"error": "Failed to create user"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        superuser_data = {
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "phone": phone,
            "myUser": user.id
        }

        serializer = SuperUserSerializer(data=superuser_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            print("Serializer errors:", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except Exception as err:
        traceback.print_exc()
        return Response({"error": "Server Error!"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

