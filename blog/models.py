from django.db import models

from django.utils.text import slugify
from django.conf import settings
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver


def upload_location(instance, filename):
    file_path = "blog/{author_id}/{title}-{filename}".format(
        author_id=str(instance.author_id), title = str(instance.title), filename=filename
    )

    return file_path

class Post(models.Model):

    title               = models.CharField(max_length=50, null=False, blank=False, unique=True)
    subtitle            = models.CharField(max_length=100, null=True, blank=False, unique=True)
    body                = models.TextField(max_length=5000, null=False, blank=False)
    # image               = models.ImageField(upload_to=upload_location, null=False, blank=False)
    date_published      = models.DateTimeField(auto_now_add=True, verbose_name='Date published')
    date_updated        = models.DateTimeField(auto_now=True, verbose_name='Date updated')
    author              = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    slug                = models.SlugField(blank=True, unique=True)

    def __str__(self):
        return self.title

# @receiver(post_delete, sender=Post)
# def submission_delete(sender, instance, **kwargs):
#     instance.image.delete(False)

def pre_save_post_reciever(sender, instance, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.author.username + '-' + instance.title)

pre_save.connect(pre_save_post_reciever, sender=Post)

# class CommentModel(models.Model):
#     user = models.CharField(max_length=20)
#     comment_text = models.TextField()
#     blog = models.ForeignKey('Post', on_delete=models.CASCADE)
    
#     def __str__(self):
#         return f"Comment by Name: {self.user}"