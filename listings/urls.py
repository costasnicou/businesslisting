from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("register", views.register, name="register"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("all-listings", views.all_listings, name="all_listings"),
    path("category/<str:cat_name>",views.category, name="category"),
    path("city/<str:city_name>",views.city, name="city"),
    path("business/<str:business_name>",views.singlelisting, name="singlelisting"),
    path("search/",views.search,name="search"),
]