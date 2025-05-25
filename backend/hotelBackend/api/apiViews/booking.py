from .imports import *
from django.utils.text import slugify
from .checkAvailableTable import checkTableAvailability
    

# Both Staff and User have access
@api_view(['POST', 'GET', 'PATCH'])
def booking(request, pk):
    user = request.user
    if not (SuperUserProfile.objects.get(myUser=user.id) or StaffProfile.objects.get(myUser=user.id) or CustomerProfile.objects.get(myUser=user.id)) and not user.is_active:
        return Response({"error": "Unauthorized access denied."}, status=status.HTTP_401_UNAUTHORIZED)
    
    # POST Method
    if request.method == 'POST':
        if checkTableAvailability == False:
            return  Response({"error": "Tables are not available for booking."}, status=status.HTTP_400_BAD_REQUEST)
            
        try:
            data = request.data
            
            booking_date = str(data.get('booking_date')).strip()
            booking_time = str(data.get('booking_time')).strip()
            totalPeople = str(data.get('totalPeople')).strip()
            table = str(data.get('table')).strip()
            food_type = str(data.get('food_type')).strip()
            customer = str(data.get('customer')).strip()
            assigned_to = str(data.get('assigned_to')).strip()
            b_status = str(data.get('status')).strip()

            if (
                booking_date is not None and 
                booking_time is not None and 
                totalPeople is not None and
                table is not None and
                food_type is not None and
                customer is not None and
                assigned_to is not None and
                b_status is not None
            ):
                check_status = 'confirmed'
                if Booking.objects.filter(b_status=check_status).exists():
                    return Response({"error": "Duplicate entry. Booking already exists"}, status=status.HTTP_400_BAD_REQUEST)
                
                data['booking_date'] = booking_date
                data['booking_time'] = booking_time
                data['totalPeople'] = totalPeople
                data['table'] = table
                data['food_type'] = food_type
                data['customer'] = customer
                data['assigned_to'] = assigned_to
                data['b_status'] = 'confirmed'
                data['created_by'] = user.id
                
                serializer = BookingSerializer(data=data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(
                            {
                                "message": "Booking Successfully Created",
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
        try:
            if pk:
                booking = Booking.objects.filter(id=pk)
                serializer = BookingSerializer(booking)
                return Response({"data": serializer.data}, status=status.HTTP_200_OK)
            else:
                booking = Booking.objects.all()
                serializer = BookingSerializer(booking, many=True)
                return Response({"data": serializer.data}, status=status.HTTP_200_OK)
            
        except Exception:
            traceback.print_exc()
            return Response({"error": "Something went wrong while fetching data."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    # PATCH Method
    if request.method == 'PATCH':
        data = request.data
        try:
            name = str(data.get('name')).strip()
            price = str(data.get('price')).strip()
            food_type = str(data.get('food_type')).strip()
            food_category = str(data.get('food_category')).strip()
            food_img = request.FILES.get('food_img')
            m_status = str(data.get('status')).strip()
            slug = slugify(name)
            
            if (
                name is not None and
                price is not None and 
                food_img is not None
            ):
                menu = Menu.objects.get(id=pk)
                if menu:
                    menu.name = name
                    menu.price = price
                    menu.food_type = food_type
                    menu.food_category = food_category
                    menu.image = food_img
                    menu.status = m_status
                    menu.slug = slug
                    menu.created_by = user.id

                    menu.save()
                    serializer = MenuSerializer(menu)
                    return Response(
                        {
                            "message": "Menu Successfully Updated.",
                            "data": serializer.data,
                        },
                        status=status.HTTP_200_OK
                    )
                else:
                    return Response({"error": "Menu not found."}, status=status.HTTP_404_NOT_FOUND)
                
            else:
                return Response({"error": "Please enter valid input."}, status=status.HTTP_400_BAD_REQUEST)
            
        except Menu.DoesNotExist:
            return Response({"error": "Menu table not found."}, status=status.HTTP_404_NOT_FOUND)
        
    # DELETE Method
    if request.method == 'DELETE':
        try:
            booking = Booking.objects.get(id=pk)
            if booking:
                booking.delete()
                return Response({"message": "Booking deleted successfully."}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Booking not found."}, status=status.HTTP_404_NOT_FOUND)
            
        except Booking.DoesNotExist:
            return Response({"error": "Booking table not found."}, status=status.HTTP_404_NOT_FOUND)
        
        
