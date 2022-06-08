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
from .models import Voter,SaralBooth,BjpVotes,Ac,State
from rest_framework.views import APIView
from django.core import serializers
import json
from django.views import View
from django.shortcuts import render, HttpResponse, redirect
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework import mixins, viewsets, views


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

# class GetVotes(views.APIView):
#
#     def get(self,request):
#
#         booth_id = request.query_params.get('booth_id')
#         data = SaralBooth.objects.using('bjp_db').get(id=booth_id)
#         data=data.bjpvote.using('bjp_db').all()
#         # data = SaralBooth.objects.get(id=booth_id).bjpvote.all()
#         data = data.order_by('election_year')
#         data=data.values()
#
#
#         return Response({'message': 'booth data', 'data': data}, status=200)

from itertools import groupby

class GetVotes(views.APIView):

    def get(self,request):
        state=request.query_params.get('state')
        ac=request.query_params.get('ac')
        booth_id = request.query_params.get('booth_id')

        if booth_id:
            try:
                data = SaralBooth.objects.using('bjp_db').get(id=booth_id)

                data = data.bjpvote.using('bjp_db').all()
                data = data.order_by('-election_year')
                boot_wise_votes = data.values()
                # print(data)
                voters=SaralBooth.objects.using('bjp_db').filter(id=booth_id)
                voters=voters.values()
                voters=voters[0]['current_voters']
                total_voter = {
                    "id":0,
                    "text": "Total voters",
                    "votes": voters
                }
                result = []
                result.append(total_voter)
                for booth in boot_wise_votes:
                    year = booth['election_year']
                    election_type = booth['election_type']
                    temp_obj = {
                        "id":  booth['id'],
                        "text": ('Total Number of votes obtained by BJP in {} {}'.format(year, election_type)),
                        "votes": booth["vote_ssecured_by_bjp"],
                        "corrected_votes": booth["corrected_votes"]
                    }
                    result.append(temp_obj)

                return Response({'message': 'booth data', 'data': result}, status=200)
            except Exception as e:
                dict=[]
                return Response({'message': 'No Data Available', 'data': dict}, status=200)



        elif state and ac:

            data = BjpVotes.objects.using('bjp_db').raw(
                'SELECT * FROM "bjp_votes" INNER JOIN "saral_booth" ON "saral_booth"."id" = "bjp_votes"."booth_id" WHERE "saral_booth"."state"=%s AND "saral_booth"."ac"=%s ORDER BY "bjp_votes"."booth_id","bjp_votes"."election_year"',
                [state, ac])

            queryset = serializers.serialize('json', data)

            json_object = json.loads(queryset)

            for i in json_object:
                i.pop('model')


            for j in json_object:
                for k,v in j['fields'].items():
                    j[k]=v
                j.pop('fields')

            data = sorted(json_object, key=lambda d: d['booth'])
        else:
            return Response({'message': 'Give valid details'}, status=200)

        return Response({'message': 'booth data', 'data': data}, status=200)


class UpdateVotes(views.APIView):

    def post(self, request):


        data = request.data

        if 'id' in data:
            id = data['id']
            if len(id)==0:
                if 'booth_id' in data:
                    booth_id = data['booth_id']
                    if len(booth_id)==0:
                        return Response({'message': 'booth_id or Id is required'}, status=400)

                else:
                    id=None

        else:
            id=None
        if 'value' in data:
            value = data['value']
            if len(value)==0:
                value=None
        else:
            value=None
        if 'type' in data:
            ty = data['type']
            if len(ty)==0:
                ty=None
        else:
            ty=None


        if id==None or value==None or ty==None:
            if id == None and value == None and ty == None:
                return Response({'message': 'Id, Value and Type are required'}, status=400)
            if id == None and value == None and ty != None:
                return Response({'message': 'Id and Value are required'}, status=400)
            if id == None and value != None and ty == None:
                return Response({'message': 'Id and Type are required'}, status=400)
            if id != None and value == None and ty == None:
                return Response({'message': 'Value and Type are required'}, status=400)
            if id != None and value != None and ty == None:
                return Response({'message': 'Type is required'}, status=400)
            if id != None and value == None and ty != None:
                return Response({'message': 'Value is required'}, status=400)
            if id == None and value != None and ty != None:
                return Response({'message': 'Id is required'}, status=400)

        if len(id)==0:
            BjpVotes.objects.using('bjp_db').create(booth_id=booth_id,election_year=2024,election_type='Loksabha Election',corrected_votes=value)
        elif ty.casefold()=='votes'.casefold():
            BjpVotes.objects.using('bjp_db').filter(id=id).update(corrected_votes=value)
        elif ty.casefold()=='voters'.casefold():
            SaralBooth.objects.using('bjp_db').filter(id=id).update(corrected_voters=value)


        return Response({'status': 'Success', 'message': 'Saved Successfully'}, status=200)





class Home(View):
    def get(self,request):
        states=State.objects.using('gcp_db').all()
        return render(request, 'app/home.html', {'states':states})

def modules(request):
    course = request.GET.get('course')
    print(course)
    id=State.objects.using('gcp_db').get(name=course)
    modules = Ac.objects.using('gcp_db').filter(country_state=id)
    modules=modules.order_by('number')

    print(modules)
    context = {'modules': modules}
    return render(request, 'app/modules.html', context)




from google.cloud import storage

class send_files(views.APIView):

    def post(self, request):
        state = request.POST.get("course")
        ac = request.POST.get("custom-select")
        myfile = request.FILES.getlist("uploadfiles")

        storage_client = storage.Client.from_service_account_json('/home/this/Downloads/bjp-saral-039039e1a469.json')
        bucket = storage_client.get_bucket('public-saral')

        for f in myfile:
            filename = "%s/%s/%s" % (state, ac, f)
            blob = bucket.blob(filename)
            blob.upload_from_file(f)


        print('Uploaded Successfully')

        return redirect("http://127.0.0.1:8000/")




