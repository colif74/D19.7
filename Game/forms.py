from .models import *
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.core.exceptions import ValidationError
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group, User
# from ckeditor.widgets import CKEditorWidget


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = [
                'titles',
                'posttext',
                'author',
                'video_count',
                'image_count',
                    ]

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get('titles')
        contents = cleaned_data.get("posttext")
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



# class AdForm(forms.ModelForm):
#     title = forms.CharField(
#         widget=forms.TextInput(attrs={'class': 'form-control'}),
#         min_length=20,
#         max_length=128,
#         label='Заголовок'
#     )
#     context = forms.CharField(
#         widget=CKEditorUploadingWidget(),
#         label='Содержание'
#     )
#     category = forms.ModelChoiceField(
#         queryset=Category.objects.all(),
#         widget=forms.Select(attrs={'class': 'form-control'}),
#         empty_label='Выберите категорию',
#         label='Категория',
#     )
#
#     class Meta:
#         model = Post
#         fields = [
#             'headline',
#             'text',
#             'category',
#         ]
#
#         labels = {
#             # 'category': _('Категория'),
#         }
#
#     def clean(self):
#         cleaned_data = super().clean()
#         headline = cleaned_data.get("headline")
#         text = cleaned_data.get("text")
#
#         if headline == text:
#             raise ValidationError(
#                 "Заголовок не должен быть идентичен содержанию!"
#             )
#         return cleaned_data
#



class CommentDeleteForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = []


class BasicSignupForm(SignupForm):

    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        basic_group = Group.objects.get(name='common')
        basic_group.user_set.add(user)
        return user


class BaseRegisterForm(UserCreationForm):
    email = forms.EmailField(label="Email")

    class Meta:
        model = User
        fields = ("username",
                  "first_name",
                  "last_name",
                  "email",
                  "password1",
                  "password2",

                  )
