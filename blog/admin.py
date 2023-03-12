from django.contrib import admin

from .models import Author, Post, Tag

# Register your models here.

class PostSlug(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('author', 'title', 'date')
    list_filter = ('author', 'tag', 'date', )

class AuthorAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email',)


admin.site.register(Author, AuthorAdmin)
admin.site.register(Post, PostSlug)
admin.site.register(Tag)