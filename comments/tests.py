from testing.testcases import TestCase
from comments.models import Comment


# Create your tests here.
class CommentModelTests(TestCase):
    def test_comment(self):
        self.assertEqual(Comment.objects.count(), 0)
        user = self.create_user(username='linghu')
        tweet = self.create_tweet(user)
        comment = self.create_comment(user, tweet)
        self.assertNotEqual(comment.__str__(), None)
        self.assertEqual(Comment.objects.count(), 1)
