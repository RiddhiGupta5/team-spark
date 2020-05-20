import hashlib
from datetime import datetime

from django.db.models import Q
from django.shortcuts import render

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Donation, CustomToken, CustomUser, Organization
from .serializers import DonationSerializer
from .helper_functions import get_object, check_user

class DonationView(APIView):

    def post(self, request):

        token = request.headers.get('Authorization', None)

        if token is None or token=="":
            return Response({"message":"Authorization credentials missing"}, status=status.HTTP_403_FORBIDDEN)

        if check_user(token)==1:
            return Response({'message':"Only general users are allowed to make donations"}, status=status.HTTP_400_BAD_REQUEST)
        
        user = get_object(token)
        if user is None:
            return Response({"message":"You need to login to perform this action !"}, status=status.HTTP_403_FORBIDDEN)

        data = dict(request.data)
        data['user_id'] = user.id
        data['location'] = user.address
        serializer = DonationSerializer(data = data)

        if serializer.is_valid():
            serializer.save()
            return Response({"message":serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, pk):
        
        try:
            donation = Donation.objects.get(id=pk)
            serializer = DonationSerializer(donation)
            serializer = serializer.data
            user = CustomUser.objects.get(id=donation.user_id.id)
            serializer['username'] = user.username
            if donation.org_id:
                org = Organization.objects.get(id=donation.org_id.id)                
                serializer['org_name'] = org.org_name
            else:
                serializer['org_name'] = None
            return Response({"message":"Donation Found", "Donation":serializer}, status=status.HTTP_200_OK)
        except Donation.DoesNotExist:
            return Response({"message":"Donation not found or Invalid id number"}, status=status.HTTP_204_NO_CONTENT)

class AllDontaionView(APIView):

    def get(self, request):
        token = request.headers.get('Authorization', None)

        if token is None or token=="":
            return Response({"message":"Authorization credentials missing"}, status=status.HTTP_403_FORBIDDEN)
        
        required_object = get_object(token)
        if required_object is None:
            return Response({"message":"You need to login to perform this action !"}, status=status.HTTP_403_FORBIDDEN)

        if check_user(token)==0:
            donations = Donation.objects.filter(user_id=required_object.id)
        else:
            donations = Donation.objects.filter(is_accepted=False)

        serializer = DonationSerializer(donations, many=True)
        serializer_data = serializer.data
        for donation in serializer_data:
            user = CustomUser.objects.get(id=donation['user_id'])
            donation['username'] = user.username
            if donation['org_id']:
                org = Organization.objects.get(id=donation['org_id'])                
                donation['org_name'] = org.org_name
            else:
                donation['org_name'] = None
        return Response({"message":"Donations Found", "Donations":serializer_data}, status=status.HTTP_200_OK)

class MessagesView(APIView):

    def get(self, request):
        token = request.headers.get('Authorization', None)

        if token is None or token=="":
            return Response({"message":"Authorization credentials missing"}, status=status.HTTP_403_FORBIDDEN)
        
        user = get_object(token)
        if user is None:
            return Response({"message":"You need to login to perform this action !"}, status=status.HTTP_403_FORBIDDEN)

        if check_user(token)==0:
            donations = Donation.objects.filter(user_id=user.id, is_accepted=True)
        else:
            return Response({"message":"Only for general users"}, status=status.HTTP_403_FORBIDDEN)

        result = []
        for donation in donations:
            org = Organization.objects.get(id=donation.org_id.id)
            result.append({
                "username":user.username,
                "org_name":org.org_name,
                "message":donation.message,
                "id":donation.id,
                "item_name":donation.item_name
            })
        
        return Response({"message":"Donations found", "Donations":result}, status=status.HTTP_200_OK)

class AccpetDonationView(APIView):

    def post(self, request):
        token = request.headers.get('Authorization', None)

        if token is None or token=="":
            return Response({"message":"Authorization credentials missing"}, status=status.HTTP_403_FORBIDDEN)

        if check_user(token)==0:
            return Response({'message':"Only Organizations are allowed to accept requests"}, status=status.HTTP_400_BAD_REQUEST)
        
        org = get_object(token)
        if org is None:
            return Response({"message":"You need to login to perform this action !"}, status=status.HTTP_403_FORBIDDEN)

        try:
            donation = Donation.objects.get(id=request.data.get('donation_id', None))
            donation.is_accepted = True
            donation.org_id = org
            if request.data.get('message', None)==None:
                return Response({"message":"message missing"}, status=status.HTTP_400_BAD_REQUEST)
            donation.message = request.data.get('message', None)
            donation.save()
            return Response({"message":"Donation accepted"}, status=status.HTTP_200_OK)
        except Donation.DoesNotExist:
            return Response({"message":"Donation not found"}, status=status.HTTP_400_BAD_REQUEST)
