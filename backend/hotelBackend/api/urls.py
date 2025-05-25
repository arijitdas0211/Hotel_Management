from django.urls import path
from .views import createSuperUser, loginUser, logoutUser, staffType, staff, foodCategory, menu, table, booking, createOrder

urlpatterns = [
    path('admin/register/', createSuperUser, name = 'createSuperUser'),
    path('admin/login/', loginUser, name = 'loginUser'),
    path('admin/logout/', logoutUser, name = 'logoutUser'),
    path('admin/auth/create/staff_Type/', staffType, name = 'staffType'),
    path('admin/auth/create/staff/', staff, name = 'staff'),
    path('admin/auth/create/food_Category/', foodCategory, name = 'foodCategory'),
    path('admin/auth/create/menu/', menu, name = 'menu'),
    path('admin/auth/create/table/', table, name = 'table'),
    path('admin/auth/create/booking/', booking, name = 'booking'),
    path('admin/auth/create/order/', createOrder, name = 'createOrder'),
]
