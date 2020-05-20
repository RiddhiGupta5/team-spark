import hashlib
from datetime import datetime

from django.db.models import Q
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .donation_views import AllDontaionView, DonationView, MessagesView, AccpetDonationView
from .help_prg_views import AllHelpProgramView, HelpProgramView
from .helper_functions import get_object, get_token
from .models import CustomToken, CustomUser, PhoneNumbers
from .orgs_auth_views import (OrganizationDetailsView, OrganizationLoginView,
                              OrganizationLogoutView, OrganizationRegisterView)
from .serializers import UserLoginSerializer, UserSignupSerializer, PhoneNumbersSerializer


# Ping Server
class PingView(APIView):

    def get(self, request):
        return Response({"message":"OK"}, status=status.HTTP_200_OK)

# Sign up a new user View
class UserSignupView(APIView):

    # Sigup user (create new object)
    def post(self, request):

        user_data = {}
        user_data['email'] = request.data.get("email", None)
        user_data['username'] = request.data.get("username", None)
        user_data['phone_no'] = request.data.get("phone_no", None)
        user_data['address'] = request.data.get("address", None)
        user_data['password'] = request.data.get("password", None)
        if len(user_data['password'])<6:
            return Response({"Invalid Password"}, status=status.HTTP_400_BAD_REQUEST)
        serializer = UserSignupSerializer(data=user_data)       

        if serializer.is_valid():
            serializer.save()

            user = CustomUser.objects.get(email=user_data['email'])

            # Storing phone number
            phone_no = {
                'phone_no':user.phone_no
            }
            phone_serializer = PhoneNumbersSerializer(data=phone_no)
            if phone_serializer.is_valid():
                phone_serializer.save()

            token = get_token(user.id, 0)
            user_data['token'] = token
            del user_data['password']
            try:
                usertoken = CustomToken.objects.get(object_id=user.id, user_type=0)
                return Response({"message":"User Already Logged in", "User":user_data}, status=status.HTTP_400_BAD_REQUEST)
            except CustomToken.DoesNotExist:
                CustomToken.objects.create(
                    user_type=0,
                    object_id=user.id,
                    token=token
                )
                return Response({"message":"User Signed up successfully", "User":user_data}, status=status.HTTP_201_CREATED)
        else:
            return Response({"message":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


# View for user login
class UserLoginView(APIView):
    
    def post(self, request):
        req_data = request.data
        try:
            user = CustomUser.objects.get(email=req_data['email'])
        except CustomUser.DoesNotExist:
            return Response({"message":"Invalid Email"}, status=status.HTTP_400_BAD_REQUEST)
        
        m = hashlib.md5()     
        m.update(req_data['password'].encode("utf-8"))
        if user.password == str(m.digest()):
            token = get_token(user.id, 0)
            try:
                usertoken = CustomToken.objects.get(object_id=user.id, user_type=0)
                token = usertoken.token
            except CustomToken.DoesNotExist:
                CustomToken.objects.create(
                    user_type=0,
                    object_id=user.id,
                    token=token
                )
            return Response({"message":"User Logged in", 
                "User":{
                    "id":user.id,
                    "email":user.email,
                    "username":user.username,
                    "phone_no":user.phone_no,
                    "address":user.address,
                    "token":token
                }
            })
        else:
            return Response({"message":"Invalid Password"}, status=status.HTTP_403_FORBIDDEN)
        

# Signout new user
class UserLogoutView(APIView):

    def get(self, request, format=None):

        # Get User and delete the token
        token = request.headers.get('Authorization', None)
        if token is None or token=="":
            return Response({"message":"Authorization credentials missing"}, status=status.HTTP_403_FORBIDDEN)
        
        user = get_object(token)
        if user is None:
            return Response({"message":"User Already Logged Out"}, status=status.HTTP_403_FORBIDDEN)

        response = {
            "message":"User logged out", 
            "Details":{
                "id": user.id,
                "email":user.email,
                "username":user.username,
                "phone_no":user.phone_no,
                "address":user.address
            }}
        
        usertoken = CustomToken.objects.get(object_id=user.id, user_type=0)
        usertoken.delete()
        return Response(response, status=status.HTTP_200_OK)

class UserDetailsView(APIView):

    def get(self, request):
        token = request.headers.get('Authorization', None)
        if token is None or token=="":
            return Response({"message":"Authorization credentials missing"}, status=status.HTTP_403_FORBIDDEN)
        
        user = get_object(token)
        if user is None:
            return Response({"message":"User Not Found"}, status=status.HTTP_403_FORBIDDEN)
        response = {
            "message":"User details", 
            "User":{
                "id": user.id,
                "email":user.email,
                "username":user.username,
                "phone_no":user.phone_no,
                "address":user.address
            }}
        return Response(response, status=status.HTTP_200_OK)

class RegisterPhoneNo(APIView):

    def post(self, request):
        phone_no = request.data.get('phone_no', None)
        if not phone_no or len(phone_no)!=10:
            return Response({"message":"Invalid Phone Number"}, status=status.HTTP_400_BAD_REQUEST)

        phone_serializer = PhoneNumbersSerializer(data=request.data)
        if phone_serializer.is_valid():
            phone_serializer.save()
            return Response({"message": "Phone Number registered"}, status=status.HTTP_200_OK)
        else:
            return Response({'message':"Phone number already registered"}, status=status.HTTP_200_OK)

