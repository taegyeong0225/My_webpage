from django.urls import path
from . import views

urlpatterns = [
    # 클래스형 뷰 사용 명시
    path('', views.PostList.as_view()),
    path('<int:pk>/', views.PostDetail.as_view()),
    path('category/<str:slug>/', views.category_page),
    # path('<int:pk>/', views.single_post_page),
    # path('', views.index),
]