from django.urls import path

from . import views

urlpatterns = [

    path('', views.register, name='register'),
    path('login', views.login, name='login'),
    path('request', views.req, name='request'),
    path('update', views.update, name='update'),
    path('loc',views.update_loc, name='update_loc')
]
