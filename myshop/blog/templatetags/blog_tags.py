from django import template
from django.db.models import Count
from django.utils.safestring import mark_safe
import markdown
from ..models import Post, Recipe

register = template.Library()

@register.simple_tag
def total_posts():
    return Post.published.count()

@register.simple_tag
def total_recipes():
    return Recipe.objects.all().count()

@register.inclusion_tag('blog/post/latest_posts.html')
def show_latest_posts(count=5):
    latest_posts = Post.published.order_by('-publish')[:count]
    return {'latest_posts': latest_posts}

@register.inclusion_tag('blog/recipe/latest_recipes.html')
def show_latest_recipes(count=5):
    latest_recipes = Recipe.published.order_by('-publish')[:count]
    return {'latest_recipes': latest_recipes}

@register.simple_tag
def get_most_commented_posts(count=5):
    return Post.published.annotate(
        total_comments=Count('comments')
    ).order_by('-total_comments')[:count]

@register.simple_tag
def get_most_reviewed_recipes(count=5):
    return Recipe.published.annotate(
        total_reviews=Count('reviews')
    ).order_by('-total_reviews')[:count]

@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(text))