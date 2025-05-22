from .imports import *

@csrf_exempt
@api_view(['POST', 'GET'])
def loginUser(request):
    if request.method == 'POST':
        try:
            data = request.data
            username = str(data.get('username', '')).strip()
            password = data.get('password', '')

            if not username or not password:
                return Response({"error": "Username and Password both are required."}, status=400)

            # Try to find the user from any of the 3 profile tables
            user = None
            if SuperUserProfile.objects.filter(Q(phone=username) | Q(email=username)).exists():
                profile = SuperUserProfile.objects.get(Q(phone=username) | Q(email=username))
                user = profile.myUser
            elif StaffProfile.objects.filter(Q(phone=username) | Q(email=username)).exists():
                profile = StaffProfile.objects.get(Q(phone=username) | Q(email=username))
                user = profile.myUser
            elif CustomerProfile.objects.filter(Q(phone=username) | Q(email=username)).exists():
                profile = CustomerProfile.objects.get(Q(phone=username) | Q(email=username))
                user = profile.myUser
            elif MyUser.objects.filter(username=username).exists():
                user = MyUser.objects.get(username=username)

            if not user:
                return Response({"error": "User Not Found."}, status=404)

            if not user.is_active:
                return Response({"error": "User account is inactive."}, status=403)

            auth_user = authenticate(username=user.username, password=password)

            if auth_user and auth_user.is_authenticated:
                login(request, auth_user)
                user.last_login = timezone.now()
                user.save()

                # Now return the correct profile
                if user.user_type == 'superuser':
                    profile = SuperUserProfile.objects.get(myUser=user)
                    return Response({"data": SuperUserSerializer(profile).data}, status=200)
                elif user.user_type == 'staff':
                    profile = StaffProfile.objects.get(myUser=user)
                    return Response({"data": StaffSerializer(profile).data}, status=200)
                elif user.user_type == 'customer':
                    profile = CustomerProfile.objects.get(myUser=user)
                    return Response({"data": CustomerSerializer(profile).data}, status=200)
                else:
                    return Response({"error": "Unknown user role."}, status=400)

            return Response({"error": "Incorrect Password."}, status=401)

        except Exception as e:
            traceback.print_exc()
            return Response({"error": "Server Error."}, status=500)

    # GET method: return logged-in user's profile
    elif request.method == 'GET':
        user = request.user
        if not user or not user.is_authenticated:
            return Response({"error": "Unauthorized."}, status=401)
        try:
            if user.user_type == 'superuser':
                profile = SuperUserProfile.objects.get(myUser=user)
                return Response({"data": SuperUserSerializer(profile).data}, status=200)
            elif user.user_type == 'staff':
                profile = StaffProfile.objects.get(myUser=user)
                return Response({"data": StaffSerializer(profile).data}, status=200)
            elif user.user_type == 'customer':
                profile = CustomerProfile.objects.get(myUser=user)
                return Response({"data": CustomerSerializer(profile).data}, status=200)
            else:
                return Response({"error": "User role not found."}, status=404)
        except Exception:
            traceback.print_exc()
            return Response({"error": "Server Error."}, status=500)
