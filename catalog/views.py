import datetime

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.db import connection, transaction
from .models import Book, Author, BookInstance, Genre, Review

from django.contrib.auth.forms import UserCreationForm
from catalog.forms import RenewBookForm, LoanBookForm, ReviewBookForm
 

def register(request):  
    if request.POST == 'POST':  
        form = UserCreationForm()  
        print("New user is being created.")
        if form.is_valid():  
            form.save()
            print("New user should have been created.")
            messages.success(request, 'Account created successfully')  

    else:  
        form = UserCreationForm()  
        context = {  
            'form':form  
        }  
    return render(request, 'register.html', context)  


@login_required
def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    # Available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()

    # The 'all()' is implied by default.
    num_authors = Author.objects.count()

    genres = Genre.objects.all()
    num_genres = {}
    for genre in genres:
      num_genres[genre.name] = Book.objects.filter(genre__name__exact=genre.name).count()

    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_genres': num_genres,
        'num_visits': num_visits
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)


@login_required
def loan_book_librarian(request, pk):
    book_instance = get_object_or_404(BookInstance, pk=pk)

    # If this is a POST request then process the Form data
    if request.method == 'POST':
        # Create a form instance and populate it with data from the request (binding):
        form = LoanBookForm(request.POST)
        # Check if the form is valid:
        # if form.is_valid():
        # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
        # book_instance.due_back = form.cleaned_data['renewal_date']
        User = get_user_model()
        book_instance.due_back = request.POST['return_date']
        book_instance.borrower = User.objects.filter(id=request.POST['borrower']).first()
        book_instance.status = 'o'
        book_instance.save()
        # redirect to a new URL:
        return HttpResponseRedirect(reverse('borrowed') )

    # If this is a GET (or any other method) create the default form.
    else:
        proposed_return_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = LoanBookForm(initial={'return_date': proposed_return_date})

    context = {
        'form': form,
        'book_instance': book_instance,
    }

    return render(request, 'catalog/book_loan_librarian.html', context)

@login_required
def borrow_book(request, pk):
    book_instance = get_object_or_404(BookInstance, pk=pk)

    book_instance.due_back = datetime.date.today() + datetime.timedelta(weeks=3)
    book_instance.borrower = request.user
    book_instance.status = 'o'
    book_instance.save()

    return HttpResponseRedirect(reverse('my-borrowed', args=(request.user.id,)) )


@login_required
def renew_book_librarian(request, pk):
    book_instance = get_object_or_404(BookInstance, pk=pk)

    # If this is a POST request then process the Form data
    if request.method == 'POST':
        # Create a form instance and populate it with data from the request (binding):
        form = RenewBookForm(request.POST)
        # Check if the form is valid:
        # if form.is_valid():
        # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
        # book_instance.due_back = form.cleaned_data['renewal_date']
        book_instance.due_back = request.POST['renewal_date']
        book_instance.save()
        # redirect to a new URL:
        return HttpResponseRedirect(reverse('borrowed') )

    # If this is a GET (or any other method) create the default form.
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})

    context = {
        'form': form,
        'book_instance': book_instance,
    }

    return render(request, 'catalog/book_renew_librarian.html', context)

@login_required
def return_book_librarian(request, pk):
    book_instance = get_object_or_404(BookInstance, pk=pk)

    book_instance.due_back = None
    book_instance.borrower = None
    book_instance.status = 'a'
    book_instance.save()

    return HttpResponseRedirect(reverse('borrowed') )

@login_required
def review_book(request, pk):
    book = get_object_or_404(Book, pk=pk)

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        # form = ReviewBookForm(request.POST)
        # Check if the form is valid:
        # if form.is_valid():
        # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
        # book_instance.due_back = form.cleaned_data['renewal_date']
        text_content = '<p><b>' 
        for x in range(int(request.POST['stars'])):
            text_content += '*'
        text_content += '</b> - ' + request.POST['review_text'] + '<br/> -' + request.user.username + '</p>'
        
        review = Review(book=book, text_content=text_content)
        review.save()

        # redirect to a new URL:
        return HttpResponseRedirect(reverse('book-detail', args=(pk,)) )

    # If this is a GET (or any other method) create the default form.
    else:
        form = ReviewBookForm()

    context = {
        'form': form,
        'book': book,
    }

    return render(request, 'catalog/book_review.html', context)

class BookListView(LoginRequiredMixin, generic.ListView):
    model = Book
    ordering = ['author', 'title']
    paginate_by = 10


class BookDetailView(LoginRequiredMixin, generic.DetailView):
    model = Book
    
    def get_context_data(self, **kwargs):
        context = super(BookDetailView, self).get_context_data(**kwargs)
        print(self.kwargs)
        print(Review.objects.all())
        context['reviews'] = Review.objects.filter(book=Book.objects.get(id=self.kwargs['pk']))
        return context


class AuthorListView(LoginRequiredMixin, generic.ListView):
    model = Author


class LoanedBooksByUserListView(LoginRequiredMixin,generic.ListView):
    model = BookInstance
    template_name ='catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        # return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')
        return BookInstance.objects.filter(borrower=self.kwargs['userid']).filter(status__exact='o').order_by('due_back')


# class AllLoanedBooksListView(LoginRequiredMixin,PermissionRequiredMixin,generic.ListView):
class AllLoanedBooksListView(LoginRequiredMixin,generic.ListView):
    # permission_required = 'catalog.can_mark_returned'
    model = BookInstance
    template_name ='catalog/bookinstance_list_borrowed_all.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='o').order_by('due_back')