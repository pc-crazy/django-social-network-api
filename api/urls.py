from django.urls import path
from .views import SignupView, CustomLoginView, UserSearchView, SendFriendRequestView, UpdateFriendRequestView, \
    ListFriendsView, ListPendingRequestsView

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('search/', UserSearchView.as_view(), name='user_search'),
    path('friend-request/', SendFriendRequestView.as_view(), name='send_friend_request'),
    path('friend-request/<int:id>/', UpdateFriendRequestView.as_view(), name='update_friend_request'),
    path('friends/', ListFriendsView.as_view(), name='list_friends'),
    path('pending-requests/', ListPendingRequestsView.as_view(), name='list_pending_requests'),
]
