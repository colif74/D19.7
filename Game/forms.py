from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm, BooleanField
from .models import Post, Comment
from django import forms
from django.core.exceptions import ValidationError
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group, User


class PostForm(forms.ModelForm):
    title = forms.CharField(min_length=10)

    class Meta:
        model = Post
        fields = [
                'title',
                'context',
                'author',
                    ]

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get('title')
        contents = cleaned_data.get("context")
        if contents == title:
            raise ValidationError({"Содержание должно отлтчатся от заголовка"})
        return cleaned_data


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = [
            'text_comment',
            'author_comment',
                  ]


class BasicSignupForm(SignupForm):

    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        basic_group = Group.objects.get(name='common')
        basic_group.user_set.add(user)
        return user


class BaseRegisterForm(UserCreationForm):
    email = forms.EmailField(label="Email")
    first_name = forms.CharField(label="Имя")
    last_name = forms.CharField(label="Фамилия")

    class Meta:
        model = User
        fields = ("username",
                  "first_name",
                  "last_name",
                  "email",
                  "password1",
                  "password2", )
