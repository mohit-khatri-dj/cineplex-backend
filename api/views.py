from .serializers import MovieSerializer,ShowSerializer,BookingSerializer, UserSerializer
from .models import Movie,Show,Booking
from rest_framework.generics import ListAPIView, RetrieveAPIView,CreateAPIView
from django.contrib.auth.models import User
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from django.conf import settings
import razorpay


# Razorpay client initialization
razorpay_client = razorpay.Client(
    auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
)

class MoviesListView(ListAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

class MovieDetailView(RetrieveAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

class ShowsListView(ListAPIView):
    queryset = Show.objects.all()
    serializer_class = ShowSerializer


class SeatBooking(CreateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

    def perform_create(self, serializer):
        serializer.save()

class UserCreateView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        serializer.save()

class UserListView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetailView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'email'



class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})    

        try:
            serializer.is_valid(raise_exception=True)
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            return Response({
            'token': token.key,
            'user_id': user.id,
            'email': user.email,
            'username': user.username
            })
        except ValidationError as e:
            # Custom validation response
            return Response({
                'error': 'Invalid login credentials.',
                'details': e.detail
            }, status=status.HTTP_400_BAD_REQUEST)


class BookedSeatsAPIView(APIView):
    def get(self, request):
        # Get query params
        movie_id = request.query_params.get('movie_id')
        theatre_id = request.query_params.get('theatre_id')
        show_date = request.query_params.get('date')
        show_time = request.query_params.get('time')

        # Validate parameters
        if not (movie_id and theatre_id and show_date and show_time):
            return Response(
                {'error': 'Please provide movie_id, theatre_id, date, and time'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Get the show matching the criteria
        show = Show.objects.filter(
            movie_id=movie_id,
            theatre_id=theatre_id,
            date=show_date,
            time=show_time
        ).first()

        if not show:
            return Response({'error': 'Show not found'}, status=status.HTTP_404_NOT_FOUND)

        # Get bookings for that show
        bookings = Booking.objects.filter(show=show)

        # Collect all booked seats
        booked_seats = []
        for booking in bookings:
            seats = booking.seats.split(',')
            booked_seats.extend([seat.strip() for seat in seats if seat.strip()])

        # Remove duplicates
        booked_seats = list(set(booked_seats))

        return Response({'booked_seats': booked_seats}, status=status.HTTP_200_OK)



class BookingHistoryApi(APIView):
    def get(self, request):
        email = request.query_params.get('email')
        user = User.objects.get(email=email)
        bookings = Booking.objects.filter(user=user).select_related('show__movie')

        booking_history = []
        for booking in bookings:
            booking_history.append({
                'id': booking.id,
                'movie': booking.show.movie.name,
                'theatre': booking.show.theatre.name,
                'date': booking.show.date,
                'time': booking.show.time,
                'seats': booking.seats,
                'created_at': booking.created_at,
                'amount': booking.amount,
                'status': booking.status
            })

        return Response(booking_history, status=status.HTTP_200_OK)


class CreateRazorpayOrderAPIView(APIView):
    """
    API to create a Razorpay order.
    Expects: amount (in rupees), currency (default 'INR'), receipt (optional)
    """
    def post(self, request):
        amount = request.data.get('amount')
        currency = request.data.get('currency', 'INR')
        receipt = request.data.get('receipt', None)
        
        if not amount:
            return Response({'error': 'Amount is required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            # Razorpay expects amount in paise
            order_data = {
                'amount': int(amount),
                'currency': currency,
                'payment_capture': 1,
            }
            if receipt:
                order_data['receipt'] = receipt
            order = razorpay_client.order.create(data=order_data)
            return Response({'order': order}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

