from django.contrib import admin
from .models import Movie, Theatre, Show, Booking


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'langauge', 'genre', 'duration', 'cast', 'director', 'release_date', 'created_at', 'updated_at')
    search_fields = ('name', 'description', 'langauge', 'genre', 'director')
    list_filter = ('langauge', 'genre', 'director')
    ordering = ('-created_at',)
    date_hierarchy = 'release_date'


@admin.register(Theatre)
class TheatreAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'contact', 'created_at', 'updated_at')
    search_fields = ('name', 'address', 'contact')
    ordering = ('-created_at',)

@admin.register(Show)
class ShowAdmin(admin.ModelAdmin):
    list_display = ('movie', 'theatre', 'date', 'time', 'price', 'created_at', 'updated_at')
    search_fields = ('movie__name', 'theatre__name', 'date', 'time')
    list_filter = ('date', 'theatre')
    ordering = ('-created_at',)
    date_hierarchy = 'date'

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'movie', 'show', 'date', 'time', 'seats', 'amount', 'status', 'created_at', 'updated_at')
    search_fields = ('user__username', 'movie__name', 'show__theatre__name', 'date')
    list_filter = ('status', 'date')
    ordering = ('-created_at',)
    date_hierarchy = 'date'