from django.contrib import admin
from django.urls import path
from .views import (PostListView, PostDetailView,
PostDeleteView, MessageCreateView, MessageUpdateView, MessageDeleteView,
PostSearchView, UserPostListView, PostThemesView, PostTagView
)
from . import views

urlpatterns = [
    path('', PostListView.as_view(), name='blog'),
    path('thread=<slug:category_slug>/', PostThemesView.as_view(), name='category-view'),
    path('new/', views.createnewpost, name='createnewpost'),
    path('post_edit/<int:pk>/', views.updatepost, name='post-update'),
    path('search_results', PostSearchView.as_view(), name='search'),
    path('tag=<slug:tag_slug>', PostTagView.as_view(), name='post-by-tag'),
    path('<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('<int:post_id>/message/', MessageCreateView.as_view(), name='message-create'),
    path('<int:pk>/message_update/', MessageUpdateView.as_view(), name='message-update'),
    path('<int:pk>/delete_message/', MessageDeleteView.as_view(), name='message-delete'),
    path('author/<str:email>', UserPostListView.as_view(), name='user-posts'),
]
