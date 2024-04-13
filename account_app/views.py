from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serializers import ArtistRegistrationSerializer, ArtistLoginSerializer, ArtistProfileSerializer
from .renderers import UserRenderer
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated

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