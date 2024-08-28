from django.urls import path, re_path
from .views import *


urlpatterns = [
    path('register/', RegisterUser.as_view(), name='register'),
    path('login/', LoginUser.as_view(), name='login'),
    path('users/', UserList.as_view(), name='users'),
    path('send-friend-request/', SendFriendRequest.as_view(), name='send_friend_request'),
    path('accept-friend-request/', AcceptFriendRequest.as_view(), name='accept_friend_request'),
    path('reject-friend-request/', RejectFriendRequest.as_view(), name='reject_friend_request'),
    path('list-friends/', ListFriends.as_view(), name='list_friends'),
    path('list-pending-requests/', ListPendingRequests.as_view(), name='list_pending_requests'),

]