from django.shortcuts import render
from .models import Post

def index(request):
    posts = Post.objects.all().order_by('-pk')

    # QuerySet 출력
    # print(posts)

    return render(
        request,
        'blog/index.html', {
            'post': posts
        }
    )
