from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class ImageFeed(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/')
    processed_image = models.ImageField(upload_to='processed_images/', null=True, blank=True)
    class_name = models.CharField(max_length=100, null=True, blank=True)
    confidence = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f'ImageFeed {self.id} by {self.user.username}'