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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].required = False

    def save(self, commit=True):
        instance = super().save(commit=False)
        if not instance.alt_text:
            file_name = os.path.basename(instance.image.name)
            instance.alt_text = os.path.splitext(file_name)[0].replace('_', ' ').replace('-', ' ').strip()
        if commit:
            instance.save()
        return instance

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            if not image.content_type in ['image/jpeg', 'image/png','image/jpg']:
                raise forms.ValidationError("Only JPEG and PNG and JPG images are allowed.")
        return image


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


from django import forms
from django.forms import inlineformset_factory
from cafe.models import Cafe, CafeImage, CafeHighlight

class CafeEditForm(forms.ModelForm):
    class Meta:
        model = Cafe
        fields = [
            'cafe_name',
            'branch_name',
            'cafe_address',
            'cafe_description',
            'cafe_specialty',
            'opening_hours',
            'closing_hours',
            'contact_email',
            'contact_phone',
            'website_url',
            'map_url',
        ]

class CafeImageForm(forms.ModelForm):
    class Meta:
        model = CafeImage
        fields = ['image', 'alt_text', 'order']  # your fields here
        widgets = {
            'image': forms.ClearableFileInput(attrs={'class': 'custom-file-width'}),
        }
        

class CafeHighlightForm(forms.ModelForm):
    class Meta:
        model = CafeHighlight
        fields = ['highlight_text', 'icon_class', 'order']  # use your model's fields here
        widgets = {
            'highlight_text': forms.TextInput(attrs={'placeholder': 'e.g., Free Wi-Fi'}),
            'icon_class': forms.TextInput(attrs={'placeholder': 'Optional icon class'}),
        }

CafeImageFormSet = inlineformset_factory(
    Cafe,
    CafeImage,
    form=CafeImageForm,
    fields=['image', 'alt_text', 'order'],
    extra=5,
    max_num=5,  # Strictly allow only 5 images
    can_delete=True,
)

CafeHighlightFormSet = inlineformset_factory(
    Cafe,
    CafeHighlight,
    form=CafeHighlightForm,
    fields=['highlight_text', 'icon_class', 'order'],
    extra=6,
    max_num=6,  # Strictly allow only 5 highlights
    can_delete=True,
)

# import os
# from django import forms
# from django.forms import inlineformset_factory
# from .models import Cafe, CafeImage, CafeHighlight, CafeReview

# class CafeForm(forms.ModelForm):
#     terms_accepted = forms.BooleanField(required=True, label="I agree to the Terms & Conditions")
#     class Meta:
#         model = Cafe
#         fields = [
#             'cafe_name', 'branch_name', 'cafe_description', 'cafe_address',
#             'cafe_location', 'branch_manager_name', 'opening_hours',
#             'closing_hours', 'contact_email', 'contact_phone', 'website_url', 'cafe_specialty','terms_accepted',
#         ]
#         widgets = {
#             'cafe_description': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Tell us about your café...'}),
#             'cafe_address': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Full street address'}),
#             'cafe_location': forms.TextInput(attrs={'placeholder': 'e.g., Andheri, Mumbai'}),
#             'opening_hours': forms.TimeInput(attrs={'type': 'time'}),
#             'closing_hours': forms.TimeInput(attrs={'type': 'time'}),
#             'website_url': forms.URLInput(attrs={'placeholder': 'https://...'}),
#             'cafe_specialty': forms.Textarea(attrs={'rows': 2, 'placeholder': 'What makes your café special? Any Special Dishes?'}),
#         }
#         labels = {
#             'cafe_name': 'Café Name',
#             'branch_name': 'Branch Name',
#             'cafe_description': 'Description',
#             'cafe_address': 'Address',
#             'cafe_location': 'Location',
#             'branch_manager_name': 'Manager Name',
#             'opening_hours': 'Opening Time',
#             'closing_hours': 'Closing Time',
#             'contact_email': 'Contact Email',
#             'contact_phone': 'Phone Number',
#             'website_url': 'Website URL',
#             'cafe_specialty': 'Specialty',
#         }

# from django import forms
# from .models import CafeImage

# class CafeImageForm(forms.ModelForm):
#     def __init__(self, *args, **kwargs):
#         image_required = kwargs.pop('image_required', True)
#         super().__init__(*args, **kwargs)
#         self.fields['image'].required = image_required

#     class Meta:
#         model = CafeImage
#         fields = ['image']


# class CafeHighlightForm(forms.ModelForm):
#     class Meta:
#         model = CafeHighlight
#         fields = ['highlight_text', 'icon_class', 'order']
#         widgets = {
#             'highlight_text': forms.TextInput(attrs={'placeholder': 'e.g., Free Wi-Fi, Pet-friendly'}),
#             'icon_class': forms.TextInput(attrs={'placeholder': 'Optional icon class'}),
#         }

# class CafeReviewForm(forms.ModelForm):
#     class Meta:
#         model = CafeReview
#         fields = ['rating', 'comment']
#         widgets = {
#             'comment': forms.Textarea(attrs={
#                 'placeholder': 'Share your experience...',
#                 'class': 'mt-1 block w-full px-4 py-3 border border-amber-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-amber-500 focus:border-amber-500 text-base bg-white text-amber-900 placeholder-amber-400 resize-y'
#             }),
#             'rating': forms.HiddenInput(attrs={'id': 'selectedRating'}),
#         }
#         labels = {
#             'rating': 'Rating',
#             'comment': 'Comment',
#         }

# # Inline formsets
# from django.forms import inlineformset_factory
# from .models import Cafe, CafeImage

# CafeImageFormSet = inlineformset_factory(
#     Cafe,
#     CafeImage,
#     form=CafeImageForm,
#     extra=1,
#     fields=['image', 'alt_text', 'order'],
#     can_delete=True
# )


# CafeHighlightFormSet = inlineformset_factory(
#     Cafe,
#     CafeHighlight,
#     form=CafeHighlightForm,
#     fields=['highlight_text', 'icon_class', 'order'],
#     extra=5,
#     max_num=5,
#     can_delete=True,
# )

# from django.forms.models import BaseModelFormSet

# class BaseImageFormSet(BaseModelFormSet):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         for form in self.forms:
#             form.fields['image'].required = False


from user.models import CustomUser
from .models import CafeLocation
class AdminCafeForm(CafeForm):
    # these are the extra fields only admins should edit:
    is_approved = forms.BooleanField(required=False, label="Approved?")
    is_cafe_of_the_week = forms.BooleanField(required=False, label="Cafe of the Week?")
    location = forms.ModelChoiceField(
        queryset=CafeLocation.objects.all(), # your CafeLocation queryset
    )
    manager = forms.ModelChoiceField(
        queryset=CustomUser.objects.filter(is_cafe=True),
        required=False,
        label="Assigned Manager"
    )

    class Meta(CafeForm.Meta):
        # append the extra fields:
        fields = CafeForm.Meta.fields + [
            'is_approved',
            'is_cafe_of_the_week',
            'location',
            'manager',
        ]