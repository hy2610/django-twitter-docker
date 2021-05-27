from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from tweets.api.serializers import TweetSerializer, TweetSerializerForCreate
from tweets.models import Tweet
from newsfeed.services import NewsFeedService

class TweetViewSet(viewsets.GenericViewSet):
    serializer_class = TweetSerializerForCreate

    def get_permissions(self):
        if self.action == 'list':
            return [AllowAny()]
        return [IsAuthenticated()]

    def list(self, request):
        if 'user_id' not in request.query_params:
            return Response('missing user_id', status=400)
        tweets = Tweet.objects.filter(
            user_id=request.query_params['user_id'],
        ).order_by('-created_at')
        serializer = TweetSerializer(tweets, many=True)  # list of dicts
        return Response({
            'tweets': serializer.data
        })

    def create(self, request, *args, **kwargs):
        """
        重载 create 方法，因为需要默认用当前登录用户作为 tweet.user
        """
        serializer = TweetSerializerForCreate(
            data=request.data,
            context={'request': request},
        )
        if not serializer.is_valid():
            return Response({
                'success': False,
                'message': "Please check input",
                'errors': serializer.errors,
            }, status=400)
        tweet = serializer.save()
        NewsFeedService.fanout_to_followers(tweet)
        return Response(TweetSerializer(tweet).data, status=201)

