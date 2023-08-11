# from django.shortcuts import render
from .models import Post
from django.views.generic import ListView, DetailView
from .models import Post, Category

class PostList(ListView):
    # Generic view > generic display view > ListView
    model = Post
    # template_name = 'blog/post_list.html'
    # 안 적어주면 모델_list.html로 인식, 파일명을 변경함
    ordering = '-pk'

    # get_context_data 오버라이딩
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PostList, self).get_context_data()
        context['categories'] = Category.objects.all()
        context['no_category_post_count'] = Post.objects.filter(category=None).count()

        return context
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

class PostDetail(DetailView):
    model = Post

# FBV 방식
# def single_post_page(request, pk):
    # post = Post.objects.get(pk=pk)
    # return render(
    #     request,
    #     'blog/post_detail.html', {
    #         'post': post,
    #     }
    # )