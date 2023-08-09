from django.shortcuts import render
from .models import Post

from django.views.generic import ListView

class PostList(ListView):
    # Generic view > generic display view > ListView
    model = Post
    # template_name = 'blog/post_list.html', 안 적어주면 모델_list.html로 인식
    ordering = '-pk'

# FBV 방식
# def index(request):
#     posts = Post.objects.all().order_by('-pk')

#     # QuerySet 출력
#     # print(posts)

#     return render(
#         request,
#         'blog/post_list.html', {
#             'posts': posts
#         }
#     )

def single_post_page(request, pk):
    post = Post.objects.get(pk=pk)
    return render(
        request,
        'blog/single_post_page.html', {
            'post': post,
        }
    )