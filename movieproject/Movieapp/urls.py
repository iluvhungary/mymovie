from django.urls import path
from . import views

app_name = 'Movieapp'

urlpatterns = [
                path('', views.index, name='index'),
                path('register/', views.sign_up, name='sign_up'),
                path('sign_in/', views.sign_in, name='sign_in'),
                path('logout/', views.sign_out, name='sign_out'),
                path('movie/<int:movie_id>/', views.details, name='details'),
                path('add/', views.add_movie, name='add_movie'),
                path('update/<int:movie_id>/', views.update, name='update'),
                path('delete/<int:movie_id>/', views.delete, name='delete'),
                path('my-account/', views.my_account, name='my_account'),
                path('movies-added-by-user/', views.movies_added_by_user, name='movies_added_by_user'),
                path('genres/', views.genre_list, name='genre_list'),
                path('genres/<int:genre_id>/', views.genre_detail, name='genre_detail'),
                path('movies/year/<int:year>/', views.movies_by_year, name='movies_by_year'),
                path('top-rated/', views.top_imdb_rated, name='top_imdb_rated'),
                path('profile/edit/', views.profile_edit, name='profile_edit'),
                path('movie/<int:movie_id>/add_comment/', views.add_comment, name='add_comment'),
                path('filter_by_language/', views.filter_by_language, name='filter_by_language'),
 ]
