from django import forms
from .models import Movie
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile
from .models import Comment


class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ['title', 'poster', 'desc', 'release_date', 'actors', 'category', 'imdb_rating','language', 'youtube_trailer_link']


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name', 'email']

class RegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField(max_length=254)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100,
                               widget=forms.TextInput
                               (attrs={'placeholder': 'Enter your username',
                                       'class': 'form-control', 'required': True}))
    password = forms.CharField(widget=forms.PasswordInput
                                    (attrs={'placeholder': 'Enter your password',
                                            'class': 'form-control', 'required': True}))

    def clean_username(self):
        username = self.cleaned_data['username']
        if not User.objects.filter(username=username).exists():
            raise forms.ValidationError('This username does not exist.')
        return username

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name', 'email']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
