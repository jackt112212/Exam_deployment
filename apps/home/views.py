from django.shortcuts import render, redirect
from .models import *
import bcrypt
from django.contrib import messages

def index(request):
    return render(request, "home/index.html")

def register(request):
    errors = Traveler.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect("/") 
    elif request.POST['password'] == request.POST['confirm']:
        hashit = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        user = Traveler.objects.create(f_name=request.POST['f_name'], l_name=request.POST['l_name'], email=request.POST['email'], password=hashit.decode())
        request.session['user_id'] = user.id
        return redirect("/dashboard")        
    return redirect("/")

def login(request):
    user = Traveler.objects.get(email=request.POST['email'])
    if bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):
        request.session['user_id'] = user.id
        return redirect("/dashboard")
    else:
        error = {
            'login': "Log-in Failed",
        }
        messages.error(request, error)
        return redirect("/")

def logout(request):
    request.session['user_id']=None
    return redirect("/")

def dashboard(request):
    this_traveler = Traveler.objects.get(id=request.session['user_id'])
    context = {
        'other_trips': Trip.objects.exclude(followers=this_traveler),
        'user': this_traveler,
        'user_trips': this_traveler.group_trips.all(),
    }
    return render(request, 'home/dashboard.html', context)

def new_trip(request):
    context = {
        'user': Traveler.objects.get(id=request.session['user_id'])
    }
    return render(request, "home/new_trip.html", context)

def process_new_trip(request):
    errors = Trip.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect("/trips/new")
    else:
        this_traveler = Traveler.objects.get(id=request.session['user_id'])
        new_trip = Trip.objects.create(destination=request.POST['destination'], plan=request.POST['plan'], startdate=request.POST['startdate'], enddate=request.POST['enddate'], planner=this_traveler)
        new_trip.followers.add(this_traveler)
        return redirect("/dashboard")

def view_trip(request, trip_id):
    this_trip = Trip.objects.get(id=trip_id)
    context={
        'user': Traveler.objects.get(id=request.session['user_id']),
        "trip": this_trip,
        "followers": this_trip.followers.all(),
    }
    return render(request, "home/view.html", context)

def edit_trip(request, trip_id):
    this_trip = Trip.objects.get(id=trip_id)
    if this_trip.planner.id != request.session['user_id']:
        error = {
            'user': "This is not your trip",
        }
        messages.error(request, error)
        return redirect("/dashboard")
    
    context = {
        "trip": this_trip,
        "user": Traveler.objects.get(id=request.session['user_id']),
    }
    return render(request, "home/edit.html", context)

def process_edit_trip(request, trip_id):
    errors = Trip.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect("/trips/edit/" + trip_id)
    this_trip = Trip.objects.get(id=trip_id)
    this_trip.destination = request.POST['destination']
    this_trip.plan = request.POST['plan']
    this_trip.startdate = request.POST['startdate']
    this_trip.enddate = request.POST['enddate']
    this_trip.save()
    return redirect("/dashboard")
    
def join(request, trip_id):
    this_trip = Trip.objects.get(id=trip_id)
    this_user = Traveler.objects.get(id=request.session['user_id'])
    this_user.group_trips.add(this_trip)
    return redirect("/dashboard")

def remove(request, trip_id):
    delete_trip = Trip.objects.get(id=trip_id)
    delete_trip.delete()
    return redirect("/dashboard")

def cancel(request, trip_id):
    this_trip = Trip.objects.get(id=trip_id)
    this_user = Traveler.objects.get(id=request.session['user_id'])
    this_user.group_trips.remove(this_trip)
    return redirect("/dashboard")
