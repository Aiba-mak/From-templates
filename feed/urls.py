
from django.contrib import admin
from django.urls import path, include
from . import views
from .views import PostUpdate, PostDelete, PostList, UserPostList

urlpatterns=[
	path('', PostList.as_view(), name='home'),
	path('post/new/', views.create_post, name='post-create'),
	path('post/<int:pk>/', views.post_detail, name='post-detail'),
	path('like/', views.like, name='post-like'),
	path('post/<int:pk>/update/', PostUpdate.as_view(), name='post-update'),
	path('post/<int:pk>/delete/', PostDelete.as_view(), name='post-delete'),
	path('search_posts/', views.search_posts, name='search_posts'),
	path('user_posts/<str:username>', UserPostList.as_view(), name='user-posts'),
]