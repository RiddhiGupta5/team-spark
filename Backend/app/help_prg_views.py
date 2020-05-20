# Add prog (post), get(all, by id)
import hashlib
from datetime import datetime

from django.db.models import Q
from django.shortcuts import render

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import HelpProgram, CustomToken, Organization, PhoneNumbers
from .serializers import HelpProgramSerializer
from .helper_functions import get_object, check_user, sendSMS

class HelpProgramView(APIView):

    def post(self, request):

        token = request.headers.get('Authorization', None)

        if token is None or token=="":
            return Response({"message":"Authorization credentials missing"}, status=status.HTTP_403_FORBIDDEN)

        if check_user(token)==0:
            return Response({'message':"Only Organizations are allowed to make help programs"}, status=status.HTTP_400_BAD_REQUEST)
        
        org = get_object(token)
        if org is None:
            return Response({"message":"You need to login to perform this action !"}, status=status.HTTP_403_FORBIDDEN)

        data = dict(request.data)
        data['org_id'] = org.id
        serializer = HelpProgramSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            phone_numbers = PhoneNumbers.objects.all()
            phone_numbers = [num.phone_no for num in phone_numbers]
            message = org.org_name + ' is organizing ' + serializer.data['prg_name'] + '\n' \
                + 'Aid Provided: ' + serializer.data['aid_provided'] + '\n'\
                + 'Description: ' + serializer.data['description'] + '\n'\
                + 'Address: ' + serializer.data['address'] + '\n'
            sendSMS(phone_numbers, message)
            print(message)
            return Response({"message":serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, pk):
        
        try:
            prg = HelpProgram.objects.get(id=pk)
            serializer = HelpProgramSerializer(prg)
            serializer = serializer.data
            org = Organization.objects.get(id=prg.org_id.id)
            serializer['org_name'] = org.org_name
            return Response({"message":"Help Program Found", "HelpProgram":serializer}, status=status.HTTP_200_OK)
        except Donation.DoesNotExist:
            return Response({"message":"Help Program not found or Invalid id number"}, status=status.HTTP_204_NO_CONTENT)

class AllHelpProgramView(APIView):

    def get(self, request):
        prgs = HelpProgram.objects.all()
        serializer = HelpProgramSerializer(prgs, many=True)
        serializer_data = serializer.data
        for prg in serializer_data:
            org = Organization.objects.get(id=prg['org_id'])
            prg['org_name'] = org.org_name
        return Response({"message":"Help Programs Found", "HelpPrograms":serializer_data}, status=status.HTTP_200_OK)
