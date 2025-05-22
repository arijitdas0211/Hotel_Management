from .imports import *

@permission_classes([IsAuthenticated])
@api_view(['POST', 'GET', 'PATCH', 'DELETE'])
def staff(request, pk):
    user = request.user
    if not SuperUserProfile.objects.get(myUser=user.id):
        return Response({"error": "Unauthorized Access Denied."}, status=status.HTTP_403_FORBIDDEN)
    
    # POST Method
    if request.method == 'POST':
        try:
            data = request.data
            
            # Email validation
            try:
                validate_email(data['email']).email
            except:
                return Response({"error": "Invalid email format"}, status=status.HTTP_400_BAD_REQUEST)

            # Extract safely
            name = str(data.get('name')).strip()
            email = str(data.get('email')).strip()
            username = str(data.get('username')).strip()
            phone = str(data.get('phone')).strip()
            password = str(data.get('password')).strip()
            staff_type = str(data.get('staff_type')).strip()
            created_by = user.id

            # Validating each fields
            if len(name) <= 2:
                return Response({"error": "Name must be at least 3 characters long."}, status=status.HTTP_400_BAD_REQUEST)
            if not phone.isdigit or len(phone) != 10:
                return Response({"error": "Phone number must be exactly 10 digits."}, status=status.HTTP_400_BAD_REQUEST)
            if len(username) < 3:
                return Response({"error": "Username must be at least 3 characters long."}, status=status.HTTP_400_BAD_REQUEST)
            if staff_type is None:
                return Response({"error": "Staff type must be selected."}, status=status.HTTP_400_BAD_REQUEST)
            if len(password) < 4:
                return Response({"error": "Password must be at least 4 characters long."}, status=status.HTTP_400_BAD_REQUEST)
            
            # Uniqueness checks
            if StaffProfile.objects.filter(email=email).exists():
                return Response({"error": "Email already exists!"}, status=status.HTTP_400_BAD_REQUEST)
            if MyUser.objects.filter(username=username).exists():
                return Response({"error": "Username already exists!"}, status=status.HTTP_400_BAD_REQUEST)
            if StaffProfile.objects.filter(phone=phone).exists():
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
                    is_superuser = False,
                    user_type = "staff",
                )
            except Exception as e:
                print("User creation error:", e)
                return Response({"error": "Failed to create user"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            staff_data = {
                "first_name": first_name,
                "last_name": last_name,
                "email": email,
                "phone": phone,
                "myUser": user.id,
                "staffType": staff_type,
                "created_by": SuperUserProfile.objects.get(created_by=created_by).super_id
            }

            serializer = StaffSerializer(data=staff_data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                print("Serializer errors:", serializer.errors)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as err:
            traceback.print_exc()
            return Response({"error": "Server Error!"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    # GET Method
    elif request.method == 'GET':
        try:
            if pk:
                staff = StaffProfile.objects.filter(staff_id=pk)
                serializer = StaffSerializer(staff)
                return Response({"data": serializer.data}, status=status.HTTP_200_OK)
            else:
                staff_types = StaffProfile.objects.all()
                serializer = StaffSerializer(staff_types, many=True)
                return Response({"data": serializer.data}, status=status.HTTP_200_OK)
        except Exception:
            traceback.print_exc()
            return Response({"error": "Something went wrong while fetching data."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # PATCH Method
    elif request.method == 'PATCH':
        data = request.data
        try:
            staffId = data.get('id')
            staff_name = str(data.get('staff_name')).strip()
            staff_full_name = staff_name.split()
            first_name = staff_name[0]
            last_name = " ".join(full_name[1:]) if len(full_name) > 1 else "None"
            email = str(data.get('email')).strip()
            phone = str(data.get('phone')).strip()
            
            # Validations
            try:
                validate_email(data['email']).email
            except:
                return Response({"error": "Invalid Email Format."}, status=status.HTTP_400_BAD_REQUEST)
            
            if len(staff_name) < 3 and not staff_name.isalpha:
                return Response({"error": "Name must be at least 3 characters long"}, status=status.HTTP_400_BAD_REQUEST)
                            
            if len(phone) != 10 and not phone.isdigit():
                return Response({"error": "Phone Number must be 10 digits long."}, status=status.HTTP_400_BAD_REQUEST)
                
            if not staff_id:
                return Response({"error": "Staff ID is Required."}, status=status.HTTP_400_BAD_REQUEST)

            staff = StaffProfile.objects.get(staff_id=staffId)
            
            staff.first_name = first_name
            staff.last_name = last_name
            staff.email = email
            staff.phone = phone
            staff.save()

            serializer = StaffSerializer(staff)
            return Response({"message": "Staff updated successfully.", "data": serializer.data}, status=status.HTTP_200_OK)

        except StaffType.DoesNotExist:
            return Response({"error": "Staff not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception:
            traceback.print_exc()
            return Response({"error": "Something went wrong."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # DELETE Method
    elif request.method == 'DELETE':
        try:
            staff_id = request.data.get('id')
            if not staff_id:
                return Response({"error": "Staff ID is Required for deletion."}, status=status.HTTP_400_BAD_REQUEST)
            
            
            staff = StaffProfile.objects.get(id=staff_id)
            user_staff_id = staff.myUser
            user_staff = MyUser.objects.get(id=user_staff_id)
            staff.delete()
            user_staff.delete()
            return Response({"message": "Staff deleted successfully."}, status=status.HTTP_200_OK)

        except StaffType.DoesNotExist:
            return Response({"error": "Staff not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception:
            traceback.print_exc()
            return Response({"error": "Something went wrong."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        