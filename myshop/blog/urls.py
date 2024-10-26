from django.urls import path
from . import views
from .feeds import LatesPostsFeed

app_name = 'blog'

urlpatterns = [
    # post views
    path('', views.list, name='list'),
    path('posts/', views.post_list, name='post_list'),
    # path('', views.PostListView.as_view(), name='post_list'),
    path(
        'posts/<int:year>/<int:month>/<int:day>/<slug:post>/', 
        views.post_detail, 
        name='post_detail'
    ),
    path('<int:post_id>/share/', views.post_share, name='post_share'),
    path(
        '<int:post_id>/comment', views.post_comment, name='post_comment'
    ),
    path(
        'tag/<slug:tag_slug>/', views.post_list, name='post_list_by_tag'
    ), 
    path('feed/', LatesPostsFeed(), name='post_feed'),
    path('search/', views.post_search, name='post_search'),
    path('recipes/', views.recipe_list, name='recipe_list'),
    path('recipes/<int:year>/<int:month>/<int:day>/<slug:recipe>',
         views.recipe_detail,
         name='recipe_detail'),
    path(
        '<int:recipe_id>/review', views.recipe_review, name='recipe_review'
    ),
        path(
        'cuisineType/<slug:tag_slug>/', views.recipe_list, name='recipe_list_by_cuisineType'
    ), 
]