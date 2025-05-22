from django.contrib import admin
from .models import MyUser, SuperUserProfile, StaffType, StaffProfile, CustomerProfile, Table, FoodCategory, Menu, Booking, Order, Billing, Feedback;

# Register your models here.
admin.site.register(MyUser)
admin.site.register(SuperUserProfile)
admin.site.register(StaffType)
admin.site.register(StaffProfile)
admin.site.register(CustomerProfile)
admin.site.register(Table)
admin.site.register(FoodCategory)
admin.site.register(Menu)   
admin.site.register(Booking)
admin.site.register(Order)
admin.site.register(Billing)
admin.site.register(Feedback)
admin.site.site_header = "Hotel Management System"
admin.site.site_title = "Hotel Management System"
admin.site.index_title = "Welcome to Hotel Management System"
