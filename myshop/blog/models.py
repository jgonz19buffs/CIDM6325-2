from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.core.validators import MaxValueValidator,MinValueValidator
from taggit.managers import TaggableManager

# Create your models here.

class PublishedManager(models.Manager):
    def get_queryset(self):
        if Post:
           return (
                super().get_queryset().filter(status=Post.Status.PUBLISHED)
            )
        
        if Recipe:
            return(
                super().get_queryset().filter(status=Recipe.Status.PUBLISHED)
            )
    
class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'

    title = models.CharField(max_length=250)
    slug = models.SlugField(
        max_length=250,
        unique_for_date='publish'
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='blog_posts'
    )
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=2,
        choices=Status,
        default=Status.DRAFT
    )
    objects = models.Manager() # The default manager.
    published = PublishedManager() # Our custom manager.

    class Meta:
        ordering = ['-publish']
        indexes = [
            models.Index(fields=['-publish']),
        ]

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse(
            'blog:post_detail',
            args=[
                self.publish.year,
                self.publish.month,
                self.publish.day,
                self.slug
            ]
        )
    tags = TaggableManager()
    
class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['created']
        indexes = [
            models.Index(fields=['created']),
        ]
    def __str__(self):
        return f'Comment by {self.name} on {self.post}'
    
class Recipe(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'

        #cuisineType = TaggableManager()
    class CuisineType(models.TextChoices):
        AFRICAN = 'AF', 'African'
        AMERICAN = 'US', 'American'
        CENTRALAMERICAN = 'CA','CentralAmerican'
        SOUTHAMERICAN = 'SA','SouthAmerican'
        CARIBBEAN = 'C','Caribbean'
        ASIAN = 'AS','Asian'
        EUROPEAN = 'EU','European'
        OTHER = 'O','Other'
    

    title = models.CharField(max_length=250)
    slug = models.SlugField(
        max_length=250,
        unique_for_date='publish'
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='blog_recipe'
    )
    ingredients = models.TextField()
    instructions = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=2,
        choices=Status,
        default=Status.DRAFT
    )
    objects = models.Manager() # The default manager.
    published = PublishedManager() # Our custom manager.
    cuisineType = models.CharField(
        max_length=2,
        choices=CuisineType,
        default=CuisineType.OTHER
    )
    
    class Meta:
        ordering = ['-publish']
        indexes = [
            models.Index(fields=['-publish']),
        ]

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse(
            'blog:recipe_detail',
            args=[
                self.publish.year,
                self.publish.month,
                self.publish.day,
                self.slug
            ]
        )

class Review(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    rating = models.PositiveIntegerField(
        validators=[
            MaxValueValidator(10),
            MinValueValidator(1)
        ]
    )
