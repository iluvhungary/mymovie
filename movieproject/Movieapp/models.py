from django.db import models
from django.contrib.auth.models import User
# Create your models here.
#I need a table for my movie project with name,description and year
class Movie(models.Model):
    title = models.CharField(max_length=100, default='Default Title')
    poster = models.ImageField(upload_to='gallery', default='default_poster.jpg')
    desc = models.TextField(default='Default Description')
    release_date = models.DateTimeField(default='2024-01-01 00:00:00')
    actors = models.TextField(default='Actor 1, Actor 2')
    category = models.CharField(max_length=100, default='Default Category')
    youtube_trailer_link = models.URLField(default='https://www.youtube.com/')
    creator = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    imdb_rating = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    LANGUAGE_CHOICES = [
        ('malayalam', 'Malayalam'),
        ('hindi', 'Hindi'),
        ('english', 'English'),
    ]

    language = models.CharField(max_length=50, choices=LANGUAGE_CHOICES, default='english')
    # language = models.CharField(max_length=50,
    #                             choices=[('malayalam', 'Malayalam'), ('hindi', 'Hindi'), ('english', 'English')])


    def __str__(self):
        return self.title

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=250)
    email = models.EmailField()


    def __str__(self):
        return self.user.username

class Genre(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey('Movie', on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.user.username} on {self.movie.title}'
