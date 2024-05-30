from rest_framework import serializers
from .models import ArtistModel, ArtworkModel, ReviewModel

class ArtworkSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArtworkModel
        fields = '__all__'

# Artist Register serializers
class ArtistRegistrationSerializer(serializers.ModelSerializer):
    artworks = ArtworkSerializer(many=True, read_only=True)
    password2 = serializers.CharField(style={'input_type' : 'password'}, write_only=True)

    class Meta:
        model = ArtistModel
        fields = ['id', 'username', 'fullname', 'email', 'bio', 'artworks', 'password', 'password2']
        extra_kwargs={
            'password' : {'write_only' : True}
        }
    
    # validate password and confirm password
    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')

        if password != password2:
            raise serializers.ValidationError("password and confirm password does not match")
        return attrs

    # for coustom user use create method
    def create(self, validate_data):
        return ArtistModel.objects.create_user(**validate_data)

# Artist login serializers
class ArtistLoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=100)
    class Meta:
        model = ArtistModel
        fields = ['username', 'password']

# Artist profile serializers
class ArtistProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArtistModel
        fields = ['id', 'username', 'fullname', 'email', 'bio']

# Review serializers

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewModel
        fields = '__all__'