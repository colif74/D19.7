from django.db import models
from django.contrib.auth.models import User
import datetime
from django.urls import reverse


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


class Author(models.Model):
    object = None
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user}'


class Category(models.Model):
    objects = None
    names = models.CharField(max_length=20, choices=GAME_CATEGORY, default='Gamer', help_text='category name')
    subscribers = models.ManyToManyField(User, blank=True, null=True, related_name='subscribers')

    def __str__(self):
        return self.names


class Post(models.Model):
    object = None
    titles = models.CharField(max_length=255)
    posttext = models.TextField(blank=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    category = models.ManyToManyField(to=Category, through='PostCategory', related_name='PostCategory')
    video_count = models.FileField(upload_to='videos',default=0)
    image_count = models.FileField(upload_to='images', default=0)

    def preview(self):
        return f"{self.context[:124]}..."

    def __str__(self):
        return f'{self.title.title()}:{self.context[:20]}'

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.pk)])


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    objects = None
    text_comment = models.TextField(blank=True)
    comment_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author_comment = models.ForeignKey(User, on_delete=models.CASCADE)
    approved = models.BooleanField(default=False)


class Appointment(models.Model):
    date = models.DateField(default=datetime)
    client_name = models.CharField(max_length=200)
    message = models.TextField(default=True)

    def __str__(self):
        return f'{self.client_name}: {self.message}'
