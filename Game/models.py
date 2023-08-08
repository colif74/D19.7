from django.contrib.auth.forms import UserCreationForm
from django.db import models
from django.contrib.auth.models import User
import datetime
from django.forms import forms

Tanks = 'TN'
Healers = 'HL'
DD = 'DD'
Merchants = 'ME'
GuildMasters = 'GM'
QuestGivers = 'QG'
Blacksmiths = 'BS'
Tanners = 'TS'
PotionMakers = 'PM'
SpellMasters = 'SM'

GAME_CATEGORY = [
    (Tanks, 'Танки'),
    (DD, 'ДД'),
    (Healers, 'Хиллы'),
    (Merchants, 'Торговцы'),
    (GuildMasters, 'Гилдмастера'),
    (QuestGivers, 'Квестгиверы'),
    (Blacksmiths, 'Кузнецы'),
    (Tanners, 'Кожевники'),
    (PotionMakers, 'Зельевары'),
    (SpellMasters, 'Мастера заклинаний'),
]


class Users(models.Model):
    object = None
    userses = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.userses.username


class Category(models.Model):
    objects = None
    names = models.CharField(max_length=20, choices = GAME_CATEGORY, default='Games', help_text='category name')
    subscribers = models.ManyToManyField(User, blank=True, null=True, related_name='subscribers')

    def __str__(self):
        return self.get_names_display()


class Post(models.Model):
    object = None
    title = models.CharField(max_length=255)
    context = models.TextField(blank=True)
    author = models.ForeignKey(Users, on_delete=models.CASCADE)
    category = models.ManyToManyField(to=Category, through='PostCategory', related_name='PostCategory')
    video_count = models.PositiveIntegerField(default=0)
    image_count = models.PositiveIntegerField(default=0)
    max_video_count = 1
    max_image_count = 3

    def add_video(self):
        if self.video_count >= self.max_video_count:
            raise ValueError("Превышено максимальное количество видео")
        self.video_count += 1

    def add_image(self):
        if self.image_count >= self.max_image_count:
            raise ValueError("Превышено максимальное количество изображений")
        self.image_count += 1

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return f'/post/{self.id}'

    def approved_comments(self):
        return self.Comment.filter(approved_comment=True)


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    objects = None
    text_comment = models.TextField(blank=True)
    comment_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author_comment = models.ForeignKey(User, on_delete=models.CASCADE)
    approved = models.BooleanField(default=False)

# class Appointment(models.Model):
#     date = models.DateField(
#         default=datetime.utcnow,
#     )
#     client_name = models.CharField(
#         max_length=200
#     )
#     message = models.TextField()
#
#     def __str__(self):
#         return f'{self.client_name}: {self.message}'
#

