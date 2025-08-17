from django.urls import path
from .views import MoviesListView, MovieDetailView, ShowsListView, SeatBooking, UserCreateView, UserListView, CustomAuthToken, UserDetailView, BookedSeatsAPIView,BookingHistoryApi,CreateRazorpayOrderAPIView

urlpatterns = [
    path('movies/', MoviesListView.as_view(), name='movie-list'),
    path('movies/<int:pk>/', MovieDetailView.as_view(), name='movie-detail'),
    path('seat-booking/', SeatBooking.as_view(), name='seat-booking'),
    path('shows/', ShowsListView.as_view(), name='show-list'),
    path('register/', UserCreateView.as_view(), name='register-user'),
    path('show_users/', UserListView.as_view(), name='show-user'),
    path('show_users/<str:email>/', UserDetailView.as_view(), name='user-detail'),
    path('booked-seats/', BookedSeatsAPIView.as_view(), name='booked-seats'),
    path('booking-history/', BookingHistoryApi.as_view(), name='booking-history'),
    path('api-token-auth/', CustomAuthToken.as_view(), name='api_token_auth'),
    path('create-razorpay-order/', CreateRazorpayOrderAPIView.as_view(), name='create-razorpay-order'),
    ]