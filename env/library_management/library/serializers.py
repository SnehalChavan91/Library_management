from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Author, Genre, Book

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class AuthorSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=True)

    class Meta:
        model = Author
        fields = ['id', 'user', 'name', 'phone', 'email', 'city', 'profile_image', 'registration_code']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create_user(**user_data)
        author = Author.objects.create(user=user, **validated_data)
        return author

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'name']

class BookSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(required=True)
    genre = GenreSerializer(required=True)

    class Meta:
        model = Book
        fields = ['id', 'author', 'name', 'genre', 'number_of_pages', 'cover_image']

    def create(self, validated_data):
        author_data = validated_data.pop('author')
        genre_data = validated_data.pop('genre')

        author = Author.objects.create(**author_data)
        genre = Genre.objects.get_or_create(**genre_data)[0]

        book = Book.objects.create(author=author, genre=genre, **validated_data)
        return book