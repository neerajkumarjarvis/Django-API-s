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
from .models import Voter,SaralBooth,BjpVotes
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
        limit = int(limit)
        offset = int(offset)

        name = request.query_params.get('name')
        ac_no=request.query_params.get('ac_no')
        gender=request.query_params.get('gender')
        phone=request.query_params.get('contact_no')
        part_no=request.query_params.get('part_no')

        voters =Voter.objects.using(state).all()
        # print(voters)

        if name:
            name=name.upper()
            voters = voters.filter(name__startswith=name)

        if ac_no:
            voters = voters.filter(ac_no=ac_no)

        if gender:
            voters = voters.filter(gender__iexact=gender)

        if phone:
            voters = voters.filter(contactno=phone)


        if part_no:
            voters = voters.filter(part_no=part_no)


        voters = voters.order_by('s_no')

        voter = voters[offset:limit + offset].values()

        l=[]
        for i in voter:
            l.append(i)
        newlist = sorted(l, key=lambda d: d['name'])


        return Response({'message': 'Voter List', 'data': newlist}, status=200)

class GetVotes(views.APIView):

    def get(self,request):

        booth_id = request.query_params.get('booth_id')
        data = SaralBooth.objects.using('bjp_db').get(id=booth_id)
        data=data.bjpvote.using('bjp_db').all()
        # data = SaralBooth.objects.get(id=booth_id).bjpvote.all()
        data = data.order_by('election_year')
        data=data.values()


        return Response({'message': 'booth data', 'data': data}, status=200)


class UpdateVotes(views.APIView):

    def post(self, request):

        data=request.data
        id=data['id']
        value=data['value']

        BjpVotes.objects.using('bjp_db').filter(id=id).update(correction_in_vote_secured_by_bjp = value)


        return Response({'status': 'Success', 'message': 'Saved Successfully'}, status=200)


