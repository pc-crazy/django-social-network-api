from django.db.models import Q
from rest_framework import generics, status, permissions
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.throttling import UserRateThrottle
from .models import User, FriendRequest
from django.contrib.auth import authenticate
from .serializers import (
    UserSerializer,
    SignupSerializer,
    FriendRequestSerializer,
    SendFriendRequestSerializer,
    UpdateFriendRequestSerializer,
    AuthTokenSerializer
)


class SignupView(generics.CreateAPIView):
    serializer_class = SignupSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        user = serializer.save()
        Token.objects.create(user=user)


class CustomLoginView(ObtainAuthToken):
    permission_classes = [permissions.AllowAny]
    serializer_class = AuthTokenSerializer

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')

        user = authenticate(request, username=email, password=password)

        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)


class UserSearchView(generics.ListAPIView):
    serializer_class = UserSerializer
    pagination_class = PageNumberPagination

    def get_queryset(self):
        query = self.request.query_params.get('q', '').strip()
        if query:
            exact_email_match = User.objects.filter(email__iexact=query)
            if exact_email_match.exists():
                return exact_email_match
            return User.objects.filter(Q(first_name__icontains=query) | Q(last_name__icontains=query))
        return User.objects.none()


class SendFriendRequestThrottle(UserRateThrottle):
    rate = '3/min'


class SendFriendRequestView(generics.CreateAPIView):
    serializer_class = SendFriendRequestSerializer
    throttle_classes = [SendFriendRequestThrottle]

    def perform_create(self, serializer):
        to_user_identifier = serializer.validated_data.get('to_user')
        try:
            recipient = User.objects.get(email=to_user_identifier)
        except User.DoesNotExist:
            try:
                recipient = User.objects.get(id=to_user_identifier)
            except (User.DoesNotExist, ValueError):
                return Response({'error': 'Recipient not found.'}, status=status.HTTP_400_BAD_REQUEST)
        if self.request.user.id == recipient.id:
            raise ValidationError({'error': 'You cannot send a friend request to yourself.'})

        existing_request = FriendRequest.objects.filter(from_user=self.request.user, to_user=recipient).exists()
        if existing_request:
            if existing_request.first().status == 'pending':
                raise ValidationError({'error': 'Friend request already sent to this user.'})
            elif existing_request.first().status == 'accepted':
                raise ValidationError({'error': 'You have a already friend'})
            else:
                FriendRequest.objects.filter(from_user=self.request.user, to_user=recipient).delete()
        serializer.save(from_user=self.request.user, to_user=recipient)


class UpdateFriendRequestView(generics.UpdateAPIView):
    queryset = FriendRequest.objects.all()
    serializer_class = UpdateFriendRequestSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'

    def patch(self, request, *args, **kwargs):
        friend_request = self.get_object()

        if friend_request.to_user != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)

        if friend_request.status != 'pending':
            return Response({'error': 'This friend request has already been processed.'},
                            status=status.HTTP_400_BAD_REQUEST)

        return super().patch(request, *args, **kwargs)


class ListFriendsView(generics.ListAPIView):
    serializer_class = FriendRequestSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = PageNumberPagination

    def get_queryset(self):
        return FriendRequest.objects.filter(from_user=self.request.user, status='accepted')


class ListPendingRequestsView(generics.ListAPIView):
    serializer_class = FriendRequestSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = PageNumberPagination

    def get_queryset(self):
        return FriendRequest.objects.filter(to_user=self.request.user, status='pending')
