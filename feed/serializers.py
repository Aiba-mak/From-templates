
from rest_framework import serializers
from .models import Comments, Post

class NewPostSerializer(serializers.ModelSerializer):
	class Meta:
		model = Post
		fields = ['description', 'pic', 'tags']

class NewCommentSerializer(serializers.ModelSerializer):

	class Meta:
		model = Comments
		fields = ['comment']