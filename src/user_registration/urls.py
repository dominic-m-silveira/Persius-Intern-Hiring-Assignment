from django.urls import path, include
from django.contrib.auth.decorators import login_required
from .views import settings, UserDetailView, \
    UserDetailsUpdateView, UserProfileDetailsUpdateView, UserDeleteView
from allauth.account.views import EmailView as allauth_AccountEmail

urlpatterns = [
    path('accounts/email/', allauth_AccountEmail.as_view(), name='account_email'),
    path('accounts/', include('allauth.urls')),
    path('settings/', login_required(settings), name='settings'),
    path('settings/<slug>/update/', login_required(UserDetailsUpdateView.as_view()), name='upd-user'),
    path('settings/<slug>/delete/', login_required(UserDeleteView.as_view()), name='del-user'),
    path('settings/id/<int:pk>/update/', login_required(UserProfileDetailsUpdateView.as_view()), name='upd-profile'),
    path('profile/<slug>/', login_required(UserDetailView.as_view()), name='user-profile'),
]
