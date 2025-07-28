
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
from django.core.mail import send_mail
from django.conf import settings

def get_time_slots(opening, closing, interval=60):
    slots = []
    current = datetime.combine(datetime.today(), opening)
    end = datetime.combine(datetime.today(), closing)
    while current < end:
        slots.append(current.time())
        current += timedelta(minutes=interval)
    return slots

def cafe(request):
    cafes=Cafe.objects.filter(is_approved=True)

    context ={
        'locations': CafeLocation.objects.all(),
        'cafes': cafes,
    }
    return render(request,"cafes.html",context)
# Create your views here.
# Assuming you're getting a single cafe instance






# def register_cafe_view(request):
#     if request.method == 'POST':
#         print(request.FILES)  # <-- Add this line here
#         form = CafeForm(request.POST, request.FILES)
#         image_formset = CafeImageFormSet(request.POST, request.FILES)
#         highlight_formset = CafeHighlightFormSet(request.POST)

#         if form.is_valid() and image_formset.is_valid() and highlight_formset.is_valid():
#             cafe = form.save()

#             for image_form in image_formset:
#                 print(image_form.errors)
#                 if image_form.cleaned_data:
#                     image = image_form.save(commit=False)
#                     image.cafe = cafe
#                     image.save()

#             for highlight_form in highlight_formset:
#                 if highlight_form.cleaned_data:
#                     highlight = highlight_form.save(commit=False)
#                     highlight.cafe = cafe
#                     highlight.save()

#             return redirect('cafes:list')  # or any success URL

#     else:
#         form = CafeForm()
#         image_formset = CafeImageFormSet()
#         highlight_formset = CafeHighlightFormSet()

#     return render(request, 'register-cafe.html', {
#         'form': form,
#         'image_formset': image_formset,
#         'highlight_formset': highlight_formset,
#     })

def registration_success_view(request):
    context ={
        'locations': CafeLocation.objects.all()
    }
    return render(request, 'registration_success.html', context)


# cafe_app/views.py

# views.py
from django.shortcuts import render, redirect
from .forms import CafeForm, CafeImageFormSet, CafeHighlightFormSet

def register_cafe_view(request):
    if request.method == 'POST':
        form = CafeForm(request.POST, request.FILES)
        image_formset = CafeImageFormSet(request.POST, request.FILES)
        highlight_formset = CafeHighlightFormSet(request.POST)

        if form.is_valid() and image_formset.is_valid() and highlight_formset.is_valid():
            cafe = form.save()

            image_formset.instance = cafe
            image_formset.save()

            for highlight_form in highlight_formset:
                if highlight_form.cleaned_data:
                    highlight = highlight_form.save(commit=False)
                    highlight.cafe = cafe
                    highlight.save()

            return redirect('cafe_list')

    else:
        form = CafeForm()
        image_formset = CafeImageFormSet()
        highlight_formset = CafeHighlightFormSet()

    return render(request, 'register-cafe.html', {
        'form': form,
        'image_formset': image_formset,
        'highlight_formset': highlight_formset,
    })



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
            if booking_form.is_valid():
                booking = booking_form.save(commit=False)
                booking.cafe = cafe
                booking.user = request.user
                booking.save()

            # ✅ Try sending email
                try:
                    subject = f"Booking Confirmation for {cafe.cafe_name}"
                    message = f"""
                    Hi {request.user.first_name},

                    Your booking at {cafe.cafe_name} has been confirmed.
                    Details:
                    - Date: {booking.date}
                    - Time: {booking.time}
                    - People: {booking.people}
                    - Location: {cafe.cafe_address}

                    Thank you for choosing us!
                    """

                    send_mail(
                        subject=subject,
                        message=message,
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        recipient_list=[request.user.email],
                        fail_silently=False,  # This lets exceptions be raised
                    )

                    messages.success(request, "Your booking was submitted successfully, and a confirmation email has been sent!")

                except Exception as e:
                # Log error or notify admin if needed
                    print(f"Email sending failed: {e}")
                    messages.warning(request, "Your booking was submitted, but we couldn't send the confirmation email. Please check your booking list.")

                return redirect('booking_list')

        else:
            messages.error(request, "There was an error in your booking form. Please correct the fields below.")


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
        context["cafes"]=Cafe.objects.exclude(location=location).filter(is_approved=True)
        context['location_cafes'] = self.object.cafe_set.filter(is_approved=True)
        
        return context