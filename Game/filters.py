from django_filters import FilterSet
from .models import *


# создаём фильтр
class PostFilter(FilterSet):

    class Meta:
        model = Post

        fields = {
            'title': ['icontains'],
            'context': ['icontains']
        }



class CommentFilter(FilterSet):

    class Meta:
        model = Comment

        fields = {
            'text_comment',
            'author_comment'
        }
