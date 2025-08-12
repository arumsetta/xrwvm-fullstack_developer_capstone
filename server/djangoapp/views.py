# Uncomment the required imports before adding the code

from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import logout
from django.contrib import messages
from datetime import datetime

from django.http import JsonResponse
from django.contrib.auth import login, authenticate
import logging
import json
from django.views.decorators.csrf import csrf_exempt
from .populate import initiate
from .models import CarMake, CarModel
from .models import Dealership  
from .models import Review 
from .populate import initiate

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.

# Create a `login_request` view to handle sign in request
@csrf_exempt
def login_user(request):
    # Get username and password from request.POST dictionary
    data = json.loads(request.body)
    username = data['userName']
    password = data['password']
    # Try to check if provide credential can be authenticated
    user = authenticate(username=username, password=password)
    data = {"userName": username}
    if user is not None:
        # If user is valid, call login method to login current user
        login(request, user)
        data = {"userName": username, "status": "Authenticated"}
    return JsonResponse(data)

# Create a `logout_request` view to handle sign out request
# def logout_request(request):
def logout_user(request):
    logout(request)  # Terminate the user session
    data = {"userName": ""}  # Return empty username
    return JsonResponse(data)

# Create a `registration` view to handle sign up request
@csrf_exempt
def registration(request):
    context = {}

    # Load JSON data from the request body
    data = json.loads(request.body)
    username = data['userName']
    password = data['password']
    first_name = data['firstName']
    last_name = data['lastName']
    email = data['email']
    username_exist = False
    email_exist = False
    try:
        # Check if user already exists
        User.objects.get(username=username)
        username_exist = True
    except:
        # If not, simply log this is a new user
        logger.debug("{} is new user".format(username))

    # If it is a new user
    if not username_exist:
        # Create user in auth_user table
        user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,password=password, email=email)
        # Login the user and redirect to list page
        login(request, user)
        data = {"userName":username,"status":"Authenticated"}
        return JsonResponse(data)
    else :
        data = {"userName":username,"error":"Already Registered"}
        return JsonResponse(data)

# # Update the `get_dealerships` view to render the index page with
# a list of dealerships
# def get_dealerships(request):
def get_dealerships(request):
    dealerships = Dealership.objects.all()
    dealerships_list = [{
        "id": dealer.id,
        "name": dealer.name,
        "full_name": dealer.name,
        "city": dealer.city,
        "address": dealer.address,
        "zip": dealer.zip,
        "state": dealer.state
    } for dealer in dealerships]
    return JsonResponse({"dealerships": dealerships_list})


# Create a `get_dealer_reviews` view to render the reviews of a dealer
# def get_dealer_reviews(request,dealer_id):
def get_dealer_reviews(request, dealer_id):
    try:
        reviews = Review.objects.filter(dealership=dealer_id)
        reviews_list = [{
            "id": review.id,
            "name": review.name,
            "review": review.review,
            "purchase": review.purchase,
            "purchase_date": review.purchase_date,
            "car_make": review.car_make,
            "car_model": review.car_model,
            "car_year": review.car_year,
            "sentiment": "neutral"  # You might want to add sentiment analysis
        } for review in reviews]
        return JsonResponse({"reviews": reviews_list})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
# Create a `add_review` view to submit a review
# def add_review(request):
# ...
@csrf_exempt
def add_review(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            review = Review.objects.create(
                dealership_id=data['dealership'],
                name=data['name'],
                review=data['review'],
                purchase=data.get('purchase', False),
                purchase_date=data.get('purchase_date'),
                car_make=data.get('car_make'),
                car_model=data.get('car_model'),
                car_year=data.get('car_year')
            )
            return JsonResponse({"status": "success", "review_id": review.id})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Invalid request method"}, status=405)

# Create a `get_dealer_details` view to render the dealer details
# def get_dealer_details(request, dealer_id):
def get_dealer_details(request, dealer_id):
    try:
        dealer = Dealership.objects.get(id=dealer_id)
        dealer_data = {
            "id": dealer.id,
            "name": dealer.name,
            "city": dealer.city,
            "address": dealer.address,
            "zip": dealer.zip,
            "state": dealer.state
        }
        return JsonResponse(dealer_data)
    except Dealership.DoesNotExist:
        return JsonResponse({"error": "Dealer not found"}, status=404)




def get_cars(request):
    count = CarMake.objects.count()
    print(f"[DEBUG] CarMake count before initiate(): {count}")
    if count == 0:
        print("[DEBUG] Calling initiate() to populate the database")
        initiate()
    car_models = CarModel.objects.select_related('car_make')
    print(f"[DEBUG] Number of CarModel objects after initiate(): {car_models.count()}")
    cars = []
    for car_model in car_models:
        print(f"[DEBUG] CarModel: {car_model.name}, CarMake: {car_model.car_make.name}")
        cars.append({"CarModel": car_model.name, "CarMake": car_model.car_make.name})
    return JsonResponse({"CarModels": cars})
