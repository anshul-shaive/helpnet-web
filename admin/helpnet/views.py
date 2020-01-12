from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect,HttpResponse

from .models import person,req_made

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
    if User.objects.filter(username=username).exists():
      messages.error(request, 'That username is taken')
      return redirect('register')
    else:
      register = person(fullname=fullname,password=password,username=username, phone=phone, aadhar=aadhar, phelped=phelped, last_loc=last_loc, avg_rating=avg_rating,verified=verified)
      
      register.save()
      return HttpResponse("Saved")
  else:
    return redirect('/admin')



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
    # if User.objects.filter(username=username).exists():
    #   messages.error(request, 'That username is taken')
    #   return redirect('register')
    # else:
    req = req_made(req_type=req_type,status=status,username=username, req_time=req_time,nprespond=nprespond, location=location, auth_resp=auth_resp)
      
    req.save()
    return HttpResponse("Submitted")
  else:
    return redirect('/admin')



# def login(request):
#   if request.method == 'POST':
#     username = request.POST['username']
#     password = request.POST['password']

#     user = auth.authenticate(username=username, password=password)

#     if user is not None:
#       auth.login(request, user)
#       messages.success(request, 'You are now logged in')
#       return redirect('dashboard')
#     else:
#       messages.error(request, 'Invalid credentials')
#       return redirect('login')
#   else:
#     return render(request, 'accounts/login.html')

# def logout(request):
#   if request.method == 'POST':
#     auth.logout(request)
#     messages.success(request, 'You are now logged out')
#     return redirect('index')
#   else:
#     return redirect('/admin/')



