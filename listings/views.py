from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect,JsonResponse
from django.shortcuts import render,redirect
from django.core.paginator import Paginator
from .models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
import datetime
from django.urls import reverse
from .models import *
from django.db.models import Avg
# Create your views here.
data = []
page_obj=""

def generateListings(request,listings):
   
    # generate listings
    data = []
    for listing in listings:
        listing.featured_img = listing.business_images.filter(featured_img=True).first()
        listing.reviews_count = listing.business_reviews.all().count()
        listing.reviews_stars_avg = int(round(listing.business_reviews.aggregate(
            avg=Avg("stars")
        )["avg"] or 0))
        listing.stars_range = range(listing.reviews_stars_avg)
    
    for i in listings:
        data.append(i)

    return data

def search(request):
    businesses = Business.objects.all()
    business_names = [business.name for business in businesses]
    qr = ""
    qarr=[]
    # print(business_names)
    if request.GET["search"]:
        qr=request.GET["search"]

    if qr in business_names:
        return redirect("singlelisting",business_name=qr)
    else:
        for business_name in business_names:
            if qr in business_name:
                business = Business.objects.get(name=business_name)
                business.featured_img = business.business_images.filter(featured_img=True).first()
                business.reviews_count = business.business_reviews.all().count()
                business.reviews_stars_avg = int(round(business.business_reviews.aggregate(
                    avg=Avg("stars")
                )["avg"] or 0))
                business.stars_range = range(business.reviews_stars_avg)
                qarr.append(business)
    
   
    return render(request,"listings/search.html",{
        "qarr":qarr,
    })




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
        featured_business.reviews_count = featured_business.business_reviews.all().count()
        featured_business.reviews_stars_avg = int(round(featured_business.business_reviews.aggregate(
            avg=Avg("stars")
        )["avg"] or 0))
        featured_business.stars_range = range(featured_business.reviews_stars_avg)

    return render(request, "listings/homepage.html",{
        "cities":cities,
        "categories":categories,
        "featured_categories":featured_categories,
        "featured_businesses":featured_businesses,
        # "reviews_count":reviews_count,
        # # "reviews_stars_avg":reviews_stars_avg,
        # "stars_range": range(reviews_stars_avg),
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
        business.reviews_count = business.business_reviews.all().count()
        business.reviews_stars_avg = int(round(business.business_reviews.aggregate(
            avg=Avg("stars")
        )["avg"] or 0))
        business.stars_range = range(business.reviews_stars_avg)
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
                    "reviews_count": business.reviews_count
                     if business.reviews_count
                        else None,
                    "reviews_stars_avg":business.reviews_stars_avg
                    if business.reviews_stars_avg
                        else None,
                }
                for business in data

            ],
          
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
        "businesseslength":len(businesses),
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
        business.reviews_count = business.business_reviews.all().count()
        business.reviews_stars_avg = int(round(business.business_reviews.aggregate(
            avg=Avg("stars")
        )["avg"] or 0))
        business.stars_range = range(business.reviews_stars_avg)

   
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
                    "reviews_count": business.reviews_count
                     if business.reviews_count
                        else None,
                    "reviews_stars_avg":business.reviews_stars_avg
                    if business.reviews_stars_avg
                        else None,
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
        "businesseslength":len(businesses),
       
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
        business.reviews_count = business.business_reviews.all().count()
        business.reviews_stars_avg = int(round(business.business_reviews.aggregate(
            avg=Avg("stars")
        )["avg"] or 0))
        business.stars_range = range(business.reviews_stars_avg)

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
                    "reviews_count": business.reviews_count
                    if business.reviews_count
                        else None,
                    "reviews_stars_avg":business.reviews_stars_avg
                    if business.reviews_stars_avg
                        else None,
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

            elif not option_category:
                return HttpResponseRedirect(reverse('city', kwargs={'city_name': city}))

    return render(request, "listings/city.html",{
        "cities":cities,
        "city":city,
        "categories":categories,
        "category":category,
        "businesses":data,
        "businesseslength":len(businesses),
       
    })

    
def singlelisting(request,business_name):
    cities = City.objects.all()
    categories =  BusinessCategory.objects.all()

    business = Business.objects.get(name=business_name)
    business.featured_img = business.business_images.filter(featured_img=True).first()
    gallery = business.business_images.filter(featured_img=False)[0:4]
    reviews_count = business.business_reviews.all().count()
    reviews_stars_avg = int(round(business.business_reviews.aggregate(
        avg=Avg("stars")
    )["avg"] or 0))
    
    social = business.business_social_links.all()
    hours = business.hours.all()
    partners = business.partners.all()
    partners_range = ""
    if partners.exists():
        for partner in partners:
            partner.featured_img = partner.business_images.filter(featured_img=True).first()
            partner.reviews_count = partner.business_reviews.all().count()
            partner.reviews_stars_avg = int(round(partner.business_reviews.aggregate(
                avg=Avg("stars")
            )["avg"] or 0))
            partners_range = partner.reviews_stars_avg
    else:
        partners_range = 0


    business_reviews = business.business_reviews.all()

    
    
    
    # .featured_img = business.business_images.filter(featured_img=True).first()
    print(partners)
    return render(request, "listings/singlelisting.html",{
        "cities":cities,
        "categories":categories,
        "business":business,
        "gallery":gallery,
        "reviews_count":reviews_count,
        "reviews_stars_avg":reviews_stars_avg,
        "stars_range": range(reviews_stars_avg),
        "partner_stars_range": range(partners_range),
        "social":social,
        "hours":hours,
        "partners":partners,
        "business_reviews":business_reviews,
           
    })
    
