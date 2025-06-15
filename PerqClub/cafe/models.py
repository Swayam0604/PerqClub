from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User # Import Django's User model
from autoslug import AutoSlugField

# Create your models here.

class Cafe(models.Model):
    cafe_name = models.CharField(max_length=200)
    branch_name = models.CharField(max_length=200)
    cafe_description = models.TextField()
    cafe_address = models.TextField(default="")
    map_url = models.URLField(default='',max_length=1000)
    cafe_location = models.CharField(max_length=200)
    branch_manager_name = models.CharField(max_length=200)
    opening_hours = models.TimeField()
    closing_hours = models.TimeField()
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=200)
    website_url= models.URLField()
    cafe_specialty = models.TextField(default='')
    terms_accepted = models.BooleanField(default=False, blank=True, null=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    location = models.ForeignKey('CafeLocation', on_delete=models.PROTECT,null=True)

    def __str__(self):
        return f"{self.cafe_name} ({self.branch_name or 'Main'})"    #

    class Meta:
        verbose_name = "Cafe"           #
        verbose_name_plural = "Cafes"
    

# New Model for Cafe Images
class CafeImage(models.Model):
    cafe = models.ForeignKey(Cafe, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='cafe_images/') # The actual image file
    alt_text = models.CharField(max_length=255, blank=True,null=True) # Optional: for accessibility and SEO
    order = models.PositiveIntegerField(default=0, blank=True, null=False) # Optional: to order images

    class Meta:
        ordering = ['order'] # Order images by the 'order' field by default
        verbose_name = "Cafe Image"             #
        verbose_name_plural = "Cafe Images"     

    def __str__(self):
        return f"Image for {self.cafe.cafe_name} ({self.image.name})"
    
    
# NEW: Model for Cafe Highlights
class CafeHighlight(models.Model):
    cafe = models.ForeignKey(Cafe, on_delete=models.CASCADE, related_name='highlights')
    # Use CharField for a single highlight point
    highlight_text = models.CharField(max_length=255) # Assuming each highlight is a short phrase
    icon_class = models.CharField(
        max_length=50,
        blank=True,  # Allow it to be blank in forms
        null=True,   # Allow NULL in the database
        help_text="Optional: Manually specify icon class (e.g., 'fa-wifi'). If left blank, an icon will be inferred from highlight text if mapped."
    )
    order = models.PositiveIntegerField(default=1, blank=True, null=False) # Optional: for ordering

    class Meta:
        ordering = ['order']
        unique_together = ('cafe', 'highlight_text') # Optional: prevent duplicate highlights for a single cafe
        verbose_name = "Cafe Highlight"
        verbose_name_plural = "Cafe Highlights"

    def __str__(self):
        return f"Highlight for {self.cafe.cafe_name}: {self.highlight_text[:50]}..." # Show first 50 chars


class CafeReview(models.Model):
    cafe = models.ForeignKey(Cafe, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveIntegerField(default=0)  # 1–5 stars
    comment = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)
    helpful_count = models.PositiveIntegerField(default=0)
    reply = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['-date_posted'] # Order reviews by most recent first

    def __str__(self):
        return f"Review by {self.user.username} for {self.cafe.cafe_name} ({self.rating} stars)"

    def get_star_rating_html(self):
        """
        Generates HTML for displaying star ratings.
        Uses Font Awesome classes for solid stars (fas) and empty stars (far).
        """
        full_stars = self.rating
        print(self.rating)
        html = ''
        # Add solid stars for the rating value
        for i in range(full_stars):
            print("Hello")
            html += ' <svg class="h-5 w-5 star-filled" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.538 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.783.57-1.838-.197-1.538-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.462a1 1 0 00.95-.69l1.07-3.292z" /></svg>'
        # Add empty stars for the remainder up to 5
        for _ in range(5 - full_stars):
            html += ' <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="gray" stroke="#FFD700" stroke-width="0.5" class="h-5 w-5 star-filled"><path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.7551.688-1.538 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.783.57-1.838-.197-1.538-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.462a1 1 0 00.95-.69l1.07-3.292z" /></svg>'
        return html
    

## TO CREATE A CATEGORY FOR LOCATION 

class CafeLocation(models.Model):
    location_name=models.CharField(max_length=10)
    location_slug=AutoSlugField(populate_from='location_name',unique=True)

    def __str__(self):
        return self.location_name
