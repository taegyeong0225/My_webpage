# from django.shortcuts import render
<<<<<<< HEAD
from django.shortcuts import render
=======
from .models import Post
>>>>>>> origin/main
from django.views.generic import ListView, DetailView
from .models import Post, Category

class PostList(ListView):
    # Generic view > generic display view > ListView
    model = Post
    # template_name = 'blog/post_list.html'
    # 안 적어주면 모델_list.html로 인식, 파일명을 변경함
    ordering = '-pk'

<<<<<<< HEAD
    # get_context_data 오버라이딩, 카테고리 파트 데이터 get
=======
    # get_context_data 오버라이딩
>>>>>>> origin/main
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PostList, self).get_context_data()
        context['categories'] = Category.objects.all()
        context['no_category_post_count'] = Post.objects.filter(category=None).count()

        return context
<<<<<<< HEAD


=======
>>>>>>> origin/main
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
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PostDetail, self).get_context_data()
        context['categories'] = Category.objects.all()
        context['no_category_post_count'] = Post.objects.filter(category=None).count()

        return context



def category_page(request, slug):
    '''
    FBV 방식
    :param slug:
    :return:
    '''
    if slug == 'no_category':
        category = '미분류'
        post_list = Post.objects.filter(category=None)
    else:
        category = Category.objects.get(slug=slug)
        post_list = Post.objects.filter(category=category)
    return render(
        request,
        'blog/post_list.html',
        {
            'post_list': post_list,
            'categories': Category.objects.all(),
            'no_category_post_count': Post.objects.filter(category=None).count(),
            'category': category,
        }
    )
    return render(
        request,
        'blog/post_list.html',
        {
            'post_list': Post.objects.filter(category=category),
            'categories': Category.objects.all(),
            'no category.post_count': Post.objects.filter(category=None).count(),
            'category': category,
        }
    )