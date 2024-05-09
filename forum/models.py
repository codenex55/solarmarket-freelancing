from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
from django_ckeditor_5.fields import CKEditor5Field

# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=200)
    # content = models.TextField()
    content = CKEditor5Field(blank=True, null=True, config_name="extends")
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date_posted = models.DateTimeField(auto_now_add=True)
    image = CloudinaryField('image', null=True, blank=True)

    def __str__(self):
        return self.title
    

class PostComment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date_posted = models.DateTimeField(auto_now_add=True)
    

class Question(models.Model):
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date_posted = models.DateTimeField(auto_now_add=True)
    image = CloudinaryField('image', default="https://res.cloudinary.com/dmpxni4ku/image/upload/v1714992400/default_question_image_vie1nx.webp")


class QuestionComment(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date_posted = models.DateTimeField(auto_now_add=True)
