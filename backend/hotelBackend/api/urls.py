from django.urls import path
from .views import createSuperUser, loginUser, logoutUser, createStaffType, createStaff, createFoodCategory, createMenu, createTable, createBooking, createOrder

urlpatterns = [
    path('admin/register/', createSuperUser, name = 'createSuperUser'),
    path('admin/login/', loginUser, name = 'loginUser'),
    path('admin/logout/', logoutUser, name = 'logoutUser'),
    path('admin/auth/create/staff_Type/', createStaffType, name = 'createStaffType'),
    path('admin/auth/create/staff/', createStaff, name = 'createStaff'),
    path('admin/auth/create/food_Category/', createFoodCategory, name = 'createFoodCategory'),
    path('admin/auth/create/menu/', createMenu, name = 'createMenu'),
    path('admin/auth/create/table/', createTable, name = 'createTable'),
    path('admin/auth/create/booking/', createBooking, name = 'createBooking'),
    path('admin/auth/create/order/', createOrder, name = 'createOrder'),
]
