from django.shortcuts import get_object_or_404, render, redirect
from django.db.models import Q
from django.http import HttpResponse
# from django.urls import reverse_lazy

from .models import Post
from .forms import CreatePostForm, UpdatePostForm
from authentication.models import Account
from operator import attrgetter
from django.core.paginator import EmptyPage, Paginator, PageNotAnInteger

from .models import Post
# Create your views here.



def view_posts(request):
    context = {}

    posts = sorted(Post.objects.all(), key=attrgetter('date_published'), reverse=True)

    context['posts'] = posts

    return render(request, 'blog/posts.html', context)


def create_post_view(request):
    context = {}

    user = request.user
    if not user.is_authenticated:
        return redirect('signup')

    form = CreatePostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        obj = form.save(commit=False)
        author = Account.objects.filter(username=user.username).first()
        obj.author = author
        obj.save()
        return redirect('home')

    form = CreatePostForm()
    context['post_form'] = form

    return render(request, 'blog/create_post.html', context)

def post_detail_view(request, slug):

    # user = request.user
    # if not user.is_authenticated:
    #     return redirect('home')

    context = {}

    post = get_object_or_404(Post, slug=slug)

    context['post'] = post

    return render(request, 'blog/post_detail.html', context)

def delete_post_view(request, slug):
    
    user = request.user
    if not user.is_authenticated:
        return redirect('home')

    context = {}

    
    post = get_object_or_404(Post, slug=slug)

    if post.author != user.username:
        return HttpResponse("You are not the author of that post.")

    if request.method == 'POST':
        post.delete()
        return redirect('home')
    
    return render(request, 'blog/delete_post.html', context)


def edit_post_view(request, slug):
    
    user = request.user
    if not user.is_authenticated:
        return redirect('home')
        
    context = {}
    
    post = get_object_or_404(Post, slug=slug)
    
    if post.author != user.username:
        return HttpResponse("You are not the author of that post.")
   
    if request.POST:
        form = UpdatePostForm(request.POST or None, request.FILES or None, instance=post)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()

            context['success_message'] = 'Updated Successfully!'
            post = obj
    form = UpdatePostForm(
        initial = {
            "title": post.title,
            "subtitle": post.subtitle,
            "body": post.body,
            "image": post.image
        }
    )

    context['form'] = form

    return render(request, 'blog/edit_post.html', context)
