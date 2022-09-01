from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.views.generic.base import TemplateView
from django.shortcuts import redirect

from .models import Group, Post, User

from posts.forms import PostForm


def index(request):
    posts = Post.objects.select_related('group')[:Post.OUTPUT_OF_POSTS]
    paginator = Paginator(posts, Post.OUTPUT_OF_POSTS)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'posts': posts,
        'title': 'Последние обновления на сайте',
        'page_obj': page_obj,
    }

    return render(request, 'posts/index.html', context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = group.posts.all()[:Post.OUTPUT_OF_POSTS]
    paginator = Paginator(posts, Post.OUTPUT_OF_POSTS)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'group': group,
        'posts': posts,
        'page_obj': page_obj,
    }
    return render(request, 'posts/group_list.html', context)


class JustStaticPage(TemplateView):
    template_name = 'app_name/just_page.html'


def profile(request, username):
    template = 'posts/profile.html'
    user = get_object_or_404(User, username=username)
    profile_list = Post.objects.filter(author=user)
    count_posts = profile_list.count()
    paginator = Paginator(profile_list, Post.OUTPUT_OF_POSTS)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'author': user,
               'profile_list': profile_list,
               'count_posts': count_posts,
               'page_obj': page_obj,

               }

    return render(request, template, context)


def post_detail(request, post_id):
    template = 'posts/post_detail.html'
    post = get_object_or_404(Post, id=post_id)
    context = {'post': post,
               }

    return render(request, template, context)


def post_create(request):
    template = 'posts/create_post.html'
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('posts:profile', post.author)
    else:
        form = PostForm()
    return render(request, template, {'form': form})


def post_edit(request, post_id):
    template = 'posts/create_post.html'
    post = get_object_or_404(Post, id=post_id)
    form = PostForm(instance=post)
    context = {
        'is_edit': True,
        'form': form
    }
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('posts:post_detail', post_id)
    else:
        return render(request, template, context)
