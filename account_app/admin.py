from django.contrib import admin
from .models import ArtistModel, ArtworkModel, ReviewModel
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# Register your models here.
class ArtistAdmin(BaseUserAdmin):
    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ["id", "username", "fullname", "email", "bio", "is_admin", "created_at"]
    list_filter = ["is_admin"]
    fieldsets = [
        ("User Credentials", {"fields": ["username", "password"]}),
        ("Personal info", {"fields": ["fullname", "email", "bio"]}),
        ("Permissions", {"fields": ["is_admin"]}),
    ]
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields": ["username", "fullname", "email", "bio", "password1", "password2"],
            },
        ),
    ]
    search_fields = ["username"]
    ordering = ["username", "id"]
    filter_horizontal = []

# Now register the new UserAdmin...
admin.site.register(ArtistModel, ArtistAdmin)

class ArtworkAdmin(admin.ModelAdmin):
    list_display = ['id', 'artist', 'title', 'description', 'image_url', 'creation_date']
# Now register the Artwork
admin.site.register(ArtworkModel, ArtworkAdmin)
admin.site.register(ReviewModel)