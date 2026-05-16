from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

# Create your models here.
class User(AbstractUser):
    pass


class City(models.Model):
    city_name = models.CharField(max_length=255)
    city_photo = models.ImageField(upload_to="city_images",null=True,blank=True)
    def __str__(self):
        return self.city_name

class BusinessCategory(models.Model):
    cat_name = models.CharField(max_length=255)
    cat_photo = models.ImageField(upload_to="cat_images",null=True,blank=True)
    featured = models.BooleanField(default=False)
    def __str__(self):
        return self.cat_name

class Business(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    name = models.CharField(max_length=200,blank=False)
    desc = models.TextField(blank=False)
    city = models.ForeignKey(City,on_delete=models.CASCADE,related_name="businesses_by_city")
    category = models.ForeignKey(BusinessCategory,on_delete=models.CASCADE,related_name="businesses_by_city")
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    featured = models.BooleanField(default=False)
    partners = models.ManyToManyField(
        "self",
        symmetrical=True,
        blank=True
    )
    # use for map location
    address = models.CharField(max_length=255)
    

    def __str__(self):
        return self.name


class BusinessSocial(models.Model):
    platform = [
        ('facebook', 'Facebook'),
        ('instagram', 'Instagram'),
        ('linkedin', 'LinkedIn'),
        ('x', 'X'),
        ('youtube', 'YouTube'),
        ('tiktok', 'TikTok'),
    ]
    business = models.ForeignKey(
        Business,
        on_delete=models.CASCADE,
        related_name='business_social_links'
    )
    network = models.CharField(
        max_length=20,
        choices=platform,
    )
    url = models.URLField()

    class Meta:
        unique_together = ('business', 'network')

    def __str__(self):
        return f"{self.business.name} - {self.platform}"


class BusinessReview(models.Model):
    choices = [
        (1, '1 Star'),
        (2, '2 Stars'),
        (3, '3 Stars'),
        (4, '4 Stars'),
        (5, '5 Stars'),
    ]
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    stars = models.PositiveSmallIntegerField(choices=choices)
    description = models.TextField()
    creation_time = models.DateTimeField(auto_now_add=True)
    business = models.ForeignKey(
        Business,
        on_delete=models.CASCADE,
        related_name='business_reviews'
    )

    class Meta:
        unique_together = ('business', 'user')

    def __str__(self):
        return f"{self.user.username} review for {self.business.name}"
    

class BusinessImage(models.Model):
    business  = models.ForeignKey(Business,on_delete=models.CASCADE,related_name="business_images")
    image = models.ImageField(upload_to="business_images")
    uploaded_time = models.DateTimeField(auto_now_add=True)
    featured_img = models.BooleanField(default=False)
    def __str__(self):
        return f"Image for {self.business.name}"


class BusinessHours(models.Model):
    weekdays = [
        ('mon', 'Monday'),
        ('tue', 'Tuesday'),
        ('wed', 'Wednesday'),
        ('thu', 'Thursday'),
        ('fri', 'Friday'),
        ('sat', 'Saturday'),
        ('sun', 'Sunday'),
    ]
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name='hours')
    day = models.CharField(max_length=3, choices=weekdays)
    open_time = models.TimeField()
    close_time = models.TimeField()
    
    def __str__(self): 
        return f"{self.business.name} - {self.day}"

class BusinessPartnerRequest(models.Model):

    STATUS = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]

    from_business = models.ForeignKey(
        Business,
        on_delete=models.CASCADE,
        related_name='sent_partnership_requests'
    )

    to_business = models.ForeignKey(
        Business,
        on_delete=models.CASCADE,
        related_name='received_partnership_requests'
    )

    status = models.CharField(
        max_length=10,
        choices=STATUS,
        default='pending'
    )

    message = models.TextField(blank=False)

    creation_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('from_business', 'to_business')

    def __str__(self):
        return f"{self.from_business} -> {self.to_business}"


