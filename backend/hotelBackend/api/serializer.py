from rest_framework import serializers
from .models import (
    SuperUserProfile, StaffType, StaffProfile, CustomerProfile,
    Table, FoodCategory, Menu, Booking, Order,
    Billing, Feedback
)


# Profiles serializers
class SuperUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = SuperUserProfile
        fields = "__all__"


class StaffTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaffType
        fields = "__all__"

class StaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaffType
        fields = ['id', 'staff_type_name', 'created_by']


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerProfile
        fields = "__all__"


# Table serializers
class TableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Table
        fields = "__all__"


# Food Category serializers
class FoodCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodCategory
        fields = "__all__"


# Menu serializers
class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = "__all__"


# Booking serializer
class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = "__all__"


# Order serializer
class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"


# Billing serializer
class BillingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Billing
        fields = "__all__"


# Feedback serializer
class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = "__all__"

