from django.urls import path
from . import views

urlpatterns = [
    path('', views.PostList.as_view()),
    # 클래스형 뷰 사용 명시
    path('<int:pk>/', views.single_post_page),
    # path('', views.index),
]
