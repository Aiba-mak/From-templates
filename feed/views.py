from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.urls import reverse
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from .serializers import NewCommentSerializer, NewPostSerializer
# from django.views.generic import ListView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Post, Comments, Like
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
import json
import random
from rest_framework.response import Response
# from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.decorators import api_view

class PostList(APIView):
	queryset = Post.objects.all()
	model = Post
	context_object_name = 'posts'
	ordering = ['-date_posted']
	paginate_by = 10
	serializer_class = NewPostSerializer


	def get_context_data(self, **kwargs):
		context = super(PostList, self).get_context_data(**kwargs)
		if self.request.user.is_authenticated:
			liked = [i for i in Post.objects.all() if Like.objects.filter(user = self.request.user, post=i)]
			context['liked_post'] = liked
		return context
		
class UserPostList(LoginRequiredMixin, APIView):
	model = Post
	queryset = Post.objects.all()
	context_object_name = 'posts'
	paginate_by = 10
	serializer_class = NewPostSerializer

	def get_context_data(self, **kwargs):
		context = super(UserPostList, self).get_context_data(**kwargs)
		user = get_object_or_404(User, username=self.kwargs.get('username'))
		liked = [i for i in Post.objects.filter(user_name=user) if Like.objects.filter(user = self.request.user, post=i)]
		context['liked_post'] = liked
		return Response({"data": "Request has no 'content_type' or 'object_id' field"})

	def get_queryset(self):
		user = get_object_or_404(User, username=self.kwargs.get('username'))
		return Post.objects.filter(user_name=user).order_by('-date_posted')


@login_required
def post_detail(request, pk):
	post = get_object_or_404(Post, pk=pk)
	user = request.user
	is_liked =  Like.objects.filter(user=user, post=post)
	if request.method == 'POST':
		form = NewCommentForm(request.POST)
		if form.is_valid():
			data = form.save(commit=False)
			data.post = post
			data.username = user
			data.save()
			return redirect('post-detail', pk=pk)
	else:
		form = NewCommentForm()
	return Response() #Что делать дальше

@login_required
def create_post(request):
	user = request.user
	if request.method == "POST":
		form = NewPostSerializer(request.POST, request.FILES)
		if form.is_valid():
			data = form.save(commit=False)
			data.user_name = user
			data.save()
			messages.success(request, f'Posted Successfully')
			return redirect('home')
	else:
		form = NewPostSerializer()
	return Response

class PostUpdate(LoginRequiredMixin, UserPassesTestMixin, APIView):
	model = Post
	queryset = Post.objects.all()
	fields = ['description', 'pic', 'tags']
	serializer_class = NewPostSerializer

	def form_valid(self, form):
		form.instance.user_name = self.request.user
		return super().form_valid(form)

	def test_func(self):
		post = self.get_object()
		if self.request.user == post.user_name:
			return True
		return False

class PostDelete(LoginRequiredMixin, UserPassesTestMixin, APIView):
	model = Post
	queryset = Post.objects.all()
	success_url = '/'
	serializer_class = NewPostSerializer

	def test_func(self):
		post = self.get_object()
		if self.request.user == post.user_name:
			return True
		return False


@login_required
def search_posts(request):
	query = request.GET.get('p')
	object_list = Post.objects.filter(tags__icontains=query)
	liked = [i for i in object_list if Like.objects.filter(user = request.user, post=i)]
	context ={
		'posts': object_list,
		'liked_post': liked
	}
	return Response()

@login_required
def like(request):
	post_id = request.GET.get("likeId", "")
	user = request.user
	post = Post.objects.get(pk=post_id)
	liked= False
	like = Like.objects.filter(user=user, post=post)
	if like:
		like.delete()
	else:
		liked = True
		Like.objects.create(user=user, post=post)
	resp = {
        'liked':liked
    }
	response = json.dumps(resp)
	return HttpResponse(response, content_type = "application/json")


