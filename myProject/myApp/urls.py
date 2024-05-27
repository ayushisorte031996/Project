from . import views
from django.urls import path
from .views import create_organization, get_organization_details, update_organization, delete_organization, create_role, get_role_details, delete_role, list_organizations, role_list

urlpatterns = [
    path('create_organization/', create_organization, name='create_organization'),
    path('get_organization_details/<int:organization_id>/', get_organization_details, name='get_organization_details'),
    path('update_organization/<int:organization_id>/', update_organization, name='update_organization'),
    path('delete_organization/<int:organization_id>/', delete_organization, name='delete_organization'),
    path('list_organizations/<int:organization_id>/', list_organizations, name='list_organizations'),


    path('create_role/<int:organization_id>/', create_role, name='create_role'),
    path('get_role_details/<int:organization_id>/', get_role_details, name='get_role_details'),
    path('update_organization/<int:organization_id>/', update_organization, name='update_organization'),
    path('delete_role/<int:organization_id>/', delete_role, name='delete_role'),
    path('role_list/<int:organization_id>/', role_list, name='role_list'),

]
