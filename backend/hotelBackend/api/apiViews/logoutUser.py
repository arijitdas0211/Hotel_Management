from .imports import *

@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logoutUser(request):
    try:
        logout(request)
        return Response({"message": "Logout Successful."}, status=status.HTTP_200_OK)
    except:
        traceback.print_exc()
        return Response({"message": "Logout Failed."}, status=status.HTTP_400_BAD_REQUEST)