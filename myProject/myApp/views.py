from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import Organization, Role, User
from .serializers import OrganizationSerializer, RoleSerializer, OrganizationUpdateSerializer, RoleUpdateSerializer
from datetime import timedelta
from datetime import datetime
from .permissions import IsSuperAdminOrAdminOnly

# Create your views here.

###Create Organization
@api_view(['POST'])
@permission_classes(['IsAuthenticated'])  # Only authenticated users can access
def create_organization(request):
    user_role = User.objects.get(username=request.user)
    if user_role.roles in ['Super Admin', 'Admin']:
        serializer = OrganizationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_at = datetime.now())
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response("You don't have permission to create organizations", status=status.HTTP_403_FORBIDDEN)


###Retrieve Organization Details: All roles can retrieve details of organizations.
@api_view(['GET'])
@permission_classes(['IsAuthenticated'])  # Only authenticated users can access
def get_organization_details(request, organization_id):
    try:
        get_organization = Organization.objects.get(id=organization_id)
        serializer = OrganizationSerializer(get_organization)
        return Response(serializer.data)
    except Organization.DoesNotExist:
        return Response("Organization not found", status=status.HTTP_404_NOT_FOUND)
    

###
@api_view(['PUT'])
@permission_classes(['IsAuthenticated'])
def update_organization(request, organization_id):
    try:
        organization = Organization.objects.get(organization_id = organization_id)
    except Organization.DoesNotExist:
        return Response("Organization not found", status=status.HTTP_404_NOT_FOUND)

    get_user = User.objects.get(username=request.user)

    if get_user.role in ['Super Admin', 'Admin'] and organization.admin == request.user:
        serializer = OrganizationUpdateSerializer(organization, data = request.data, partial=True)
    else:
        return Response("You don't have permission to update organization information", status=status.HTTP_403_FORBIDDEN)
    if serializer.is_valid():
        serializer.save(created_at = datetime.now())
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    


###Delete Organization
@api_view(['DELETE'])
@permission_classes([IsSuperAdminOrAdminOnly])
def delete_organization(request, organization_id):
    try:
        organization = Organization.objects.get(organization_id=organization_id)
    except Organization.DoesNotExist:
        return Response("Organization not found", status=status.HTTP_404_NOT_FOUND)

    organization.delete()
    return Response("Organization deleted successfully", status=status.HTTP_204_NO_CONTENT)

###List organiations
@api_view(['GET'])
def list_organizations(request, organization_id):
    queryset = Role.objects.filter(organization=organization_id)
    serializer = OrganizationSerializer(queryset, many=True)
    #return Response(serializer.data)
    return Response(serializer.data)


###Create Role
@api_view(['POST'])
@permission_classes(['IsAuthenticated'])  # Only authenticated users can access
def create_role(request, organization_id):
    user_role = User.objects.get(username=request.user)
    if user_role.roles in ['Super Admin', 'Admin']:
        serializer = RoleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response("You don't have permission to create organizations", status=status.HTTP_403_FORBIDDEN)


###Retrieve Role Details: All roles can retrieve details of roles.
@api_view(['GET'])
@permission_classes(['IsAuthenticated'])  # Only authenticated users can access
def get_role_details(request, organization_id):
    try:
        get_role = Role.objects.filter(organization_id=organization_id)
        serializer = RoleSerializer(get_role, many=True)
        return Response(serializer.data)
    except Organization.DoesNotExist:
        return Response("Roles not found", status=status.HTTP_404_NOT_FOUND)


###Update Role
@api_view(['PUT'])
@permission_classes(['IsAuthenticated'])
def update_role(request, organization_id):
    try:
        role_obj = Role.objects.get(organization_id = organization_id)
    except Organization.DoesNotExist:
        return Response("RoleOrganization not found", status=status.HTTP_404_NOT_FOUND)

    get_user = User.objects.get(username=request.user)

    if get_user.role in ['Super Admin', 'Admin'] and role_obj.admin == request.user:
        serializer = RoleUpdateSerializer(role_obj, data = request.data, partial=True)
    else:
        return Response("You don't have permission to update role information", status=status.HTTP_403_FORBIDDEN)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 

###Delete Role
@api_view(['DELETE'])
@permission_classes([IsSuperAdminOrAdminOnly])
def delete_role(request, organization_id):
    try:
        role = Role.objects.get(organization_id=organization_id)
    except Organization.DoesNotExist:
        return Response("Role not found", status=status.HTTP_404_NOT_FOUND)

    role.delete()
    return Response("Role deleted successfully", status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@permission_classes(['IsAuthenticated'])
def role_list(request, organization_id):
        roles = Role.objects.filter(organization_id=organization_id)
        serializer = RoleSerializer(roles, many=True)
        return Response(serializer.data)
