from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect,JsonResponse
from django.shortcuts import render
from .models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
import datetime
from django.urls import reverse
from .models import *
# Create your views here.

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "listings/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        cities = City.objects.all()
        categories =  BusinessCategory.objects.all()
        return render(request, "listings/login.html",{
            "cities":cities,
            "categories":categories,
        })


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "listings/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "listings/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        cities = City.objects.all()
        categories =  BusinessCategory.objects.all()
        return render(request, "listings/register.html",{
            "cities":cities,
            "categories":categories
        })


def index(request):
    cities = City.objects.all()
    categories =  BusinessCategory.objects.all()
    featured_categories = BusinessCategory.objects.filter(featured=True)
    featured_businesses = Business.objects.filter(featured=True)
    for featured_business in featured_businesses:
        featured_business.featured_img = featured_business.business_images.filter(featured_img=True).first()




    return render(request, "listings/homepage.html",{
        "cities":cities,
        "categories":categories,
        "featured_categories":featured_categories,
        "featured_businesses":featured_businesses,
    })


def all_listings(request):
    cities = City.objects.all()
    categories =  BusinessCategory.objects.all()
    businesses = Business.objects.all()


    # start and end of  listings
    start = int(request.GET.get("start") or 0)
    end = int(request.GET.get("end") or (start +9))

    # generate listings
    data = []
    for business in businesses:
        business.featured_img = business.business_images.filter(featured_img=True).first()
    for i in range(start,end):
        data.append(businesses[i])
    # print(data)
    if request.GET:
       # Return list of posts
        return JsonResponse({
            "businesses": [
                {
                    "id": business.id,
                    "title": business.name,
                    "desc": business.desc,
                    "city": business.city.city_name if business.city else None,
                    "category": business.category.cat_name if business.category else None,
                    "cat_photo":business.category.cat_photo.url
                        if business.category.cat_photo
                        else None,
                    "img": business.featured_img.image.url
                        if business.featured_img and business.featured_img.image
                        else None,
                    "phone":business.phone,
                }
                for business in data
            ]
        })

    return render(request, "listings/all-listings.html",{
        "cities":cities,
        "categories":categories,
        "businesses":data,
    })