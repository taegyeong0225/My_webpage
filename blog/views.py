# from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin # 로그인했을 때만 정상적으로 페이지가 보이게 해주는 클래스
from django.views.generic import ListView, DetailView, CreateView
from .models import Post, Category, Tag

class PostList(ListView):
    # Generic view > generic display view > ListView
    model = Post
    # template_name = 'blog/post_list.html'
    # 안 적어주면 모델_list.html로 인식, 파일명을 변경함
    ordering = '-pk'

    # get_context_data 오버라이딩, 카테고리 파트 데이터 get
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PostList, self).get_context_data()
        context['categories'] = Category.objects.all()
        context['no_category_post_count'] = Post.objects.filter(category=None).count()

        # 현재 요청의 slug 값을 가져와서 context에 추가
        context['slug'] = self.kwargs.get('category_slug')

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
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PostDetail, self).get_context_data()
        context['categories'] = Category.objects.all()
        context['no_category_post_count'] = Post.objects.filter(category=None).count()

        return context


class PostCreate(LoginRequiredMixin, CreateView):
    '''
    폼을 만드는 클래스
    fields는 장고의 폼(form) 클래스를 생성할 때 사용되는 필드들을 지정하는 속성
    post_form 템플릿 필요
    '''
    model = Post
    fields = ['title', 'hook_text', 'content', 'head_image', 'file_upload', 'category']

    def form_valid(self, form):
        current_user = self.request.user # 방문자
        if current_user.is_authenticated: # 로그인 상태인지 확인하는 메소드
            form.instance.author = current_user # instance :  새로 생성한 포스트
            return super(PostCreate, self).form_valid(form)
        else:
            return redirect('/blog/')

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


def tag_page(request, slug):
    tag = Tag.objects.get(slug=slug)
    post_list = tag.post_set.all()

    return render(
        request,
        'blog/post_list.html',
        {
            'post_list': post_list,
            'tag': tag,
            'categories': Category.objects.all(),
            'no_category_post_count': Post.objects.filter(category=None).count(),
        }
    )