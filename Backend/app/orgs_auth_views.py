import hashlib
from datetime import datetime

from django.db.models import Q
from django.shortcuts import render

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Organization, CustomToken
from .serializers import OrganizationSerializer
from .helper_functions import get_object, get_token

# Register Organization
class OrganizationRegisterView(APIView):

    # Sigup user (create new object)
    def post(self, request):

        org_data = dict(request.data)

        if len(org_data['password'])<6:
            return Response({"Invalid Password"}, status=status.HTTP_400_BAD_REQUEST)
        serializer = OrganizationSerializer(data=org_data)       

        if serializer.is_valid():
            serializer.save()

            org = Organization.objects.get(org_name=org_data['org_name'])
            token = get_token(org.id, 1)
            org_data['token'] = token
            del org_data['password']
            try:
                orgtoken = CustomToken.objects.get(object_id=org.id, user_type=1)
                return Response({"message":"Organization Already Logged in", "Organization":org_data}, status=status.HTTP_400_BAD_REQUEST)
            except CustomToken.DoesNotExist:
                CustomToken.objects.create(
                    user_type=1,
                    object_id=org.id,
                    token=token
                )
                return Response({"message":"Organization Registered successfully", "Organization":org_data}, status=status.HTTP_201_CREATED)
        else:
            return Response({"message":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


# View for user login
class OrganizationLoginView(APIView):
    
    def post(self, request):
        req_data = request.data
        try:
            org = Organization.objects.get(org_name=req_data['org_name'])
        except Organization.DoesNotExist:
            return Response({"message":"Invalid Organization Name"}, status=status.HTTP_400_BAD_REQUEST)
        
        m = hashlib.md5()     
        m.update(req_data['password'].encode("utf-8"))
        if org.password == str(m.digest()):
            token = get_token(org.id, 1)
            try:
                orgtoken = CustomToken.objects.get(object_id=org.id, user_type=1)
                token = orgtoken.token
            except CustomToken.DoesNotExist:
                CustomToken.objects.create(
                    user_type=1,
                    object_id=org.id,
                    token=token
                )
            return Response({"message":"Organization Logged in", 
                "Organization":{
                    "id":org.id,
                    "email":org.email,
                    "org_name":org.org_name,
                    "phone_no":org.phone_no,
                    "address":org.address,
                    "areas_catered":org.areas_catered,
                    "description":org.description,
                    "web_link":org.web_link, 
                    "token":token
                }
            })
        else:
            return Response({"message":"Invalid Password"}, status=status.HTTP_403_FORBIDDEN)
        

# Signout new user
class OrganizationLogoutView(APIView):

    def get(self, request, format=None):

        # Get User and delete the token
        token = request.headers.get('Authorization', None)
        if token is None or token=="":
            return Response({"message":"Authorization credentials missing"}, status=status.HTTP_403_FORBIDDEN)
        
        org = get_object(token)
        if org is None:
            return Response({"message":"Organization Already Logged Out"}, status=status.HTTP_403_FORBIDDEN)

        response = {
            "message":"Organization logged out", 
            "Details":{
                "id":org.id,
                "email":org.email,
                "org_name":org.org_name,
                "phone_no":org.phone_no,
                "address":org.address,
                "areas_catered":org.areas_catered,
                "description":org.description,
                "web_link":org.web_link
            }}
        
        usertoken = CustomToken.objects.get(object_id=org.id, user_type=1)
        usertoken.delete()
        return Response(response, status=status.HTTP_200_OK)


class OrganizationDetailsView(APIView):

    def get(self, request):
        token = request.headers.get('Authorization', None)
        if token is None or token=="":
            return Response({"message":"Authorization credentials missing"}, status=status.HTTP_403_FORBIDDEN)
        
        org = get_object(token)
        if org is None:
            return Response({"message":"Organization Not Found"}, status=status.HTTP_403_FORBIDDEN)
        response = {
            "message":"Organization details", 
            "Organization":{
                "id":org.id,
                "email":org.email,
                "org_name":org.org_name,
                "phone_no":org.phone_no,
                "address":org.address,
                "areas_catered":org.areas_catered,
                "description":org.description,
                "web_link":org.web_link
            }}
        return Response(response, status=status.HTTP_200_OK)
