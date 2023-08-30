from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils.text import slugify
from django.utils.timezone import now

from accounts.models import User

class Category(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=200, unique=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Category, self).save(*args, **kwargs)

class Module(models.Model):
    title = models.CharField(max_length=100)
    video = models.FileField(upload_to='videos/', null=True)
    text = models.TextField(blank=True)
    course = models.ForeignKey('Course', on_delete=models.CASCADE, related_name='modules')

    def __str__(self):
        return self.title

class Course(models.Model):
    title = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    slug = models.SlugField(max_length=200, unique=True, primary_key=True, auto_created=False)
    short_description = models.TextField(blank=False, max_length=60)
    description = models.TextField(blank=False)
    outcome = models.CharField(max_length=200)
    requirements = models.CharField(max_length=200)
    language = models.CharField(max_length=200)
    price = models.FloatField(validators=[MinValueValidator(9.99)])
    level = models.CharField(max_length=20)
    thumbnail = models.ImageField(upload_to='thumbnails/')
    video_url = models.CharField(max_length=100)
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=now)
    updated_at = models.DateTimeField(default=now)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Course, self).save(*args, **kwargs)

# class Lesson(models.Model):
#     course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')
#     title = models.CharField(max_length=100)
#     duration = models.FloatField(validators=[MinValueValidator(0.20), MaxValueValidator(30.00)])
#     chapter1 = models.FileField(upload_to='videos/', null=True)
#     chapter2 = models.FileField(upload_to='videos/', null=True)
#     chapter3 = models.FileField(upload_to='videos/', null=True)
#     chapter4 = models.FileField(upload_to='videos/', null=True)
#     chapter5 = models.FileField(upload_to='videos/', null=True)
#     created_at = models.DateTimeField(default=now)
#     updated_at = models.DateTimeField(default=now)

    def __str__(self):
        return self.title


    