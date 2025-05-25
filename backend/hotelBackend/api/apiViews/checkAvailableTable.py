from .imports import *

# Check for Table Availability
@api_view(['GET'])
def checkTableAvailability(request):    
    try:
        tables = Table.objects.filter(status='free')
        if not tables.exists():
            return False
            # return Response(False, status=status.HTTP_404_NOT_FOUND)
        else:
            serializer = TableSerializer(tables, many=True)
            return Response({
                "data": serializer.data
            }, status=status.HTTP_200_OK)
            
    except Exception:
        traceback.print_exc()
        return Response({"error": "Server error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

