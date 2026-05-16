from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from .forms import BusinessHoursAdminForm

from .models import (
    User,
    City,
    BusinessCategory,
    Business,
    BusinessSocial,
    BusinessReview,
    BusinessImage,
    BusinessHours,
    BusinessPartnerRequest
)
@admin.register(BusinessHours)
class BusinessHoursAdmin(admin.ModelAdmin):

    form = BusinessHoursAdminForm

    list_display = [
        "business",
        "day",
        "open_time",
        "close_time"
    ]

    list_filter = [
        "day"
    ]

# =========================================================
# INLINE MODELS
# =========================================================

class BusinessSocialInline(admin.TabularInline):
    model = BusinessSocial
    extra = 1


class BusinessHoursInline(admin.TabularInline):
    model = BusinessHours
    form = BusinessHoursAdminForm
    extra = 1
class BusinessImageInline(admin.TabularInline):
    model = BusinessImage
    extra = 1

    readonly_fields = ["image_preview"]

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="120" style="border-radius:8px;" />',
                obj.image.url
            )
        return "No Image"

    image_preview.short_description = "Preview"


# =========================================================
# USER ADMIN
# =========================================================

@admin.register(User)
class UserAdmin(BaseUserAdmin):

    search_fields = [
        "username",
        "email",
        "first_name",
        "last_name"
    ]


# =========================================================
# CITY ADMIN
# =========================================================

@admin.register(City)
class CityAdmin(admin.ModelAdmin):

    list_display = [
        "city_name",
        "city_image_preview"
    ]

    search_fields = [
        "city_name"
    ]

    readonly_fields = [
        "city_image_preview"
    ]

    fields = [
        "city_name",
        "city_photo",
        "city_image_preview"
    ]

    def city_image_preview(self, obj):
        if obj.city_photo:
            return format_html(
                '<img src="{}" width="150" style="border-radius:10px;" />',
                obj.city_photo.url
            )
        return "No Image"

    city_image_preview.short_description = "Preview"


# =========================================================
# CATEGORY ADMIN
# =========================================================

@admin.register(BusinessCategory)
class BusinessCategoryAdmin(admin.ModelAdmin):

    list_display = [
        "cat_name",
        "featured",
        "category_image_preview"
    ]

    list_filter = [
        "featured"
    ]

    search_fields = [
        "cat_name"
    ]

    readonly_fields = [
        "category_image_preview"
    ]

    fields = [
        "cat_name",
        "featured",
        "cat_photo",
        "category_image_preview"
    ]

    def category_image_preview(self, obj):
        if obj.cat_photo:
            return format_html(
                '<img src="{}" width="150" style="border-radius:10px;" />',
                obj.cat_photo.url
            )
        return "No Image"

    category_image_preview.short_description = "Preview"


# =========================================================
# BUSINESS ADMIN
# =========================================================

@admin.register(Business)
class BusinessAdmin(admin.ModelAdmin):

    list_display = [
        "name",
        "city",
        "category",
        "featured",
        "phone",
        "email"
    ]

    list_filter = [
        "featured",
        "city",
        "category"
    ]

    search_fields = [
        "name",
        "address",
        "phone",
        "email"
    ]

    autocomplete_fields = [
        "user",
        "city",
        "category",
        "partners"
    ]

    filter_horizontal = [
        "partners"
    ]

    fieldsets = (

        ("Business Information", {
            "fields": (
                "user",
                "name",
                "desc",
                "featured"
            )
        }),

        ("Category & Location", {
            "fields": (
                "category",
                "city",
                "address"
            )
        }),

        ("Contact Information", {
            "fields": (
                "phone",
                "email"
            )
        }),

        ("Partners", {
            "fields": (
                "partners",
            )
        }),
    )

    inlines = [
        BusinessSocialInline,
        BusinessHoursInline,
        BusinessImageInline
    ]


# =========================================================
# REVIEW ADMIN
# =========================================================

@admin.register(BusinessReview)
class BusinessReviewAdmin(admin.ModelAdmin):

    list_display = [
        "business",
        "user",
        "stars",
        "creation_time"
    ]

    list_filter = [
        "stars",
        "creation_time"
    ]

    search_fields = [
        "business__name",
        "user__username"
    ]

    readonly_fields = [
        "creation_time"
    ]


# =========================================================
# PARTNER REQUEST ADMIN
# =========================================================

@admin.register(BusinessPartnerRequest)
class BusinessPartnerRequestAdmin(admin.ModelAdmin):

    list_display = [
        "from_business",
        "to_business",
        "status",
        "creation_time"
    ]

    list_filter = [
        "status",
        "creation_time"
    ]

    search_fields = [
        "from_business__name",
        "to_business__name"
    ]

    readonly_fields = [
        "creation_time"
    ]


# =========================================================
# ADMIN BRANDING
# =========================================================

admin.site.site_header = "Business Directory Admin"
admin.site.site_title = "Business Directory"
admin.site.index_title = "Administration"