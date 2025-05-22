from rest_framework.decorators import api_view, permission_classes
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from rest_framework.response import Response
from email_validator import validate_email, EmailNotValidError
from django.db.models import Q
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.utils import timezone
from datetime import timedelta, datetime
import traceback
# Models
from ..models import MyUser, SuperUserProfile, StaffType, StaffProfile, CustomerProfile, Table, FoodCategory, Menu, Booking, Order, Billing
# Serializers
from ..serializer import SuperUserSerializer, StaffTypeSerializer, StaffSerializer, CustomerSerializer, TableSerializer, FoodCategorySerializer, MenuSerializer, BookingSerializer, OrderSerializer, BillingSerializer
# GET, PATCH, PUT, DELETE
from ..controller import handleGetMethod, handlePatchMethod, handleDeleteMethod