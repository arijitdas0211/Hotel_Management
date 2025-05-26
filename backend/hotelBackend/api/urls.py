from django.urls import path
from .views import createSuperUser, loginUser, logoutUser, staffType, staff, foodCategory, menu, table, booking, createOrder

urlpatterns = [
    path('admin/register/', createSuperUser, name = 'createSuperUser'),
    path('admin/login/', loginUser, name = 'loginUser'),
    path('admin/logout/', logoutUser, name = 'logoutUser'),
    path('admin/stafftype/', staffType, name = 'staffType'),
    path('admin/stafftype/<int:pk>', staffType, name = 'staffType'),
    path('admin/staff/', staff, name = 'staff'),
    path('admin/food_Category/', foodCategory, name = 'foodCategory'),
    path('admin/menu/', menu, name = 'menu'),
    path('admin/table/', table, name = 'table'),
    path('admin/booking/', booking, name = 'booking'),
    path('admin/order/', createOrder, name = 'createOrder'),
]
