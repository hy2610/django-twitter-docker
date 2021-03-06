from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from comments.models import Comment
from comments.api.serializers import CommentsSerializerForCreate
from comments.api.serializers import CommentsSerializer
from comments.api.permissions import IsObjectOwner
from comments.api.serializers import CommentsSerializerForUpdate
from utils.decorators import require_params


class CommentsViewSets(viewsets.GenericViewSet):
    serializer_class = CommentsSerializerForCreate
    queryset = Comment.objects.all()
    filterset_fields = ('tweet_id',)

    def get_permissions(self):
        if self.action == 'create':
            return [IsAuthenticated()]
        if self.action in ['destroy', 'update']:
            return [IsAuthenticated(), IsObjectOwner()]
        return [AllowAny()]

    def create(self, request, *args, **kwargs):
        data = {
            'user_id': request.user.id,
            'tweet_id': request.data.get('tweet_id'),
            'content': request.data.get('content'),
        }
        # 注意这里必须要加 'data=' 来指定参数是传给 data 的
        # 因为默认的第一个参数是 instance
        serializer = CommentsSerializerForCreate(data=data)
        if not serializer.is_valid():
            return Response({
                'message': 'Please check input',
                'errors': serializer.errors,
            }, status=status.HTTP_400_BAD_REQUEST)
        # save 方法会触发 serializer 里的 create 方法，点进 save 的具体实现里可以看到
        comment = serializer.save()
        return Response(
            CommentsSerializer(comment, context={'request': request}).data,
            status=status.HTTP_201_CREATED,
        )

    def update(self, request, pk):
        serializer = CommentsSerializerForUpdate(
            instance=self.get_object(),
            data=request.data,
        )
        if not serializer.is_valid():
            return Response({
                'message': 'Please Check Input',
            }, status=400)
        comment = serializer.save()
        return Response(CommentsSerializer(comment, context={'request': request}).data, status=status.HTTP_200_OK)

    def destroy(self, request, pk):
        comment = self.get_object()
        comment.delete()

        return Response({
            'success': True,
        }, status=status.HTTP_200_OK)

    @require_params(params=['tweet_id'])
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        comments = self.filter_queryset(queryset).order_by('created_at')
        serializer = CommentsSerializer(
            comments,
            context={'request': request},
            many=True,
        )
        return Response(
            {'comments': serializer.data},
            status=status.HTTP_200_OK,
        )



