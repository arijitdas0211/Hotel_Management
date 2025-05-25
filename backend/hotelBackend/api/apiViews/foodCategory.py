from .imports import *;
from django.utils.text import slugify

# Both SuperUser and Staff have access
@api_view(['POST', 'GET', 'PATCH', 'DELETE'])
def foodCategory(request, pk):
    user = request.user
    if not (SuperUserProfile.objects.get(myUser=user.id) or StaffProfile.objects.get(myUser=user.id)) and not user.is_active:
        return Response({"error": "Unauthorized access denied."}, status=status.HTTP_401_UNAUTHORIZED)
    
    # POST Method
    if request.method == 'POST':
        try:
            data = request.data
            
            category_name = str(data.get('category_name')).strip()
            food_type = str(data.get('food_type')).strip()
            fc_status = str(data.get('status')).strip()
            slug = slugify(category_name)

            if (
                category_name is not None and 
                food_type is not None
            ):
                if FoodCategory.objects.filter(category_name=category_name).exists():
                    return Response({"error": "Duplicate entry. Food category already exists"}, status=status.HTTP_400_BAD_REQUEST)
                
                data['category_name'] = category_name
                data['food_type'] = food_type
                data['status'] = fc_status
                data['slug'] = slug
                data['created_by'] = user.id
                
                serializer = FoodCategorySerializer(data=data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(
                            {
                                "message": "Food Category Successfully Created",
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
                foodCategory = FoodCategory.objects.filter(id=pk)
                serializer = FoodCategorySerializer(foodCategory)
                return Response({"data": serializer.data}, status=status.HTTP_200_OK)
            else:
                foodCategories = FoodCategory.objects.all()
                serializer = FoodCategorySerializer(foodCategories, many=True)
                return Response({"data": serializer.data}, status=status.HTTP_200_OK)
            
        except Exception:
            traceback.print_exc()
            return Response({"error": "Something went wrong while fetching data."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    # PATCH Method
    if request.method == 'PATCH':
        data = request.data
        try:
            category_name = str(data.get('category_name')).strip()
            food_type = str(data.get('food_type')).strip()
            fc_status = str(data.get('status')).strip()
            slug = slugify(category_name)
            
            if (
                category_name is not None and
                food_type is not None
            ):
                foodCategory = FoodCategory.objects.get(id=pk)
                if foodCategory:
                    foodCategory.category_name = category_name
                    foodCategory.food_type = food_type
                    foodCategory.status = fc_status
                    foodCategory.slug = slug
                        
                    foodCategory.save()
                    serializer = FoodCategorySerializer(foodCategory)
                    return Response(
                        {
                            "message": "Food Category Successfully Updated.",
                            "data": serializer.data,
                        },
                        status=status.HTTP_200_OK
                    )
                else:
                    return Response({"error": "Food Category not found."}, status=status.HTTP_404_NOT_FOUND)
                
            else:
                return Response({"error": "Please enter valid input."}, status=status.HTTP_400_BAD_REQUEST)
            
        except FoodCategory.DoesNotExist:
            return Response({"error": "Food Category table not found."}, status=status.HTTP_404_NOT_FOUND)
        
    # DELETE Method
    if request.method == 'DELETE':
        try:
            foodCategory = FoodCategory.objects.get(id=pk)
            if foodCategory:
                foodCategory.delete()
                return Response({"message": "Food Category deleted successfully."}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Food Category not found."}, status=status.HTTP_404_NOT_FOUND)
            
        except FoodCategory.DoesNotExist:
            return Response({"error": "Food Category table not found."}, status=status.HTTP_404_NOT_FOUND)
        
        