from django.urls import path
from .views import(
    author_signup,
    common_login,
    add_genre,
    get_all_authors,
    get_author_details,
    get_books_of_author,
    delete_genre,
    add_book,
    edit_book,
    export_books_by_genre,
)
urlpatterns = [
    path('author/signup/', author_signup, name='author_signup'),
    path('common/login/', common_login, name='common_login'),
    path('add/genre/', add_genre, name='add_genre'),
    path('get/all/authors/', get_all_authors, name='get_all_authors'),
    path('get/author/details/<int:author_id>/', get_author_details, name='get_author_details'),
    path('get/books/<int:author_id>/', get_books_of_author, name='get_books_of_author'),
    path('delete/genre/<int:genre_id>/', delete_genre, name='delete_genre'),
    path('author/add/book/', add_book, name='add_book'),
    path('author/edit/book/<int:book_id>/', edit_book, name='edit_book'),
    path('export/books/by/genre/<int:genre_id>/', export_books_by_genre, name='export_books_by_genre'),
]