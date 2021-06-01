from testing.testcases import TestCase
from rest_framework.test import APIClient

COMMENT_URL = '/api/comments/'


class CommentsApiTest(TestCase):

    def setUp(self):
        self.linghu = self.create_user(username='linghu')
        self.linghu_client = APIClient()
        self.linghu_client.force_authenticate(self.linghu)
        self.dongxie = self.create_user(username='dongxie')
        self.dongxie_client = APIClient()
        self.dongxie_client.force_authenticate(self.dongxie)

        self.tweet = self.create_tweet(self.linghu)

    def test_create(self):

        response = self.anonymous_client.post(COMMENT_URL)
        self.assertEqual(response.status_code, 403)

        response = self.linghu_client.post(COMMENT_URL)
        self.assertEqual(response.status_code, 400)

        response = self.linghu_client.post(COMMENT_URL, {'tweet_id': self.tweet.id})
        self.assertEqual(response.status_code, 400)

        response = self.linghu_client.post(COMMENT_URL, {'content': 'dsaasdasd'})
        self.assertEqual(response.status_code, 400)

        response = self.linghu_client.post(COMMENT_URL, {
            'tweet_id': self.tweet.id,
            'content': '1'*200,
        })
        self.assertEqual(response.status_code, 400)

        response = self.linghu_client.post(COMMENT_URL, {
            'tweet_id': self.tweet.id,
            'content': '1',
        })
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['user']['id'], self.linghu.id)
        self.assertEqual(response.data['tweet_id'], self.tweet.id)
        self.assertEqual(response.data['content'], '1')