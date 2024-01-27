from django.shortcuts import render
from rest_framework.decorators import api_view,permission_classes,authentication_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework.permissions import AllowAny
from rest_framework import status
from .models import *
from .serializers import *
from django.contrib.auth import authenticate,login
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authentication import TokenAuthentication


@ api_view(['POST'])
@csrf_exempt
def author_signup(request):
    serializer=AuthorSerializer(data=request.data)
    if serializer.is_valid():
        user=serializer.save()
        response_data = {
            'user_id': user.id,
            'registration_code': user.author.registration_code,
            'message': 'Author registered successfully.'
        }
        return Response(response_data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def common_login(request):
    username=request.data.get('username')
    password=request.data.get('password')

    if not username or not password:
        return Response({'error': 'Both username and password are required.'}, status=status.HTTP_400_BAD_REQUEST)

    user=authenticate(request,username=username,password=password)

    if user is not None:
        login(request,user)
        response_data={
            'user_id': user.id,
            'username': user.username,
            'message': 'Login successful.'

        }
        return Response(response_data, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Invalid credentials.'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
@permission_classes([IsAdminUser])
def add_genre(request):
    serializer = GenreSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'Genre added successfully.'}, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAdminUser])
def get_all_authors(request):
    authors = Author.objects.all()
    serializer = AuthorSerializer(authors, many=True)

    authors_data = []
    for author_data in serializer.data:
        # Include books data for each author
        author = Author.objects.get(id=author_data['id'])
        books = Book.objects.filter(author=author)
        book_serializer = BookSerializer(books, many=True)
        author_data['books'] = book_serializer.data
        authors_data.append(author_data)
    return Response(authors_data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAdminUser])
def get_author_details(request, author_id):
    try:
        author = Author.objects.get(id=author_id)
    except Author.DoesNotExist:
        return Response({'error': 'Author not found.'}, status=status.HTTP_404_NOT_FOUND)

    serializer = AuthorSerializer(author)
    author_data = serializer.data

    # Include books data for the author
    books = Book.objects.filter(author=author)
    book_serializer = BookSerializer(books, many=True)
    author_data['books'] = book_serializer.data

    return Response(author_data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def get_books_of_author(request, author_id):
    try:
        author = Author.objects.get(id=author_id)
    except Author.DoesNotExist:
        return Response({'error': 'Author not found.'}, status=status.HTTP_404_NOT_FOUND)

    books = Book.objects.filter(author=author)
    serializer = BookSerializer(books, many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def delete_genre(request, genre_id):
    try:
        genre = Genre.objects.get(id=genre_id)
    except Genre.DoesNotExist:
        return Response({'error': 'Genre not found.'}, status=status.HTTP_404_NOT_FOUND)

    genre.delete()

    return Response({'message': 'Genre deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_book(request):
    # Get the authenticated author
    author = request.user.author

    # Add the author to the request data before serializing
    request.data['author'] = author.id

    serializer = BookSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'Book added successfully.'}, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def edit_book(request, book_id):
    try:
        book = Book.objects.get(id=book_id)
    except Book.DoesNotExist:
        return Response({'error': 'Book not found.'}, status=status.HTTP_404_NOT_FOUND)

    # Check if the authenticated user is the owner of the book
    if request.user.author != book.author:
        return Response({'error': 'You do not have permission to edit this book.'}, status=status.HTTP_403_FORBIDDEN)

    serializer = BookSerializer(book, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'Book edited successfully.'}, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAdminUser])
def export_books_by_genre(request, genre_id):
    try:
        books = Book.objects.filter(genre_id=genre_id)
    except Genre.DoesNotExist:
        return Response({'error': 'Genre not found.'}, status=status.HTTP_404_NOT_FOUND)

    serializer = BookSerializer(books, many=True)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_all_authors_protected(request):
    authors = Author.objects.all()
    serializer = AuthorSerializer(authors, many=True)

    authors_data = []
    for author_data in serializer.data:
        # Include books data for each author
        author = Author.objects.get(id=author_data['id'])
        books = Book.objects.filter(author=author)
        book_serializer = BookSerializer(books, many=True)
        author_data['books'] = book_serializer.data
        authors_data.append(author_data)

    return Response(authors_data)
from django.shortcuts import render
