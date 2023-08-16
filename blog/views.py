# from django.shortcuts import render
from django.shortcuts import render, redirect
# 로그인했을 때만 정상적으로 페이지가 보이게 해주는 클래스
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
# CreateView, UpdateView는 모델명_form.html을 사용함
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from .models import Post, Category, Tag

from django.core.exceptions import PermissionDenied
from django.utils.text import slugify

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


class PostCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    '''
    폼을 만드는 클래스
    fields는 장고의 폼(form) 클래스를 생성할 때 사용되는 필드들을 지정하는 속성
    post_form 템플릿 필요
    '''
    model = Post
    fields = ['title', 'hook_text', 'content', 'head_image', 'file_upload', 'category']

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff


    def form_valid(self, form):
        current_user = self.request.user # 방문자
        # is_authenticated: 로그인 상태인지 확인하는 메소드
        if current_user.is_authenticated and (current_user.is_staff or current_user.is_superuser):
            form.instance.author = current_user # instance :  새로 생성한 포스트
            response = super(PostCreate, self).form_valid(form)
            # form_valid() 함수는 폼 안에 들어온 값을 바탕으로 모델에 해당하는 인스턴스를 만들어 
            # 데이터베이스에 저장한 다음 그 인스턴스의 경로로 리다이렉트 함, 오버라이딩해서 작성자 정보, 태그 추가

            tags_str = self.request.POST.get('tags_str')
            if tags_str:
                tags_str = tags_str.strip()

                tags_str = tags_str.replace(',', ';')
                tags_list = tags_str.split(';')

                for t in tags_list:
                    t = t.strip()
                    tag, is_tag_created = Tag.objects.get_or_create(name=t)
                    if is_tag_created:
                        tag.slug = slugify(t, allow_unicode=True)
                        tag.save()
                    self.object.tags.add(tag) # 이번에 새로 만든 태그 self.object
            return response
        else:
            return redirect('/blog/')


class PostUpdate(LoginRequiredMixin, UpdateView):
    model = Post
    fields = ['title', 'hook_text', 'content', 'head_image', 'file_upload', 'category', 'tags']

    template_name = 'blog/post_update_form.html'

    # 방문자가 웹 사이트 서버에 get 방식으로 요청했는지 post 방식으로 요청했는지 판단하는 기능
    def dispatch(self, request, *args, **kwargs):
        # UpdateView의 메소드 : get_object()는 Post.objects.get(pk=pk)과 같은 역할을 함
        # Post 인스턴스(레코드)의 author 필드가 방문자와 동일한 경우에만 dispatch() 메소드가 원래 역할을 해야함
        if request.user.is_authenticated and request.user == self.get_object().author:
            return super(PostUpdate, self).dispatch(request, *args, **kwargs)
        else:
            # 권한이 없음을 나타냄, 타인의 포스트를 수정하려고 하면 403 메세지를 띄움
            raise PermissionDenied


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