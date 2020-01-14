from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect, HttpResponse
import json
from .models import person, req_made
import requests
from django.contrib.auth.models import User
from django.http import JsonResponse


@csrf_exempt
def register(request):
    if request.method == 'POST':
        fullname = request.POST['fullname']
        password = request.POST['password']
        username = request.POST['username']
        phone = request.POST['phone']
        aadhar = request.POST['aadhar']
        phelped = request.POST['phelped']
        last_loc = request.POST['last_loc']
        avg_rating = request.POST['avg_rating']
        verified = request.POST['verified']
        if person.objects.filter(phone=phone).exists():
            messages.error(request, 'That phone.no is taken')
            # return redirect('register')
            return HttpResponse("Mobile Number already exists")

        else:
            register = person(fullname=fullname, password=password, username=username, phone=phone, aadhar=aadhar,
                              phelped=phelped, last_loc=last_loc, avg_rating=avg_rating, verified=verified)

            register.save()
            return HttpResponse("Registered")
    else:
        return redirect('/admin')

#
# def send_otp(request):
#     response_data = {}
#     if request.method == "POST":
#         user_phone = request.POST['phone_number']
#         url = "http://2factor.in/API/V1/293832-67745-11e5-88de-5600000c6b13/SMS/" + user_phone + "/AUTOGEN/OTPSEND"
#         response = requests.request("GET", url)
#         data = response.json()
#         request.session['otp_session_data'] = data['Details']
#         # otp_session_data is stored in session.
#         response_data = {'Message': 'Success'}
#     else:
#         response_data = {'Message': 'Failed'}
#     return JsonResponse(response_data)
#
#
# def otp_verification(request):
#     response_data = {}
#     if request.method == "POST" :
#         user_otp = request.POST['otp']
#         url = "http://2factor.in/API/V1/293832-67745-11e5-88de-5600000c6b13/SMS/VERIFY/" + request.session['otp_session_data'] + "/" + user_otp + ""
#
#         # otp_session_data is fetched from session.
#         response = requests.request("GET", url)
#         data = response.json()
#         if data['Status'] == "Success":
#             logged_user.is_active = True
#             response_data = {'Message': 'Success'}
#         else:
#             response_data = {'Message': 'Failed'}
#             logout(request)
#     return JsonResponse(response_data)
#

@csrf_exempt
def req(request):
    if request.method == 'POST':
        req_type = request.POST['req_type']
        status = request.POST['status']
        username = request.POST['username']
        req_time = request.POST['req_time']
        location = request.POST['location']
        nprespond = request.POST['nprespond']
        auth_resp = request.POST['auth_resp']
        user_id = request.POST['user_id']
        presponded_ids = request.POST['presponded_ids']
        passigned_ids = request.POST['passigned_ids']

        # if User.objects.filter(username=username).exists():
        #   messages.error(request, 'That username is taken')
        #   return redirect('register')
        # else:
        req = req_made(req_type=req_type, status=status,user_id= user_id, username=username, req_time=req_time, nprespond=nprespond,
                       location=location, auth_resp=auth_resp)

        req.save()
        return HttpResponse("Submitted")
    else:
        return redirect('/admin')


@csrf_exempt
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        ob = person.objects.get(phone=str(username))

        actual_pass = ob.password
        if actual_pass == password:
            return HttpResponse(json.dumps({'status': 'verified', 'user_id': '{uid}'.format(uid=ob.user_id)}))
        else:
            return HttpResponse("Wrong Password")
    else:
        return redirect('/admin')
