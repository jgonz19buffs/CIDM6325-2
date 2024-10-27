from django.urls import path
from django.utils.translation import gettext_lazy as _
from . import views
from .feeds import LatesPostsFeed

app_name = 'blog'

urlpatterns = [
    # post views
    path('', views.list, name='list'),
    path(_('posts/'), views.post_list, name='post_list'),
    # path('', views.PostListView.as_view(), name='post_list'),
    path(
        _('posts/<int:year>/<int:month>/<int:day>/<slug:post>/'), 
        views.post_detail, 
        name='post_detail'
    ),
    path(_('<int:post_id>/share/'), views.post_share, name='post_share'),
    path(
        _('<int:post_id>/comment'), views.post_comment, name='post_comment'
    ),
    path(
        'tag/<slug:tag_slug>/', views.post_list, name='post_list_by_tag'
    ), 
    path(_('feed/'), LatesPostsFeed(), name='post_feed'),
    path(_('search/'), views.post_search, name='post_search'),
    path(_('recipes/'), views.recipe_list, name='recipe_list'),
    path(_('recipes/<int:year>/<int:month>/<int:day>/<slug:recipe>'),
         views.recipe_detail,
         name='recipe_detail'),
    path(
        _('<int:recipe_id>/review'), views.recipe_review, name='recipe_review'
    ),
        path(
        _('cuisineType/<slug:tag_slug>/'), views.recipe_list, name='recipe_list_by_cuisineType'
    ), 
]