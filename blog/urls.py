from django.contrib import admin
from django.urls import path
from .views import (PostListView, PostDetailView,
PostDeleteView, MessageCreateView, MessageUpdateView, MessageDeleteView,
FilterPostListView, UserPostListView
)
from . import views

urlpatterns = [
    path('', PostListView.as_view(), name='blog'),
    path('new/', views.createnewpost, name='createnewpost'),
    path('post_edit/<int:pk>/', views.updatepost, name='post-update'),
    path('search_results', FilterPostListView.as_view(), name='search'),
    path('<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('<int:post_id>/message/', MessageCreateView.as_view(), name='message-create'),
    path('<int:pk>/message_update/', MessageUpdateView.as_view(), name='message-update'),
    path('<int:pk>/delete_message/', MessageDeleteView.as_view(), name='message-delete'),
    path('author/<str:email>', UserPostListView.as_view(), name='user-posts'),
]
