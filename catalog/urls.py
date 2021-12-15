from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('books/', views.BookListView.as_view(), name='books'),
    path('authors/', views.AuthorListView.as_view(), name='authors'),
    path('book/<int:pk>', views.BookDetailView.as_view(), name='book-detail'),
    path('mybooks/<int:userid>', views.LoanedBooksByUserListView.as_view(), name='my-borrowed'),
    path('borrowed/', views.AllLoanedBooksListView.as_view(), name='borrowed'),
    path('book/<uuid:pk>/renew/', views.renew_book_librarian, name='renew-book-librarian'),
    path('book/<uuid:pk>/return/', views.return_book_librarian, name='return-book-librarian'),
    path('book/<uuid:pk>/loan/', views.loan_book_librarian, name='loan-book-librarian'),
    path('book/<uuid:pk>/borrow/', views.borrow_book, name='borrow-book'),
    path('book/<int:pk>/review/', views.review_book, name='review-book'),
]