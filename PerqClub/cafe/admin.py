from django.contrib import admin
from .models import Cafe,CafeImage,CafeHighlight,CafeReview,CafeLocation
# Register your models here.

class CafeImageInline(admin.TabularInline): # Or admin.StackedInline
    model = CafeImage
    extra = 0 # How many empty forms to show
    # max_num = 5 # This is where you set the limit!
    fields = ['image', 'alt_text', 'order'] # Expose alt_text and order for admin editing
    # readonly_fields = ['image'] # Make image read-only after upload in admin (optional)
    # list_editable = ['order'] # Allow direct editing of order in the inline list
    # list_display=['cafe','images','alt_text']
@admin.register(CafeImage)
class CafeImageAdmin(admin.ModelAdmin):
    list_display = ['cafe', 'image', 'alt_text']
    search_fields = ['alt_text', 'cafe__cafe_name']
    list_filter = ['cafe']  # ✅ Filters on the right sidebar

# admin.site.register(CafeImage, CafeImageAdmin)

# NEW: Define the inline for CafeHighlight
class CafeHighlightInline(admin.TabularInline): # Use TabularInline for compactness
    model = CafeHighlight
    extra = 0 # Show 1 empty form by default
    # max_num = 6 # <--- THIS IS WHERE YOU SET THE LIMIT OF 6 HIGHLIGHTS
    fields = ['highlight_text','icon_class', 'order'] # Expose text and order
    list_editable = ['order']
@admin.register(CafeHighlight)
class cafeHighlightAdmin(admin.ModelAdmin):
    list_display = ['cafe', 'highlight_text','icon_class','order']
    search_fields = ['highlight_text', 'cafe__cafe_name']
    list_filter = ['cafe','highlight_text']  # ✅ Filters on the right sidebar

# admin.site.register(CafeHighlight,cafeHighlightAdmin)

@admin.register(Cafe)
class CafeAdmin(admin.ModelAdmin):
    # list_display = ["cafe_name","branch_name","cafe_description","cafe_location","opening_time","closing_time"]
    # inlines = [CafeImageInline,CafeHighlightInline]
    ##
    list_display = (
        'cafe_name', 'branch_name', 'cafe_location', 'is_approved', 'created_at',
        'contact_email', 'contact_phone', 'opening_hours', 'closing_hours', 'is_cafe_of_the_week', 'location',
        'manager'
    )
    list_filter = ('is_approved', 'location','is_cafe_of_the_week')
    list_editable = ('is_approved',)
    search_fields = ('cafe_name', 'branch_name', 'cafe_location')
    inlines = [CafeImageInline, CafeHighlightInline] # Integrate inlines here

    # Customize the admin form layout
    fieldsets = (
        ('Cafe Details', {
            'fields': (
                'cafe_name', 'branch_name', 'cafe_description', 'cafe_address',
                'cafe_location', 'branch_manager_name',
                ('opening_hours', 'closing_hours'), # Group times on one line
                ('contact_email', 'contact_phone'), # Group contact info
                'website_url', 'cafe_specialty', 'map_url', 'location', 'is_cafe_of_the_week',
                'manager',  # <-- Add this line
            )
        }),
        ('Legal & Compliance', {
            'fields': ('terms_accepted',),
            'classes': ('collapse',) # Makes this section collapsible in admin
        }),
    )


# Register the CafeReview model
@admin.register(CafeReview)
class CafeReviewAdmin(admin.ModelAdmin):
    """
    Admin configuration for the CafeReview model.
    Provides comprehensive management of cafe reviews.
    """
    list_display = (
        'cafe', 'user', 'rating', 'comment_snippet',
        'date_posted', 'helpful_count', 'has_reply', 'is_featured'
    )
    list_filter = ('cafe', 'rating', 'date_posted','is_featured')
    search_fields = ('comment', 'user__username', 'cafe__cafe_name')
    readonly_fields = ('date_posted', 'helpful_count') # These are typically auto-set or managed by interaction
    
    # Custom method to display a snippet of the comment in the list view
    def comment_snippet(self, obj):
        return obj.comment[:75] + '...' if len(obj.comment) > 75 else obj.comment
    comment_snippet.short_description = 'Comment' # Column header in admin list

    # Custom method to check if a review has a reply
    def has_reply(self, obj):
        return bool(obj.reply)
    has_reply.boolean = True # Displays a checkmark/cross icon
    has_reply.short_description = 'Replied' # Column header

    # Define the fields order and grouping for the detail view in the admin
    fieldsets = (
        (None, {
            'fields': ('cafe', 'user', 'rating', 'comment','is_featured')
        }),
        ('Admin Actions', {
            'fields': ('reply', 'helpful_count'),
            'description': "Fields managed by administrators."
        }),
        ('Timestamps', {
            'fields': ('date_posted',),
            'classes': ('collapse',), # Makes this section collapsible
        }),
    )



# admin.site.register(Cafe,CafeAdmin)



class LocationAdmin(admin.ModelAdmin):
    list_display=['id','location_name','location_slug']
    search_fields = ['location_name']
admin.site.register(CafeLocation,LocationAdmin)

admin.site.site_header="PerqClub"