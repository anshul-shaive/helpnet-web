from django.urls import path

from . import views

urlpatterns = [
    path('',views.register,name='register'),
    #path('login/',view.login,name='login'),
    #path('logout/',view.logout,name='logout'),
    path('request/',views.req, name='request'),

]