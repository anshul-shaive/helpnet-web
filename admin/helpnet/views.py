from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect, HttpResponse
import json
from .models import person, req_made, loc
import requests
from django.contrib.auth.models import User
from django.http import JsonResponse

import math


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
        data = req_made.objects.all()
        
        reqsend = {
            "req_number": data
        }
        
        return render(request, 'helpnet/index.html', reqsend)



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
        req = req_made(req_type=req_type, status=status, user_id=user_id, username=username, req_time=req_time,
                       nprespond=nprespond,
                       location=location, auth_resp=auth_resp, presponded_ids=presponded_ids,
                       passigned_ids=passigned_ids)

        req.save()
        req_id = req.req_id
        # ob = req_made.objects.get(user_id=user_id,req_time=req_time)
        #
        # req_id = ob.req_id
        return HttpResponse(req_id)
    else:
        return render(request, "helpnet/index.html")


    


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


@csrf_exempt
def helpinfo(request):
    if request.method == 'POST':
        req_id = request.POST['req_id']

        ob = req_made.objects.get(req_id=str(req_id))

        presponded = ob.presponded_ids
        passigned = ob.passigned_ids
        resls=[]
        uloc=[]

        if presponded != "":
            presponded=presponded[:-1]
            resls=presponded.split(",")
            for uid in resls:
                ob = loc.objects.get(user_id=str(uid))
                res_loc = ob.last_loc
                uloc.append(str(uid)+"L"+str(res_loc))

            return HttpResponse(str(uloc))
        else:
             return HttpResponse("")
    else:
        return redirect('/admin')


@csrf_exempt
def update(request):
    if request.method == 'POST':
        user_id = request.POST['user_id']
        req_id = request.POST['req_id']

        ob = req_made.objects.get(req_id=str(req_id))
        req_made.objects.filter(req_id=str(req_id)).update(presponded_ids=ob.presponded_ids + user_id + ",")
        if(ob.nprespond==""):
            req_made.objects.filter(req_id=str(req_id)).update(nprespond="1")
        else:
            req_made.objects.filter(req_id=str(req_id)).update(nprespond=str(int(ob.nprespond) + 1))

    return HttpResponse("updated")


@csrf_exempt
def update_loc(request):
    if request.method == 'POST':
        user_id = request.POST['user_id']
        last_loc = request.POST['last_loc']

        lat_2 = float(last_loc.split(':')[0])
        lng_2 = float(last_loc.split(':')[1])

        lst = req_made.objects.values_list('req_id', 'location')
        # print(lst)

        rtype=[]
        final_lst = []
        for i in lst:
            location_req = i[1]
            ob = req_made.objects.get(req_id=i[0])
            lat_1 = float(location_req.split(':')[0])
            lng_1 = float(location_req.split(':')[1])

            diff_distance = get_distance(lat_1, lng_1, lat_2, lng_2)
            if (diff_distance <= 5):
                final_lst.append(i[0])
                rtype.append(str(ob.req_type)+"        " + str(round(diff_distance*1000,3))+"m away")
        # print(final_lst)

        actual_req = {}
        req = "request"
        count = 1
        for i in final_lst:
            val = list(req_made.objects.filter(req_id=i).values())[0]
            actual_req[req + str(count)] = val
            count = count + 1
        actual_req["rtypes"] = rtype

        if (loc.objects.filter(user_id=user_id).exists()):
            ob = loc.objects.get(user_id=str(user_id))
            loc.objects.filter(user_id=str(user_id)).update(last_loc=last_loc)
        else:
            locate = loc(user_id=user_id, last_loc=last_loc)
            locate.save()
    return HttpResponse(json.dumps(actual_req))


def get_distance(lat_1, lng_1, lat_2, lng_2):
    lat_1, lng_1, lat_2, lng_2 = map(math.radians, [lat_1, lng_1, lat_2, lng_2])
    d_lat = lat_2 - lat_1
    d_lng = lng_2 - lng_1

    temp = (
            math.sin(d_lat / 2) ** 2
            + math.cos(lat_1)
            * math.cos(lat_2)
            * math.sin(d_lng / 2) ** 2
    )

    return 6373.0 * (2 * math.atan2(math.sqrt(temp), math.sqrt(1 - temp)))



@csrf_exempt
def profile(request,user_id):
    data = person.objects.filter(user_id=user_id).values()
    context = {'data': data}
    return render(request,'helpnet/profile.html',context)

