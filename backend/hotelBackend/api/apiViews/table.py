from .imports import *;

# Both SuperUser and Staff have access
@api_view(['POST', 'GET', 'PATCH', 'DELETE'])
def table(request, pk):
    user = request.user
    if not (SuperUserProfile.objects.get(myUser=user.id) or StaffProfile.objects.get(myUser=user.id)) and not user.is_active:
        return Response({"error": "Unauthorized access denied."}, status=status.HTTP_401_UNAUTHORIZED)
    
    # POST Method
    if request.method == 'POST':        
        try:
            data = request.data
            
            table_no = str(data.get('table_no')).strip()
            capacity = str(data.get('capacity')).strip()
            t_status = str(data.get('status')).strip()

            if (
                table_no is not None and
                capacity is not None
            ):
                if Table.objects.filter(tableNo=table_no).exists():
                    return Response({"error": "Duplicate entry. Table number already exists"}, status=status.HTTP_400_BAD_REQUEST)
                
                data['tableNo'] = table_no
                data['capacity'] = capacity
                data['status'] = t_status
                data['created_by'] = user.id
                
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
        try:
            if pk:
                table = Table.objects.filter(id=pk)
                serializer = TableSerializer(table)
                return Response({"data": serializer.data}, status=status.HTTP_200_OK)
            else:
                tables = Table.objects.all()
                serializer = TableSerializer(tables, many=True)
                return Response({"data": serializer.data}, status=status.HTTP_200_OK)
            
        except Exception:
            traceback.print_exc()
            return Response({"error": "Something went wrong white fetching data."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    # PATCH Method
    if request.method == 'PATCH':
        data = request.data
        try:
            table_no = str(data.get('tableNo')).strip()
            capacity = str(data.get('capacity')).strip()
            t_status = str(data.get('status')).strip()
            
            if (
                table_no is not None and
                capacity is not None
            ):
                table = Table.objects.get(id=pk)
                if table:
                    if table_no:
                        table.tableNo = table_no
                    if capacity:
                        table.capacity = capacity
                    if t_status:
                        table.status = t_status
                        
                    table.save()
                    serializer = TableSerializer(table)
                    if serializer.is_valid():
                        serializer.save()
                        return Response(
                            {
                                "message": "Table Successfully Updated.",
                                "data": serializer.data,
                            },
                            status=status.HTTP_200_OK
                        )
                else:
                    return Response({"error": "Table not found."}, status=status.HTTP_404_NOT_FOUND)
                
            else:
                return Response({"error": "Please enter valid input."}, status=status.HTTP_400_BAD_REQUEST)
            
        except Table.DoesNotExist:
            return Response({"error": "Table not found."}, status=status.HTTP_404_NOT_FOUND)
        
    # DELETE Method
    if request.method == 'DELETE':
        try:
            table = Table.objects.get(id=pk)
            if table:
                table.delete()
                return Response({"message": "Table deleted successfully."}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Table not found."}, status=status.HTTP_404_NOT_FOUND)
            
        except Table.DoesNotExist:
            return Response({"error": "Table not found."}, status=status.HTTP_404_NOT_FOUND)
        

            
                