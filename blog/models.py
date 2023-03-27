from django.db import models

from django.core.validators import MinLengthValidator

# Create your models here.


class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=254)

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"
    
class Tag(models.Model):

    caption = models.CharField(max_length=50)

    def __str__(self) -> str:
        return f'{self.caption}'
    

class Post(models.Model):
    title = models.CharField(max_length=50)
    excerpt = models.CharField(max_length=200)
    image = models.ImageField(upload_to='image', null=True)
    date = models.DateField(auto_now=True, auto_now_add=False)
    slug = models.SlugField(unique=True, db_index=True)
    content = models.TextField(validators=[MinLengthValidator(10)])
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, related_name='posts', null=True)
    tag = models.ManyToManyField(Tag)
 
    def __str__(self) -> str:
        return f'{self.title}, {self.date}'

class Comments(models.Model):
    user_name = models.CharField(max_length=50)
    user_email = models.EmailField(max_length=254)
    comment_imput = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')


