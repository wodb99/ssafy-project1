from django.urls import path
from . import views

urlpatterns = [
    # 전체 게시글 조회/ 생성
    path('', views.article_list),
    # 단일 게시글/ 조회/ 수정/ 삭제
    path('<int:article_pk>/', views.article_detail),
    # 전체 댓글 조회
    path('comments/', views.comment_list),
    # 단일 댓글 조회/ 수정/ 삭제
    path('comments/<int:comment_pk>/', views.comment_detail),
    # 단일 게시글에서 댓글 생성
    path('<int:article_pk>/comments/', views.comment_create),
]
