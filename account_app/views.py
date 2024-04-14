from rest_framework.response import Response
from rest_framework import status, generics, permissions
from rest_framework.views import APIView
from .models import ArtistModel, ArtworkModel
from .serializers import ArtistRegistrationSerializer, ArtistLoginSerializer, ArtistProfileSerializer, ArtworkSerializer
from .renderers import UserRenderer
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework import permissions
from django.views.decorators.csrf import csrf_exempt

# Generate Token Manually
def get_tokens_for_user(user):
  refresh = RefreshToken.for_user(user)
  return {
      'refresh': str(refresh),
      'access': str(refresh.access_token),
  }

# Artist registration views 
class ArtistRegistrationViews(APIView):
    def post(self, request):
        serializer = ArtistRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = get_tokens_for_user(user)
        return Response({"data": serializer.data, "Message": "Registration successfully completed", 'token':token,}, status=status.HTTP_201_CREATED)

# Artist loginviews
class ArtistLoginView(APIView):
    renderer_classes = [UserRenderer]
    def post(self, request):
        serializer = ArtistLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.data.get('username')
        password = serializer.data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            token = get_tokens_for_user(user)
            return Response({'token':token, 'Message':'Login Success'}, status=status.HTTP_200_OK)
        else:
            return Response({'errors':{'non_field_errors':['username or Password is not Valid']}}, status=status.HTTP_404_NOT_FOUND)

# Artist profile views
class ArtistProfileView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        serializer = ArtistProfileSerializer(request.user)
        return Response({"data" : serializer.data}, status=status.HTTP_200_OK)
    def put(self, request, format=None):
        serializer = ArtistProfileSerializer(request.user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Profile updated successfully"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, format=None):
        serializer = ArtistProfileSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Profile partial updated successfully"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# using coustom permission method for art owner
class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the artwork.
        return obj.artist == request.user

# create artwork and disply artwork list
class ArtworkListCreateAPIView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request, format=None):
        artworks = ArtworkModel.objects.all()
        serializer = ArtworkSerializer(artworks, many=True)
        return Response({"message": "successfully get Artwork All data", "data" : serializer.data}, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        serializer = ArtworkSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(artist=request.user)
            return Response({"message": "successfully create a new instance", "data" : serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Update and delete artwork
class ArtworkUpdateAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def get(self, request, pk, format=None):
        artwork = self.get_object(pk)
        serializer = ArtworkSerializer(artwork)
        return Response({"message": "successfully get Artwork single instance", "data" : serializer.data}, status=status.HTTP_200_OK)

    @csrf_exempt
    def put(self, request, pk, format=None):
        artwork = self.get_object(pk)
        serializer = ArtworkSerializer(artwork, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "successfully Update single instance", "data" : serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @csrf_exempt
    def patch(self, request, pk, format=None):
        artwork = self.get_object(pk)
        serializer = ArtworkSerializer(artwork, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "successfully Partial update single instance", "data" : serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        artwork = self.get_object(pk)
        artwork.delete()
        return Response({"message": "successfully delete single instance"}, status=status.HTTP_204_NO_CONTENT)

    def get_object(self, pk):
        try:
            return ArtworkModel.objects.get(pk=pk)
        except ArtworkModel.DoesNotExist:
            raise Http404

