from django.shortcuts import render
from cafe.models import Cafe
# Create your views here.
from django.shortcuts import render, redirect
from django.urls import reverse # To get URL by name
from django.db import transaction # For atomic transactions
from .forms import CafeForm, CafeImageFormSet, CafeHighlightFormSet


from django.contrib.auth.mixins import LoginRequiredMixin # Required to ensure users are logged in
from .models import CafeReview # Import your Cafe and CafeReview models
from .forms import CafeReviewForm # Import the CafeReviewForm you just created
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View


from cafe.models import CafeLocation
from django.views.generic.detail import DetailView

from datetime import datetime, timedelta
from booking.forms import BookingForm
from django.contrib import messages
from datetime import date

def get_time_slots(opening, closing, interval=60):
    slots = []
    current = datetime.combine(datetime.today(), opening)
    end = datetime.combine(datetime.today(), closing)
    while current < end:
        slots.append(current.time())
        current += timedelta(minutes=interval)
    return slots

def cafe(request):
    cafes=Cafe.objects.all()

    context ={
        'locations': CafeLocation.objects.all(),
        'cafes': cafes,
    }
    return render(request,"cafes.html",context)
# Create your views here.
# Assuming you're getting a single cafe instance






def register_cafe_view(request):
    if request.method == 'POST':
        cafe_form = CafeForm(request.POST)
        # Pass request.FILES for image uploads
        image_formset = CafeImageFormSet(request.POST, request.FILES, prefix='images')
        highlight_formset = CafeHighlightFormSet(request.POST, prefix='highlights')

        # Check if all forms and formsets are valid
        if cafe_form.is_valid() and image_formset.is_valid() and highlight_formset.is_valid():
            try:
                # Use a transaction to ensure all saves succeed or fail together
                with transaction.atomic():
                    cafe = cafe_form.save() # Save the main Cafe instance

                    # Save images with automatically assigned sequential order
                    image_order_counter = 0
                    for form in image_formset:
                        # Check if the form has data and is not marked for deletion
                        if form.cleaned_data and not form.cleaned_data.get('DELETE'):
                            image = form.save(commit=False) # Get the instance but don't save to DB yet
                            image.cafe = cafe # Link the image to the newly created cafe
                            image_order_counter += 1
                            image.order = image_order_counter # Assign order
                            image.save() # Now save the image

                    # Save highlights with automatically assigned sequential order
                    highlight_order_counter = 0
                    for form in highlight_formset:
                        if form.cleaned_data and not form.cleaned_data.get('DELETE'):
                            highlight = form.save(commit=False)
                            highlight.cafe = cafe
                            highlight_order_counter += 1
                            highlight.order = highlight_order_counter # Assign order
                            highlight.save()

                # Redirect to a success page after successful registration
                return redirect(reverse('registration_success'))

            except Exception as e:
                # In a real application, you'd log this error and show a user-friendly message
                print(f"Error saving cafe: {e}")
                # Optionally, re-render the form with a general error message
                # messages.error(request, "There was an error registering your cafe. Please try again.")

        else:
            # If any form/formset is invalid, print errors for debugging
            print("Data")
            print("Form errors:")
            print("Cafe Form Errors:", cafe_form.errors)
            print("Image Formset Errors:", image_formset.errors)
            print("Highlight Formset Errors:", highlight_formset.errors)
            # The template will automatically display specific field errors

    else: # GET request, display empty forms
        cafe_form = CafeForm()
        image_formset = CafeImageFormSet(prefix='images')
        highlight_formset = CafeHighlightFormSet(prefix='highlights')

    context = {
        'form': cafe_form,
        'image_formset': image_formset,
        'highlight_formset': highlight_formset,
        'locations': CafeLocation.objects.all()
    }
    return render(request, 'register-cafe.html', context)

def registration_success_view(request):
    context ={
        'locations': CafeLocation.objects.all()
    }
    return render(request, 'registration_success.html', context)


# --- Class-Based Views for Review Functionality ---

class CafeDetailWithReviewsView( View):
    """
    View for displaying a specific cafe's details and its reviews,
    as well as handling the submission of new reviews for that cafe.
    Users must be logged in to access this view (LoginRequiredMixin).
    This view now handles the 'cafe_detail' URL.
    """
    template_name = 'cafe-details.html' # Path to your template

    def get(self, request, pk, *args, **kwargs): # Changed cafe_id to pk to match URL
        """
        Handles GET requests to display the cafe details and reviews.
        """
        # Retrieve the Cafe object based on the 'pk' (cafe ID) from the URL.
        cafe = get_object_or_404(Cafe, id=pk) # Use id=pk for lookup
        
        # Fetch all reviews related to this specific cafe, ordered by most recent first.
        reviews = CafeReview.objects.filter(cafe=cafe).order_by('-date_posted')
        
        # --- ADDED: Fetch cafe images and highlights ---
        cafe_images = cafe.images.all() # Using the related_name 'images' from CafeImage model
        cafe_highlights = cafe.highlights.all() # Using the related_name 'highlights' from CafeHighlight model
        
        # Initialize an empty form for new review submission.
        form = CafeReviewForm()
        
        # Assuming 'cafe' is your Cafe instance
        booking_form = BookingForm()
        time_slots = get_time_slots(cafe.opening_hours, cafe.closing_hours, interval=60)  # interval in minutes

        context = {
            'cafe': cafe,             # The specific cafe object
            'reviews': reviews,       # Queryset of reviews for this cafe
            'form': form,             # The empty review submission form
            'cafe_images': cafe_images,     # Queryset of images for this cafe
            'cafe_highlights': cafe_highlights, # Queryset of highlights for this cafe
            'locations': CafeLocation.objects.all(), # Pass all locations for navigation
            'booking_form': booking_form,
            'time_slots': time_slots,
            'today': date.today().isoformat(),
        }
        # Render the template with the gathered context data.
        return render(request, self.template_name, context)

    def post(self, request, pk, *args, **kwargs): # Changed cafe_id to pk to match URL
        """
        Handles POST requests for submitting a new review.
        """
        cafe = get_object_or_404(Cafe, id=pk) # Use id=pk for lookup
        # Create a form instance and populate it with data from the POST request.
        form = CafeReviewForm(request.POST)
        booking_form = BookingForm(request.POST)
        time_slots = get_time_slots(cafe.opening_hours, cafe.closing_hours, interval=60)  # interval in minutes

        
        # Check which form was submitted (you can use a hidden field or button name in your template)
        if 'submit_review' in request.POST:
            if not request.user.is_authenticated:
                messages.error(request, "Please log in to submit a review.")
                return redirect('login_user')
            if form.is_valid():
                review = form.save(commit=False)
                review.cafe = cafe
                review.user = request.user
                review.save()
                messages.success(request, "Your review was submitted successfully!")
                return redirect('cafe_reviews', pk=cafe.id)
            else:
                # ... handle review form errors ...
                pass

        elif 'submit_booking' in request.POST:
            print(booking_form.is_valid())
            if booking_form.is_valid():
                booking = booking_form.save(commit=False)
                booking.cafe = cafe
                booking.user = request.user
                booking.save()
                messages.success(request, "Your booking was submitted successfully!")
                return redirect('booking_list')  # <-- CHANGE THIS LINE
            else:
                # ... handle booking form errors ...
                pass

        # If neither form was submitted or there was an error, re-render the page with the form errors.
        reviews = CafeReview.objects.filter(cafe=cafe).order_by('-date_posted')
        
        # --- ADDED: Re-fetch cafe images and highlights on form error ---
        cafe_images = cafe.images.all()
        cafe_highlights = cafe.highlights.all()

        context = {
            'cafe': cafe,
            'reviews': reviews,
            'form': form, # Pass the form with errors back to the template
            'cafe_images': cafe_images,     # Include images on re-render
            'cafe_highlights': cafe_highlights, # Include highlights on re-render
            'locations': CafeLocation.objects.all(),
            'booking_form': booking_form,
            'time_slots': time_slots,
            'today': date.today().isoformat(),
        }
        return render(request, self.template_name, context)

class AllReviewsListView(View):
    """
    View to display all reviews for a specific cafe.
    It takes a 'pk' (cafe_id) from the URL to filter the reviews.
    This view now handles the 'all_reviews_for_cafe' URL.
    """
    template_name = 'reviews.html' # Path to your 'all reviews' template
    
    def get(self, request, pk, *args, **kwargs): # Changed cafe_id to pk to match URL
        """
        Handles GET requests to display all reviews for a specific cafe.
        """
        # Get the specific cafe or return 404
        cafe = get_object_or_404(Cafe, id=pk) # Use id=pk for lookup
        
        # Fetch all CafeReview objects related to this cafe, ordered by most recent first.
        reviews = CafeReview.objects.filter(cafe=cafe).order_by('-date_posted')
        context = {
            'cafe': cafe,      # Pass the cafe object to the template
            'reviews': reviews, # Queryset of all reviews for this cafe
            'locations': CafeLocation.objects.all()
        }
        # Render the template with all reviews.
        return render(request, self.template_name, context)

class CafeLocationDetails(DetailView):
    model=CafeLocation
    template_name='location/location.html'
    context_object_name="location"
    slug_field="location_slug"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        location=self.object
        context['locations'] = CafeLocation.objects.all()
        context["cafes"]=Cafe.objects.exclude(location=location)
        
        return context