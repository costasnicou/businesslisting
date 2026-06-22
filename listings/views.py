from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect,JsonResponse
from django.shortcuts import render
from django.core.paginator import Paginator
from .models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
import datetime
from django.urls import reverse
from .models import *

# Create your views here.
data = []
page_obj=""

def generateListings(request,listings):
   
    # generate listings
    data = []
    for listing in listings:
        listing.featured_img = listing.business_images.filter(featured_img=True).first()
    
    for i in listings:
        data.append(i)

    return data

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
    data = businesses[start:end]






    if request.GET and not "submit-filter" in request.GET and "page" not in request.GET:
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


    if request.method == "GET":
        if "submit-filter" in request.GET or "page" in request.GET:
           
            if request.GET.get("category_select") != "none":
                option_category = request.GET.get("category_select")
               
                
            else:
                option_category = ""

            if request.GET.get("city_select") != "none":
                option_city = request.GET.get("city_select")
               

                
            else:
                option_city=""

            if option_category and option_city:
                # data = []
                businesses = Business.objects.filter(category=option_category,city=option_city)
                data = generateListings(request,businesses)
                # paginator
                paginator = Paginator(data, 9) #Show 9 per page.
                page_number = request.GET.get('page')
                page_obj = paginator.get_page(page_number)
 
                return render(request, "listings/all-listings.html",{
                    "cities":cities,
                    "categories":categories,
                    "page_obj":page_obj,
                    
                })



                
            elif option_category and option_category != "" and option_city=="":
                businesses = Business.objects.filter(category=option_category)
                data = generateListings(request,businesses)
                # paginator
                paginator = Paginator(data, 9) # Show 9 per page.
                page_number = request.GET.get('page')
                page_obj = paginator.get_page(page_number)

              
                return render(request, "listings/all-listings.html",{
                    "cities":cities,
                    "categories":categories,
                    "page_obj":page_obj,
                   
                })
               
                 
            elif option_city and option_city != "" and option_category=="":
                businesses = Business.objects.filter(city=option_city)
                data = generateListings(request,businesses)   
                # paginator
                paginator = Paginator(data, 9) # Show 9 per page.
                page_number = request.GET.get('page')
                page_obj = paginator.get_page(page_number)

                return render(request, "listings/all-listings.html",{
                    "cities":cities,
                    "categories":categories,
                    "page_obj":page_obj,
                    
                })

            elif not option_city and not option_category:
                return HttpResponseRedirect("all-listings")
               


    return render(request, "listings/all-listings.html",{
        "cities":cities,
        "categories":categories,
        "businesses":data,
    })

def category(request,cat_name):

    cities = City.objects.all()
    categories =  BusinessCategory.objects.all()
    category = BusinessCategory.objects.get(cat_name=cat_name)
    businesses = category.businesses_by_category.all()
  
    # start and end of  listings
    start = int(request.GET.get("start") or 0)
    end = int(request.GET.get("end") or (start +9))
  
    # generate listings
    data = []
    for business in businesses:
        business.featured_img = business.business_images.filter(featured_img=True).first()

   
    data = businesses[start:end]
    
    if request.GET and not "submit-filter" in request.GET and "page" not in request.GET:
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


    if request.method == "GET":
        if "submit-filter" in request.GET or "page" in request.GET:
             
            if request.GET.get("city_select") != "none":
                option_city = request.GET.get("city_select")
                
            else:
                option_city=""

            if option_city:
                
                # businesses = Business.objects.filter(category=option_category)
                category = BusinessCategory.objects.get(cat_name=cat_name)
                
                businesses = category.businesses_by_category.filter(city=option_city)

                

                data = generateListings(request,businesses)
                # paginator
                paginator = Paginator(data, 9) #Show 9 per page.
                page_number = request.GET.get('page')
                page_obj = paginator.get_page(page_number)
 
                return render(request, "listings/category.html",{
                    "cities":cities,
                    "categories":categories,
                    "category":category,
                    "page_obj":page_obj,
                    
                })

            elif not option_city:
                return HttpResponseRedirect(reverse('category', kwargs={'cat_name': category}))

    return render(request, "listings/category.html",{
        "cities":cities,
        "categories":categories,
        "category":category,
        "businesses":data,
       
    })

def city(request,city_name):

    cities = City.objects.all()
    categories =  BusinessCategory.objects.all()
    city = City.objects.get(city_name=city_name)
    businesses = city.businesses_by_city.all()

    start = int(request.GET.get("start") or 0)
    end = int(request.GET.get("end") or (start +9))

    # generate listings
    data = []
    for business in businesses:
        business.featured_img = business.business_images.filter(featured_img=True).first()
    data = businesses[start:end]

    if request.GET and not "submit-filter" in request.GET and "page" not in request.GET:
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

    if request.method == "GET":
        if "submit-filter" in request.GET or "page" in request.GET:
             
            if request.GET.get("category_select") != "none":
                option_category = request.GET.get("category_select")           
                
            else:
                option_category = ""
                
            if option_category:
                
                # businesses = Business.objects.filter(category=option_category)
                city = City.objects.get(city_name=city_name)
                
                businesses = city.businesses_by_city.filter(category=option_category)

                

                data = generateListings(request,businesses)
                # paginator
                paginator = Paginator(data, 9) #Show 9 per page.
                page_number = request.GET.get('page')
                page_obj = paginator.get_page(page_number)
 
                return render(request, "listings/city.html",{
                    "cities":cities,
                    "categories":categories,
                    "city":city,
                    "page_obj":page_obj,
                    
                })

            elif not option_city:
                return HttpResponseRedirect(reverse('city', kwargs={'city_name': city}))

    return render(request, "listings/city.html",{
        "cities":cities,
        "city":city,
        "categories":categories,
        "category":category,
        "businesses":data,
       
    })

    
def singlelisting(request,business_name):
    cities = City.objects.all()
    categories =  BusinessCategory.objects.all()

    business = Business.objects.get(name=business_name)
    business.featured_img = business.business_images.filter(featured_img=True).first()
    print(business.name)
    return render(request, "listings/singlelisting.html",{
        "cities":cities,
        "categories":categories,
        "business":business,
           
    })
    
