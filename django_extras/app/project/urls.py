from django.urls import path
from .views import BooksListView, BooksDetailView, BooksCreateView, BookUpdateView, BookDeleteView

urlpatterns = [
    path("books/", BooksListView.as_view(template_name="books.html"), name="books"),
    path("books/<int:pk>", BooksDetailView.as_view(template_name="detail.html"), name="book"),
    path('books/create/', BooksCreateView.as_view(), name='book-create'),
    path('books/update/<slug:slug>', BookUpdateView.as_view(), name='book-update'),
    path('books/delete/<slug:slug>', BookDeleteView.as_view(), name='book-delete')
]
