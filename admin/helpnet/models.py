from django.db import models
from datetime import datetime


class person (models.Model):
    user_id = models.AutoField(primary_key=True,)
    fullname = models.CharField(max_length=200)
    password = models.CharField(max_length=20)
    username = models.CharField(max_length=200, null=True, blank=True)
    photo = models.ImageField(upload_to='media/%Y/%m/%d/', null=True, blank=True)
    phone = models.CharField(max_length=20,unique=True)
    verified = models.CharField(default=False, max_length=6)
    aadhar = models.CharField(max_length=20)
    phelped = models.CharField(null=True, default=0, blank=True, max_length=5)
    last_loc = models.CharField(max_length=200, null=True, blank=True)
    avg_rating = models.CharField(null=True, default=0, blank=True, max_length=5)

    def __str__(self):
        return "reg"


class req_made(models.Model):
    # user_id = models.ForeignKey(person, on_delete=models.DO_NOTHING,related_name='uid', null=True, blank=True)
    user_id = models.CharField(max_length=200)
    presponded_ids = models.TextField(null=True, blank=True)
    passigned_ids = models.TextField(null=True, blank=True)
    req_id = models.AutoField(primary_key=True)
    req_type = models.CharField(max_length=200)
    status = models.CharField(max_length=20)
    username = models.CharField(max_length=200, null=True, blank=True)
    req_time = models.CharField(max_length=6)
    location = models.CharField(max_length=20)
    nprespond = models.CharField(null=True, default=0, blank=True, max_length=5)
    auth_resp = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return "ad"
