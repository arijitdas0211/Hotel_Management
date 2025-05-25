from .imports import *
from django.utils.text import slugify

# Both SuperUser and Staff have access
@api_view(['POST', 'GET', 'PATCH', 'DELETE'])
def menu(request, pk):
    user = request.user
    if not (SuperUserProfile.objects.get(myUser=user.id) or StaffProfile.objects.get(myUser=user.id)) and not user.is_active:
        return Response({"error": "Unauthorized access denied."}, status=status.HTTP_401_UNAUTHORIZED)
    
    # POST Method
    if request.method == 'POST':
        try:
            data = request.data
            
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
                food_type is not None and
                food_category is not None and
                food_img is not None and
                m_status is not None
            ):
                if Menu.objects.filter(name=name).exists():
                    return Response({"error": "Duplicate entry. Menu already exists"}, status=status.HTTP_400_BAD_REQUEST)
                
                data['name'] = name
                data['price'] = price
                data['food_type'] = food_type
                data['food_category'] = food_category
                data['image'] = food_img
                data['status'] = m_status
                data['slug'] = slug
                data['created_by'] = user.id
                
                serializer = MenuSerializer(data=data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(
                            {
                                "message": "Menu Successfully Created",
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
                menu = Menu.objects.filter(id=pk)
                serializer = MenuSerializer(menu)
                return Response({"data": serializer.data}, status=status.HTTP_200_OK)
            else:
                foodCategories = Menu.objects.all()
                serializer = MenuSerializer(foodCategories, many=True)
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
            menu = Menu.objects.get(id=pk)
            if menu:
                menu.delete()
                return Response({"message": "Menu deleted successfully."}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Menu not found."}, status=status.HTTP_404_NOT_FOUND)
            
        except Menu.DoesNotExist:
            return Response({"error": "Menu table not found."}, status=status.HTTP_404_NOT_FOUND)
        
