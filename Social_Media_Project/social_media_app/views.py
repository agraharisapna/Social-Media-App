from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .pagination import CustomPageNumberPagination
from rest_framework import generics
from django.views.decorators.csrf import csrf_exempt
from rest_framework import filters
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.db.models import Q
from django.utils import timezone
from .serializers import *
import logging

logger = logging.getLogger(__name__)



class RegisterUser(APIView):
    
    @csrf_exempt
    def post(self, request, format=None):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            request_data = {'message':'User Registered Successfully.....', 
            'data':serializer.data}
            return Response(request_data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginUser(APIView):

    @csrf_exempt
    def post(self, request, format=None):
        email = request.data.get('email')
        password = request.data.get('password')

        try:
            verify_user = User.objects.get(email__iexact=email)
        except User.DoesNotExist:
            return Response({"message": "User with this email does not exist"}, status=status.HTTP_404_NOT_FOUND)
        
  
        if verify_user.check_password(password):
            login(request, verify_user)
            return Response({"message": "Login successful"}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Invalid password entered"}, status=status.HTTP_401_UNAUTHORIZED)


class UserList(generics.ListAPIView):

    permission_classes = [IsAuthenticated]
    pagination_class = CustomPageNumberPagination
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['=email','username']

class SendFriendRequest(APIView):
    permission_classes = [IsAuthenticated]

    @csrf_exempt
    def post(self, request, format=None):

        print(f"Request data: {request.data}")
        receiver_id = request.data.get('receiver_id')
        sender = request.user 

        if not receiver_id:
            return Response({"message": "Receiver ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            receiver = User.objects.get(id=receiver_id)
        except User.DoesNotExist:
            return Response({"message": "Receiver does not exist"}, status=status.HTTP_404_NOT_FOUND)

        if sender == receiver:
            return Response({"message": "Receiver and Sender can't be same."}, status=status.HTTP_400_BAD_REQUEST)

        one_minute_ago = timezone.now() - timezone.timedelta(minutes=1)
        recent_req = FriendRequest.objects.filter(sender=sender, timestamp__gte=one_minute_ago)

        if recent_req.count() >= 3:
            return Response({"message": "Cannot send more than 3 friend requests within a minute."},
                status=status.HTTP_429_TOO_MANY_REQUESTS)

        try:
            friend_req = FriendRequest(
                sender = sender,
                receiver = receiver
            )
            friend_req.save()
            return Response({"message": "Friend request sent"}, status=status.HTTP_201_CREATED)
        
        except ValidationError as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class AcceptFriendRequest(APIView):
    permission_classes = [IsAuthenticated]

    @csrf_exempt
    def post(self, request, format=None):
        request_id = request.data.get('request_id')
        user = request.user

        if not request_id:
            return Response({"message": "Request ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Check if the logged-in user is the receiver of the friend request
            friend_request = FriendRequest.objects.get(id=request_id, receiver=user)
        except FriendRequest.DoesNotExist:
            return Response({"message": "Friend request does not exist or is not for you"}, status=status.HTTP_404_NOT_FOUND)

        # Create the friendship
        Friendship.objects.create(
            user1=friend_request.sender,
            user2=friend_request.receiver
        )

        # Delete the friend request after acceptance
        friend_request.delete()

        return Response({"message": "Friend request accepted"}, status=status.HTTP_200_OK)


class RejectFriendRequest(APIView):
    permission_classes = [IsAuthenticated]

    @csrf_exempt
    def post(self, request, format=None):
        request_id = request.data.get('request_id')
        user = request.user

        if not request_id:
            return Response({"message": "Request ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Fetch the friend request where the logged-in user is the receiver
            friend_request = FriendRequest.objects.get(id=request_id, receiver=user)
        except FriendRequest.DoesNotExist:
            return Response({"message": "Friend request does not exist or is not for you"}, status=status.HTTP_404_NOT_FOUND)

        # Delete the friend request
        friend_request.delete()

        return Response({"message": "Friend request rejected"}, status=status.HTTP_200_OK)


class ListFriends(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FriendshipSerializer

    def get_queryset(self):
        user = self.request.user
        friends_list = Friendship.objects.filter(Q(user1=user) | Q(user2=user))
        return friends_list


class ListPendingRequests(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FriendRequestSerializer

    def get_queryset(self):
        user = self.request.user
        return FriendRequest.objects.filter(sender=user)










