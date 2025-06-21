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

def cafe(request):
    cafes=Cafe.objects.all()

    context ={
        'locations': CafeLocation.objects.all(),
        'cafes': cafes,
    }
    return render(request,"cafes.html",context)
# Create your views here.
# Assuming you're getting a single cafe instance


# def cafe_detail_view(request, pk):
#     cafe = Cafe.objects.get(pk=pk)
#     # Now you can get all images related to this cafe
#     # reviews = cafe.reviews.order_by('-date_posted')  # related_name from model
#     cafe_images = cafe.images.all() # Using the related_name 'images'
#     cafe_highlights = cafe.highlights.all()  # related_name from the model
#     context = {
#         'cafe': cafe,
#         'cafe_images': cafe_images,
#         'cafe_highlights': cafe_highlights,
        
#     }
#     return render(request, 'cafe-details.html', context)

# def cafereview(request):
#     return render(request,"reviews.html")


##
# cafe_app/views.py





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
        print("Hrllo")
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
        
        context = {
            'cafe': cafe,             # The specific cafe object
            'reviews': reviews,       # Queryset of reviews for this cafe
            'form': form,             # The empty review submission form
            'cafe_images': cafe_images,     # Queryset of images for this cafe
            'cafe_highlights': cafe_highlights, # Queryset of highlights for this cafe
            'locations': CafeLocation.objects.all(), # Pass all locations for navigation
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

        if form.is_valid():
            # If the form data is valid, save the review but don't commit it to the database yet.
            review = form.save(commit=False)
            
            # Assign the current Cafe instance to the review.
            review.cafe = cafe
            # Assign the currently logged-in user to the review.
            review.user = request.user 
            
            # Now, save the review to the database.
            review.save()
            
            # Redirect back to the same cafe's review page after successful submission
            return redirect('cafe_detail', pk=cafe.id) # Use pk for redirect argument
        else:
            # If the form data is NOT valid, re-render the page with the form errors.
            # IMPORTANT: Print form errors to your console to debug why validation failed.
            print("Form errors:", form.errors)
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
            }
            return render(request, self.template_name, context, {'locations': CafeLocation.objects.all()})

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