from rest_framework import serializers
from .models import Article, Comment


# 전체 게시글 직렬화
class ArticleListSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)
    class Meta:
        model = Article
        fields = (
            'id',
            'title',
            'content',
            'user_name'
        )
        

# 단일 게시글 직렬화
class ArticleSerializer(serializers.ModelSerializer):
    # 게시글하나(1) : 댓글들(N)
    class CommentDetailSerializer(serializers.ModelSerializer):
        class Meta:
            model = Comment
            fields = (
                'id',
                'content',
            )
    user_name = serializers.CharField(source='user.username', read_only=True)
    comment_set = CommentDetailSerializer(many=True, read_only=True)
    # comment_set : 역참조, count : 메서드
    comment_count = serializers.IntegerField(
        source = 'comment_set.count', read_only = True
    )
    class Meta:
        model = Article
        fields = '__all__'
        read_only_fields = ('user',)
        

class CommentSerializer(serializers.ModelSerializer):
    # 1. 댓글을 조회했을때 게시글의 제목도 같이 나오게
    class ArticleTitleSerializer(serializers.ModelSerializer):
        class Meta:
            model = Article
            fields = ('title', )
    # 댓글 조회했을 때 같이 응답받는 게시글의 제목은 읽기 전용
    article = ArticleTitleSerializer(read_only=True)
    user_name = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('user', 'article')
