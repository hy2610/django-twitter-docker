from testing.testcases import TestCase


# Create your tests here.
class CommentModelTests(TestCase):
    def test_comment(self):
        user = self.create_user(username='linghu')
        tweet = self.create_tweet(user)
        comment = self.create_comment(user, tweet)
        self.asserNotEqual(comment.__str__(), None)