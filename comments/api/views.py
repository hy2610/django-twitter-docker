from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from comments.models import Comment
from comments.api.serializers import CommentsSerializerForCreate
from comments.api.serializers import CommentsSerializer


class CommentsViewSets(viewsets.GenericViewSet):
    serializer_class = CommentsSerializerForCreate
    queryset = Comment.objects.all()

    def get_permissions(self):
        if self.action == 'create':
            return [IsAuthenticated()]
        return [AllowAny()]

    def create(self, request):
        data = {
            'user_id': request.user.id,
            'tweet_id': request.data.get('tweet_id'),
            'content': request.data.get('content'),
        }

        serializer = CommentsSerializerForCreate(data=data)
        if not serializer.is_valid():
            return Response({
                'success': False,
                'message': 'Please Check Input',
                'errors': serializer.errors,
            }, status=status.HTTP_400_BAD_REQUEST)
        comment = serializer.save()
        return Response(CommentsSerializer(comment).data, status=201)