from django.shortcuts import render
from .models import Post

def index(request):
    posts = Post.objects.all().order_by('-pk')

    # QuerySet 출력
    # print(posts)

    return render(
        request,
        'blog/index.html', {
            'posts': posts
        }
    )

def single_post_page(request, pk):
    post = Post.objects.get(pk=pk)
    return render(
        request,
        'blog/single_post_page.html', {
            'posts': post,
        }
    )