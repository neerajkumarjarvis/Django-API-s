from django.http import HttpResponse,JsonResponse
import datetime
from rest_framework import mixins, viewsets, views
from rest_framework.templatetags.rest_framework import data
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView  # for api
from rest_framework import viewsets
from rest_framework.response import Response
from django.shortcuts import render, redirect
from django.core.files import File
from .models import Voter
from rest_framework.views import APIView
from django.core import serializers
import json


class GetVoters(views.APIView):

    def get(self,request):

        state = request.query_params.get('state')
        limit = request.query_params.get('limit')
        offset = request.query_params.get('offset')

        if state==None or limit==None or offset==None:
            if state == None and limit == None and offset == None:
                return Response({'message': 'State, Limit and Offset are required'}, status=400)
            if state == None and limit == None and offset != None:
                return Response({'message': 'State and Limit are required'}, status=400)
            if state == None and limit != None and offset == None:
                return Response({'message': 'State and Offset are required'}, status=400)
            if state != None and limit == None and offset == None:
                return Response({'message': 'Limit and Offset are required'}, status=400)
            if state != None and limit != None and offset == None:
                return Response({'message': 'Offset is required'}, status=400)
            if state != None and limit == None and offset != None:
                return Response({'message': 'Limit is required'}, status=400)
            if state == None and limit != None and offset != None:
                return Response({'message': 'State is required'}, status=400)


        state = state.lower() + '_db'
        limit = int(request.query_params.get('limit'))
        offset = int(request.query_params.get('offset'))

        name = request.query_params.get('name')
        ac_no=request.query_params.get('ac_no')
        gender=request.query_params.get('gender')

        voters =Voter.objects.using(state).all()
        # print(voters)

        if name:
            name=name.upper()
            voters = voters.filter(name__startswith=name)

            print('NAME VOTERS')
        if ac_no:
            voters = voters.filter(ac_no=ac_no)
            print('AC_NO VOTERS')

        if gender:
            voters = voters.filter(gender__iexact=gender)
            print('GENDER VOTERS')
            print(voters)

        voters = voters.order_by('s_no')
        print(type(voters))
        voters = voters[offset:limit + offset].values()
        l=[]
        for i in voters:
            l.append(i)
        newlist = sorted(l, key=lambda d: d['name'])


        return Response({'message': 'Voter List', 'data': newlist}, status=200)



