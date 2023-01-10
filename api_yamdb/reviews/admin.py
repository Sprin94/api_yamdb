from django.contrib import admin

from reviews.models import Review, Comment, Category, Genre, Title


admin.site.register(Review)
admin.site.register(Comment)
admin.site.register(Category)
admin.site.register(Genre)
admin.site.register(Title)
