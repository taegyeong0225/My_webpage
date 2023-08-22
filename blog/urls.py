from django.urls import path
from . import views

urlpatterns = [
    # 클래스형 뷰 사용 명시
    path('', views.PostList.as_view()),
    path('<int:pk>/', views.PostDetail.as_view()),
    path('category/<str:slug>/', views.category_page), # 카테고리 모인 페이지
    path('tag/<str:slug>/', views.tag_page), # 태그 모인 페이지
    path('create_post/', views.PostCreate.as_view()),
    path('update_post/<int:pk>/', views.PostUpdate.as_view()),
    path('update_comment/<int:pk>/', views.CommentUpdate.as_view()), # 댓글 수정 경로
    path('<int:pk>/new_comment/', views.new_comment), # 새 댓글 작성시
    # path('',)
    # path('<int:pk>/', views.single_post_page),
    # path('', views.index),
]