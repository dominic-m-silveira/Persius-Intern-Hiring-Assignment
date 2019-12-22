from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import PostDetailView, PostListAndCreateView, PostUpdateView, PostDeleteView

app_name = 'post'
urlpatterns = [
    # path('', home, name='home'),
    path('<int:pk>/', login_required(PostDetailView.as_view()), name='detail'),
    path('', login_required(PostListAndCreateView.as_view()), name='list'),
    path('<int:pk>/edit/', login_required(PostUpdateView.as_view()), name='update'),
    path('<int:pk>/delete/', login_required(PostDeleteView.as_view()), name='delete'),
]
