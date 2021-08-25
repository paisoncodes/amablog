from django.shortcuts import render
from operator import attrgetter

from blog.models import Post

# Create your views here.

POSTPERPAGE = 5
def homepage_view(request):
    
    context = {}

    # query = ""
    # if request.GET:
    #     query = request.GET.get('q', '')
    #     context['query'] = str(query)
        
    posts = sorted(Post.objects.all(), key=attrgetter('date_updated'), reverse=True)

    # # pagination
    # page = request.GET.get('page', 1)
    # posts_paginator = Paginator(blog_posts, POSTPERPAGE)

    # try:
    #     blog_posts = posts_paginator.page(page)

    # except PageNotAnInteger:
    #     blog_posts = posts_paginator.page(POSTPERPAGE)

    # except EmptyPage:
    #     blog_posts = posts_paginator.page(posts_paginator.num_pages)


    context['posts'] = posts

    return render(request, 'index.html', context)


# def get_blog_queryset(query=None):
#     queryset = []
#     queries = query.split(" ")
#     for q in queries:
#         posts = Post.objects.filter(
#             Q(title__icontains=q) |
#             Q(body__icontains=q)
#         ).distinct()

#         for post in posts:
#             queryset.append(post)
#     return list(set(queryset))