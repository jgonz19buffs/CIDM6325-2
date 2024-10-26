from django.contrib.postgres.search import (
    SearchVector,
    SearchQuery,
    SearchRank
)
from django.contrib.postgres.search import TrigramSimilarity
from django.core.mail import send_mail
from django.core.paginator import EmptyPage, PageNotAnInteger,Paginator
from django.db.models import Count
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_POST
from django.views.generic import ListView
from taggit.models import Tag
from .forms import CommentForm, EmailPostForm, SearchForm, ReviewForm
from .models import Post, Recipe

# Create your views here.
def post_list(request, tag_slug=None):
    post_list = Post.published.all()
    tag=None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        post_list = post_list.filter(tags__in=[tag])

    # Pagination with 3 posts per page
    paginator = Paginator(post_list, 3)
    page_number = request.GET.get('page', 1)
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        # If page_number is not an integer get the first page
        posts = paginator.page(1)
    except EmptyPage:
        #If page_number is out of range get last page of results
        posts = paginator.page(paginator.num_pages)
    
    return render(
        request,
        'blog/post/list.html',
        {
            'posts': posts,
            'tag': tag,
            'section': 'posts'
        }
    )

def post_detail(request, year, month, day, post):
    post = get_object_or_404(
        Post,
        status = Post.Status.PUBLISHED,
        slug=post,
        publish__year=year,
        publish__month=month,
        publish__day=day
    )

    # List of active comments for this post
    comments = post.comments.filter(active=True)
    # Form for users to comment
    form = CommentForm()

    # List of similar posts
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(
        tags__in=post_tags_ids
    ).exclude(id=post.id)
    similar_posts = similar_posts.annotate(
        same_tags=Count('tags')
    ).order_by('-same_tags', '-publish')[:4]

    return render(
        request, 
        'blog/post/detail.html',
        {
            'post': post, 
            'comments': comments,
            'form': form, 
            'similar_posts': similar_posts
        }
    )

class PostListView(ListView):
    """
    Alternative post list view
    """
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'

def post_share(request, post_id):
    # Retrieve post by id
    post = get_object_or_404(
        Post,
        id=post_id,
        status=Post.Status.PUBLISHED
    )
    sent = False

    if request.method == 'POST':
        # Form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Form fields passed validation
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(
                post.get_absolute_url()
            )
            subject = (
                f"{cd['name']} ({cd['email']}) "
                f"recommends you read {post.title}"
            )
            message = (
                f"Read {post.title} at {post_url}\n\n"
                f"{cd['name']}\'s comments: {cd['comments']}"
            )
            send_mail(
                subject=subject,
                message=message,
                from_email=None,
                recipient_list=[cd['to']]
            )
            sent = True

    else:
        form = EmailPostForm()
    return render(
        request,
        'blog/post/share.html',
        {
            'post': post,
            'form': form,
            'sent': sent 
        }
    )

@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(
        Post,
        id=post_id,
        status=Post.Status.PUBLISHED
    )
    comment = None
    # A comment was posted
    form = CommentForm(data=request.POST)
    if form.is_valid():
        # Create a Comment object without saving ti to the database
        comment = form.save(commit=False)
        # Assign the post to the comment
        comment.post = post
        # Save the comment to the database
        comment.save()
    return render(
        request,
        'blog/post/comment.html',
        {
            'post' : post,
            'form' : form,
            'comment' : comment
        }
    )

def post_search(request):
    form = SearchForm()
    query = None
    results = []

    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            search_vector = SearchVector(
                'title', weight='A'
            ) + SearchVector('body', weight='B')
            search_query = SearchQuery(query, config='spanish')
            results = (
                Post.published.annotate(
                    similarity=TrigramSimilarity('title', query),
                )
                .filter(similarity__gt=0.1)
                .order_by('-similarity')
            )
    
    return render(
        request,
        'blog/post/search.html',
        {
            'form': form,
            'query': query,
            'results': results
        }
    )

def recipe_list(request,tag_slug=None):
    recipe_list = Recipe.objects.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        recipe_list = recipe_list.filter(cuisineType__in=[tag])
    # Pagination with 3 posts per page
    paginator = Paginator(recipe_list, 3)
    page_number = request.GET.get('page', 1)
    try:
        recipes = paginator.page(page_number)
    except PageNotAnInteger:
        # If page_number is not an integer get the first page
        recipes = paginator.page(1)
    except EmptyPage:
        # If page_number is out of range get last page of results
        recipes = paginator.page(paginator.num_pages)
    
    return render(
        request,
        'blog/recipe/list.html',
        {
            'recipes': recipes,
            'cuisineTypes':tag,
            'section': 'recipes'
        }
    )

def recipe_detail(request, year, month, day, recipe):

    recipe = get_object_or_404(
        Recipe, 
        status=Recipe.Status.PUBLISHED, 
        slug = recipe,
        publish__year=year,
        publish__month=month,
        publish__day=day
    )

    # List of active comments for this recipe
    reviews = recipe.reviews.filter(active=True)
    # Form for users to comment
    form = ReviewForm()

    # List of similar recipes
    #recipe_cuisineTypes_ids = recipe.cuisineType.values_list('id', flat=True)
    recipe_cuisineTypes_ids = recipe.cuisineType
    similar_recipes = Recipe.objects.all().filter(
        cuisineType__in=recipe_cuisineTypes_ids
    ).exclude(id=recipe.id)
    similar_recipes = similar_recipes.annotate(
        same_cuisineTypes=Count('cuisineType')
    ).order_by('-same_cuisineTypes', '-publish')[:4]

    return render(
        request,
        'blog/recipe/detail.html',
        {
            'recipe': recipe,
            'reviews': reviews,
            'form': form,
            'similar_recipes': similar_recipes
        }
    )

@require_POST
def recipe_review(request, recipe_id):
    recipe = get_object_or_404(
        Recipe,
        id=recipe_id,
        status=Recipe.Status.PUBLISHED
    )
    review = None
    # A comment was posted
    form = ReviewForm(data=request.POST)
    if form.is_valid():
        # Create a Comment object without saving ti to the database
        review = form.save(commit=False)
        # Assign the post to the comment
        review.recipe = recipe
        # Save the comment to the database
        review.save()
    return render(
        request,
        'blog/recipe/review.html',
        {
            'recipe' : recipe,
            'form' : form,
            'review' : review
        }
    )

def list(request, tag_slug=None):
    posts = Post.published.all()
    recipes = Recipe.objects.all()
    
    return render(
        request,
        'blog/list.html',
        {
            'posts': posts,
            'recipes': recipes
        }
    )