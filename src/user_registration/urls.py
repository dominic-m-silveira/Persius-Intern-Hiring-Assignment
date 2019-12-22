from django.urls import path, include
from django.contrib.auth.decorators import login_required
from .views import home, secret_page, settings, UserDetailView, UserFollowView, UserFollowRemoveView, \
    UserDetailsUpdateView, UserProfileDetailsUpdateView, UserDeleteView
from allauth.account.views import EmailView as allauth_AccountEmail

urlpatterns = [
    path('', home, name='home'),
    path('secret/', secret_page, name='secret'),
    path('accounts/email/', allauth_AccountEmail.as_view(), name='account_email'),
    path('accounts/', include('allauth.urls')),
    path('settings/', login_required(settings), name='settings'),
    path('settings/<slug>/update/', login_required(UserDetailsUpdateView.as_view()), name='upd-user'),
    path('settings/<slug>/delete/', login_required(UserDeleteView.as_view()), name='del-user'),
    path('settings/id/<int:pk>/update/', login_required(UserProfileDetailsUpdateView.as_view()), name='upd-profile'),
    path('profile/<slug>/', login_required(UserDetailView.as_view()), name='user-profile'),
    path('profile/<slug>/follow/', login_required(UserFollowView.as_view()), name='user-follow'),
    path('profile/<slug>/followremove/', login_required(UserFollowRemoveView.as_view()), name='user-follow-remove'),
]
