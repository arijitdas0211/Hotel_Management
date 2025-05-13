from django.urls import path
from .views import createSuperUser, loginSuperUser, createStaffType

urlpatterns = [
    path('admin/register/', createSuperUser, name = 'createSuperUser'),
    path('admin/login/', loginSuperUser, name = 'loginSuperUser'),
    path('admin/auth/staffType/create/', createStaffType, name = 'createStaffType'),
]
