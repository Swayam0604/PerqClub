# cafe_app/forms.py

import os # Import os module for path operations
from django import forms
from .models import Cafe, CafeImage, CafeHighlight, CafeReview
from django.forms import inlineformset_factory

class CafeForm(forms.ModelForm):
    # This field maps to your HTML checkbox and ensures it's required for submission
    terms_accepted = forms.BooleanField(required=True, label="I agree to the Terms & Conditions")

    class Meta:
        model = Cafe
        fields = [
            'cafe_name', 'branch_name', 'cafe_description', 'cafe_address',
            'cafe_location', 'branch_manager_name', 'opening_hours',
            'closing_hours', 'contact_email', 'contact_phone', 'website_url','cafe_specialty',
            
        ]
        widgets = {
            'cafe_description': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Tell us about your café...'}),
            'cafe_address': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Full street address'}),
            'cafe_location': forms.TextInput(attrs={'placeholder': 'e.g., Andheri, Mumbai'}),
            'opening_hours': forms.TimeInput(attrs={'type': 'time'}),
            'closing_hours': forms.TimeInput(attrs={'type': 'time'}),
            'website_url': forms.URLInput(attrs={'placeholder': 'https://...'}),
            'cafe_specialty': forms.Textarea(attrs={'rows': 2, 'placeholder': 'What makes your café special?Any Special Dishes?'}),
            
        }
        labels = {
            'cafe_name': 'Café Name',
            'branch_name': 'Branch Name',
            'cafe_description': 'Description',
            'cafe_address': 'Address',
            'cafe_location': 'Location',
            'branch_manager_name': 'Manager Name',
            'opening_hours': 'Opening Time',
            'closing_hours': 'Closing Time',
            'contact_email': 'contact Email',
            'contact_phone': 'Phone Number',
            'website_url': 'Website URL',
            'cafe_specialty': 'Specialty',
            
        }


class CafeImageForm(forms.ModelForm):
    class Meta:
        model = CafeImage
        fields = ['image','alt_text'] # Only include 'image'. 'alt_text' and 'order' are handled automatically/in admin.
        widgets = {
            'image': forms.FileInput(attrs={'accept': 'image/*'}),
        }

    def save(self, commit=True):
        instance = super().save(commit=False)
        if not instance.alt_text:
            file_name = os.path.basename(instance.image.name)
            instance.alt_text = os.path.splitext(file_name)[0].replace('_', ' ').replace('-', ' ').strip()
        if commit:
            instance.save()
        return instance


# Formset for Cafe Images (allows multiple image uploads)
CafeImageFormSet = inlineformset_factory(
    Cafe,
    CafeImage,
    form=CafeImageForm,
    extra=5, # Number of empty forms to display initially
    can_delete=True, # Allows forms to be marked for deletion (useful for editing)
)

class CafeHighlightForm(forms.ModelForm):
    class Meta:
        model = CafeHighlight
        fields = ['highlight_text'] # Only text is input by user
        # 'order' is handled automatically/in admin
        widgets = {
            'highlight_text': forms.TextInput(attrs={'placeholder': 'e.g., Free Wi-Fi, Pet-friendly'}),
        }

# Formset for Cafe Highlights (allows multiple highlights)
CafeHighlightFormSet = inlineformset_factory(
    Cafe,
    CafeHighlight,
    form=CafeHighlightForm,
    extra=6, # Number of empty forms to display initially
    can_delete=True,
)

class CafeReviewForm(forms.ModelForm):
    """
    A Django ModelForm for handling CafeReview submissions.
    This form allows users to input a rating and a comment.
    The 'cafe' and 'user' fields are intentionally excluded here,
    as they will be set automatically in the view based on the URL
    and the logged-in user, respectively.
    """
    class Meta:
        model = CafeReview
        # Fields that the user will fill out in the form
        fields = ['rating', 'comment']
        
        # Widgets allow for customization of HTML form elements,
        # such as adding placeholder text or CSS classes.
        widgets = {
            'comment': forms.Textarea(attrs={
                'placeholder': 'Share your experience...',
                # Tailwind CSS classes for styling the textarea
                'class': 'mt-1 block w-full px-4 py-3 border border-amber-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-amber-500 focus:border-amber-500 text-base bg-white text-amber-900 placeholder-amber-400 resize-y'
            }),
            # For the rating field, we'll use a hidden input as the stars are handled by JavaScript
            'rating': forms.HiddenInput(attrs={'id': 'selectedRating'})
        }
        
        # Labels to be displayed next to the form fields
        labels = {
            'rating': 'Rating',
            'comment': 'Comment',
        }