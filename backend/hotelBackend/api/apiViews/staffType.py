from .imports import *

@api_view(['POST', 'GET', 'PATCH', 'DELETE'])
@permission_classes([IsAuthenticated])
def staffType(request, pk=None):
    user = request.user
    if not SuperUserProfile.objects.filter(myUser=user).exists():
        return Response({"error": "Unauthorized Access Denied."}, status=status.HTTP_403_FORBIDDEN)

    # POST Method
    if request.method == 'POST':
        try:
            data = request.data
            print("Request data:", data)
            staffType = request.data.get('staffType')
            if not staffType or len(staffType) < 2:
                return Response({"error": "Invalid Staff Type."}, status=status.HTTP_400_BAD_REQUEST)

            if StaffType.objects.filter(staffType=staffType).exists():
                return Response({"error": "Staff type already exists."}, status=status.HTTP_400_BAD_REQUEST)

            try:
                super_profile = SuperUserProfile.objects.get(myUser=user)
            except SuperUserProfile.DoesNotExist:
                return Response({"error": "SuperUser profile not found."}, status=status.HTTP_404_NOT_FOUND)
            
            data['created_by'] = super_profile.super_id
            # print("Created by:", data['created_by'])
            data['staffType'] = staffType
            
            serializer = StaffTypeSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                
                return Response({"message": "Staff type successfully created.", "data": serializer.data}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            traceback.print_exc()
            return Response({"error": "Something went wrong."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # GET Method
    elif request.method == 'GET':
        try:
            if pk:
                staff_type = StaffType.objects.get(id=pk)
                serializer = StaffTypeSerializer(staff_type)
                data = serializer.data.copy()  # copy to a mutable dict
                data['created_by'] = staff_type.created_by.myUser.username if staff_type.created_by else None
                return Response({"data": data}, status=status.HTTP_200_OK)

            else:
                staff_types = StaffType.objects.all()
                serializer = StaffTypeSerializer(staff_types, many=True)
                return Response({"data": serializer.data}, status=status.HTTP_200_OK)
        except Exception:
            traceback.print_exc()
            return Response({"error": "Something went wrong while fetching data."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # PATCH Method
    elif request.method == 'PATCH':
        try:
            staff_type_id = request.data.get('id')
            staff_type_name = request.data.get('staff_type_name')

            if not staff_type_id or not staff_type_name:
                return Response({"error": "ID and staff_type_name are required."}, status=status.HTTP_400_BAD_REQUEST)

            staff_type = StaffType.objects.get(id=staff_type_id)
            staff_type.staffType = str(staff_type_name).strip()
            staff_type.save()

            serializer = StaffTypeSerializer(staff_type)
            return Response({"message": "Staff type updated successfully.", "data": serializer.data}, status=status.HTTP_200_OK)

        except StaffType.DoesNotExist:
            return Response({"error": "Staff type not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception:
            traceback.print_exc()
            return Response({"error": "Something went wrong."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # DELETE Method
    elif request.method == 'DELETE':
        try:
            staff_type_id = request.data.get('id')
            if not staff_type_id:
                return Response({"error": "Staff Type ID is required for deletion."}, status=status.HTTP_400_BAD_REQUEST)
            
            staff_type = StaffType.objects.get(id=staff_type_id)
            
            if StaffProfile.objects.filter(staffType=staff_type).exists():
                return Response({"error": "Staff type is associated with Staff."}, status=status.HTTP_400_BAD_REQUEST)
            else:
                staff_type.delete()
                return Response({"message": "Staff type deleted successfully."}, status=status.HTTP_200_OK)

        except StaffType.DoesNotExist:
            return Response({"error": "Staff type not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception:
            traceback.print_exc()
            return Response({"error": "Something went wrong."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
