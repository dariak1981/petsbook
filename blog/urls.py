from django.contrib import admin
from django.urls import path
from .views import (PostListView, PostDetailView,
PostDeleteView, MessageCreateView, MessageUpdateView, MessageDeleteView,
PostSearchView, UserPostListView, PostThemesView, PostTagView, PostLikeToggle,
)
from . import views

urlpatterns = [
    path('', PostListView.as_view(), name='blog'),
    path('thread=<slug:category_slug>/', PostThemesView.as_view(), name='category-view'),
    path('new/', views.createnewpost, name='createnewpost'),
    path('post_edit/<slug:slug>/', views.updatepost, name='post-update'),
    path('search_results', PostSearchView.as_view(), name='search'),
    path('tag=<slug:tag_slug>', PostTagView.as_view(), name='post-by-tag'),
    path('<slug:slug>/', PostDetailView.as_view(), name='post-detail'),
    path('<slug:slug>/like', PostLikeToggle.as_view(), name='like-toggle'),
    path('<slug:slug>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('<int:id>/message/', MessageCreateView.as_view(), name='message-create'),
    path('<int:id>/message_update/', MessageUpdateView.as_view(), name='message-update'),
    path('<int:id>/delete_message/', MessageDeleteView.as_view(), name='message-delete'),
    path('author/<str:username>', UserPostListView.as_view(), name='user-posts'),
]
