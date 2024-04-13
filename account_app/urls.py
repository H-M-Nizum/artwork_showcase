from django.urls import path
from .views import ArtistRegistrationViews, ArtistLoginView, ArtistProfileView, ArtworkListCreateAPIView, ArtworkUpdateAPIView

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    path('registration/', ArtistRegistrationViews.as_view(), name='artist_registration'),
    path('login/', ArtistLoginView.as_view(), name='artist_login'),
    path('profile/', ArtistProfileView.as_view(), name='artist_profile'),

    path('artworks/', ArtworkListCreateAPIView.as_view(), name='artwork_list_create'),
    path('artworks/<int:pk>/', ArtworkUpdateAPIView.as_view(), name='artwork_detail_update_delete'),
]
