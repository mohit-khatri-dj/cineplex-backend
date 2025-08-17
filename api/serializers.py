from rest_framework.serializers import ModelSerializer
from .models import Movie, Theatre, Show, Booking
from django.contrib.auth.models import User
from rest_framework import serializers

class TheatreSerializer(ModelSerializer):
    class Meta:
        model = Theatre
        fields = ['id', 'name', 'address', 'contact']
        read_only_fields = ('created_at', 'updated_at')


class ShowSerializer(ModelSerializer):
    theatre = TheatreSerializer(read_only=True)
    class Meta:
        model = Show
        fields = ['id', 'theatre', 'date', 'time', 'price']
        read_only_fields = ('created_at', 'updated_at')


class MovieSerializer(ModelSerializer):
    currentshow = ShowSerializer(many=True, read_only=True)
    
    class Meta:
        model = Movie
        fields = ['id', 'name', 'description', 'langauge', 'genre', 'duration', 'cast', 
                  'director', 'release_date', 'image', 'currentshow']
        read_only_fields = ('created_at', 'updated_at')


class BookingSerializer(ModelSerializer):
    class Meta:
        model = Booking
        fields = ['id', 'user', 'movie', 'show', 'date', 'time', 'seats', 'amount', 'status']
        read_only_fields = ('created_at', 'updated_at')


class UserSerializer(ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email','password']
        read_only_fields = ('date_joined', 'last_login')

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)  # This hashes the password
        user.save()
        return user

    
