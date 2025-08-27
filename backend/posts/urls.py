from django.urls import path
from .views import PostListCreateView, PostDetailUpdateDeleteView

app_name = 'posts'

urlpatterns = [
    path('', PostListCreateView.as_view(), name='post-list-create'),
    path('<slug:slug>/', PostDetailUpdateDeleteView.as_view(), name='post-detail-update-delete'),
] 