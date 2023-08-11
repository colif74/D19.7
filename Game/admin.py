from django.contrib import admin
from .models import Author, Post, Comment, Category
# создаём новый класс для представления товаров в админке
class PostAdmin(admin.ModelAdmin):
    list_display = ('title','context', 'author')
    # оставляем только имя и цену товара
    list_filter = ('title','context', 'author')
    # добавляем примитивные фильтры в нашу админку
    search_fields = ('title', 'category__name')
    # тут всё очень похоже на фильтры из запросов в базу


admin.site.register(Author)
admin.site.register(Post, PostAdmin)
admin.site.register(Category)
admin.site.register(Comment)

# Register your models here.
