from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth import login, logout,authenticate
from django.template.loader import render_to_string
from django.urls import reverse
from .forms import LoginForm, ProfileEditForm
from .forms import UserProfileForm
from movieproject import settings
from django.contrib.auth.decorators import login_required
from .forms import MovieForm
from .forms import RegistrationForm
from .models import Movie, UserProfile, Genre, Comment
from django.contrib import auth
from .forms import CommentForm
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render


# Create your views here.
def sign_up(request):

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)

            # Send welcome email to user
            subject = 'Welcome to our website!'
            message = render_to_string('welcome_email.html', {'user': user})
            from_email = settings.EMAIL_HOST_USER
            to_email = [user.email]
            send_mail(subject, message, from_email, to_email)

            # Redirect to home page after registration
            return redirect('Movieapp:index')  # Redirect to home page after registration
    else:
        form = RegistrationForm()
    welcome_message = "Welcome to our website! You have successfully signed up."
    return render(request, 'register.html', {'form': form, 'welcome_message': welcome_message})


@login_required
def profile_view(request):
    user = request.user
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UserProfileForm(instance=user)

    return render(request, 'profile.html', {'form': form})


def sign_in(request):
    welcome_message = "Welcome back! You have successfully logged in."
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect(reverse('Movieapp:index')+ f'?welcome_message={welcome_message}')   # Redirect to the home page after successful login
            else:
                # Authentication failed, display error message
                return render(request, 'login.html', {'form': form, 'error_message': 'Invalid username or password.'})
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

@login_required
def sign_out(request):
    auth.logout(request)
    return redirect('/')


def index(request):
    welcome_message = request.GET.get('welcome_message', None)
    movies = Movie.objects.all()
    years = set(movie.release_date.year for movie in movies)  # Extract years from release dates
    # context = {'movie_list': movie}
    return render(request, 'index.html', {'movie_list': movies, 'welcome_message': welcome_message, 'years': years})

# def user_can_view_comments(user):
#     # Check if the user has the required permissions to view comments
#     # For example, if comments are tied to a specific group or permission
#     return user.has_perm('app.view_comments')

# @user_passes_test(user_can_view_comments)
def details(request, movie_id):
    # return HttpResponse('this is movie no %s' % movie_id)
    movie = Movie.objects.get(id=movie_id)
    # retrieving and passing the comments associated with the movie to the template context
    # comments = Comment.objects.filter(movie=movie)
    # return render(request, 'detail.html', {'movie': movie, 'comments': comments})
    return render(request, 'detail.html', {'movie': movie})
@login_required
def add_movie(request):
    if request.method == 'POST':
        form = MovieForm(request.POST, request.FILES)
        if form.is_valid():
            movie = form.save(commit=False)
            movie.creator = request.user
            movie.save()
            return redirect('Movieapp:details', movie_id=movie.id)
    else:
        form = MovieForm()
    return render(request, 'add.html', {'form': form})


# Ensure that only the creator can modify or delete a movie
@login_required
def update(request, movie_id):
    movie = Movie.objects.get(id=movie_id)
    if movie.creator != request.user:
        # Handle unauthorized access
        pass
    if request.method == 'POST':
        form = MovieForm(request.POST, request.FILES, instance=movie)
        if form.is_valid():
            form.save()
            return redirect('Movieapp:details', movie_id=movie.id)
    else:
        form = MovieForm(instance=movie)
    return render(request, 'edit.html', {'form': form})


@login_required
def delete(request, movie_id):
    movie = Movie.objects.get(id=movie_id)
    if movie.creator != request.user:
        # Handle unauthorized access
        pass
    if request.method == 'POST':
        movie.delete()
        return redirect('index')  # Redirect to the home page after deletion
    return render(request, 'delete.html', {'movie': movie})




@login_required
def my_account(request):
    user = request.user
    movies_added_by_user = Movie.objects.filter(creator=user)

    context = {

        'movies_added_by_user': movies_added_by_user
    }
    return render(request, 'my_account.html', context)


@login_required
def movies_added_by_user(request):
    # Retrieve movies added by the currently logged-in user
    if request.user.is_authenticated:
        user_movies = Movie.objects.filter(creator=request.user)
        return render(request, 'movies_added_by_user.html',  {'user_movies': user_movies})
    else:
        #Handle unauthenticated users (redirect to login page or show an error message)
        return render(request, 'error.html', {'message': 'Please log in to view your movies.'})


@login_required
def profile_edit(request):
    user = request.user
    profile = UserProfile.objects.get_or_create(user=user)[0]  # Get or create the profile object
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()  # Save the form data to the profile object
            return redirect('Movieapp:index')  # Redirect to the profile page after successful edit
    else:
        form = ProfileEditForm(instance=profile)  # Populate the form with the current profile data
    return render(request, 'edit_profile.html', {'form': form})



def genre_list(request):
    genres = Genre.objects.all()
    return render(request, 'genre_list.html', {'genres': genres})

def genre_detail(request, genre_id):
    genre = get_object_or_404(Genre, id=genre_id)
    # Assuming you have a ManyToManyField in your Movie model linking it to Genre
    movies_in_genre = genre.movie_set.all()
    return render(request, 'genre_detail.html', {'genre': genre, 'movies': movies_in_genre})

def movies_by_year(request, year):
    movies = Movie.objects.filter(release_date__year=year)
    return render(request, 'movies_by_year.html', {'movies': movies, 'year': year})

def top_imdb_rated(request):
    # Filter movies with IMDb ratings and order them by descending IMDb rating
    top_rated_movies = Movie.objects.exclude(imdb_rating=None).order_by('-imdb_rating')
    return render(request, 'top_imdb_rated_movies.html', {'top_rated_movies': top_rated_movies})

def filter_by_language(request):
    # Get the selected language from the request parameters
    language = request.GET.get('language')

    # Retrieve movies based on the selected language
    if language:
        filtered_movies = Movie.objects.filter(language=language)
    else:
        # If no language is selected, return all movies
        filtered_movies = Movie.objects.all()

    # Render the template with the filtered movies
    return render(request, 'movies_listing.html', {'filtered_movies': filtered_movies})

def add_comment(request, movie_id):
    movie = Movie.objects.get(pk=movie_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.movie = movie
            comment.save()
            # Redirect to the 'details' URL pattern with the appropriate movie_id
            return redirect('Movieapp:details',  movie_id=movie_id)
    else:
        form = CommentForm()
        # Redirect to the 'details' URL pattern with the appropriate movie_id
    return redirect('Movieapp:details', movie_id=movie_id)