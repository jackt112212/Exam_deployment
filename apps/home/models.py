from django.db import models
from django.utils.dateparse import parse_date
import re
import datetime
import bcrypt
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+-_]+@[a-zA-Z0-9_-]+\.[a-zA-Z]+$')

class travelerManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if len(postData['f_name'])<2:
            errors['f_name'] = "First name should have at least 2 characters"
        if len(postData['l_name'])<2:
            errors['l_name'] = "Last name should have at least 2 characters"
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Invalid Email Address"
        elif len(Traveler.objects.filter(email=postData['email'])) > 0:
            errors['email'] = "Email already in use( Did you forget your password?)"
        if len(postData['password']) < 6:
            errors['password'] = "Invalid Password"
        return errors

class tripManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        print("the value is:" + postData['destination'])
        if len(postData['destination'])<2:
            errors['destination'] = "Destination should have at least 2 characters"
        if len(postData['plan'])<5:
            errors['plan'] = "Plan should have at least 5 characters"
        
        if len(postData['startdate']) > 0 and len(postData['enddate']) > 0:
            if datetime.date.today() > parse_date(postData['startdate']):
                errors['startdate'] = "Start date has to be in the future"
            if parse_date(postData['enddate']) < parse_date(postData['startdate']):
                errors['enddate'] = "End date has to be after start date"
        else:
            errors['dates'] = "you haven't selected a start date or an end date"
        return errors

class Traveler(models.Model):
    f_name = models.CharField(max_length=45)
    l_name = models.CharField(max_length=45)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = travelerManager()

class Trip(models.Model):
    destination = models.CharField(max_length=45)
    plan = models.TextField(null=True)
    startdate = models.DateField()
    enddate = models.DateField()
    planner = models.ForeignKey(Traveler, related_name="my_trips")
    followers = models.ManyToManyField(Traveler, related_name="group_trips")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = tripManager()

