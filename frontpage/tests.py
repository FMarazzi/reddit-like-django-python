# tests.py
from django.test import TestCase
from django.test.client import Client
import json
from .models import User, Discussion, Post


class TestPipeline(TestCase):
    def setUp(self):
        self.c = Client()

    def test_create_users(self):
        users = ["original_poster", "other_user", "third_user", "user_to_delete"]
        for user in users:
            json_string = u'{"username": "%s", "email": "%s@mail.it"}'%(user, user)
            response = self.c.post('/frontpage/create_user', json.loads(json_string), content_type="application/json")
            self.assertEqual(response.status_code, 200)

    def test_remove_users(self):
        self.test_create_users()
        user_to_delete = 4
        json_string = u'{"id": "%i"}' % user_to_delete
        json_data = json.loads(json_string)
        response = self.c.post('/frontpage/delete_user', json_data, content_type="application/json")
        self.assertEqual(response.status_code, 200)

    def test_create_discussion(self, title="first_discussion_title"):
        self.test_create_users()
        key_user = 1
        description = "This is the description relative to the first discussion."
        is_private = False
        json_string = u'{"key_user": "%i", "title":"%s", "description": "%s", "is_private": "%s"}' % (key_user, title, description, is_private)
        response = self.c.post('/frontpage/create_discussion', json.loads(json_string), content_type="application/json")
        self.assertEqual(response.status_code, 200)

    def test_remove_discussion(self):
        title = "discussion_to_remove"
        self.test_create_discussion(title)
        discussion_to_delete = "r/subreddit/%s"%title
        json_string = u'{"id": "%s"}' % discussion_to_delete
        response = self.c.post('/frontpage/remove_discussion', json.loads(json_string), content_type="application/json")
        self.assertEqual(response.status_code, 200)

    def test_create_post(self):
        title = "discussion_with_posts"
        self.test_create_discussion(title)
        key_user = 1
        key_discussion = "r/subreddit/%s" % title
        description = "This is a comment to the first discussion."
        json_string = u'{"key_user": "%i", "key_disc":"%s", "description": "%s"}' % (key_user, key_discussion, description)
        response = self.c.post('/frontpage/create_post', json.loads(json_string), content_type="application/json")
        self.assertEqual(response.status_code, 200)

    def test_remove_post(self):
        self.test_create_post()
        json_string = u'{"post": "1"}'
        response = self.c.post('/frontpage/remove_post', json.loads(json_string), content_type="application/json")
        self.assertEqual(response.status_code, 200)

    def test_private_discussion(self):
        discussion_title = "private_discussion"
        self.test_create_users()
        key_user = 1
        description = "This is the description relative to the first discussion."
        is_private = True
        json_string = u'{"key_user": "%i", "title":"%s", "description": "%s", "is_private": "%s"}' % (
        key_user, discussion_title, description, is_private)
        response = self.c.post('/frontpage/create_discussion', json.loads(json_string), content_type="application/json")
        self.assertEqual(response.status_code, 200)

        key_discussion = "r/subreddit/%s" % discussion_title
        for key_user in [2, 3]:
            json_string = u'{"key_user": "%i", "key_disc":"%s"}' % (key_user, key_discussion)
            response = self.c.post('/frontpage/add_contributor', json.loads(json_string), content_type="application/json")
            self.assertEqual(response.status_code, 200)
        for key_user in range(3):
            self.assertEqual(Discussion.objects.get(pk=key_discussion).user_can_contribute(User.objects.get(pk=key_user+1)),
                             True)
        self.assertEqual(
            Discussion.objects.get(pk=key_discussion).user_can_contribute(User.objects.get(pk=4)), False)

    def test_upvote_downvote_number_of_votes(self):
        discussion_title = "discussion_with_posts"
        self.test_create_post()
        key_post = "1"
        key_discussion = "r/subreddit/%s" % discussion_title
        votes = [1, -1, 1, -1, 1]
        for element, key in zip(["discussion", "post"], [key_discussion, key_post]):
            for vote in votes:
                json_string = u'{"element": "%s", "key_element": "%s", "upvoted": "%s"}' % (element, key, vote)
                response = self.c.post('/frontpage/vote', json.loads(json_string), content_type="application/json")
                self.assertEqual(response.status_code, 200)
        self.assertEqual(Post.objects.get(pk=int(key_post)).votes(), sum(votes))
        self.assertEqual(Discussion.objects.get(pk=key_discussion).votes(), sum(votes))


    def test_number_of_messages(self):
        discussion_title = "discussion_with_posts"
        self.test_create_discussion(discussion_title)
        key_user = 1
        key_discussion = "r/subreddit/%s" % discussion_title
        description = "This is a comment to the first discussion."
        n_mess = 4
        for _ in range(n_mess):
            json_string = u'{"key_user": "%i", "key_disc":"%s", "description": "%s"}' % (
            key_user, key_discussion, description)
            response = self.c.post('/frontpage/create_post', json.loads(json_string), content_type="application/json")
            self.assertEqual(response.status_code, 200)
        json_string = u'{"key_element": "%s"}' % key_discussion
        response = self.c.post('/frontpage/number_of_messages', json.loads(json_string), content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Discussion.objects.get(pk=key_discussion).number_of_messages(), n_mess)

    def test_number_of_partecipants(self):
        discussion_title = "discussion_with_posts"
        self.test_create_discussion(discussion_title)
        key_discussion = "r/subreddit/%s" % discussion_title
        description = "This is a comment to the first discussion."
        n_mess = 4
        for key_user in range(n_mess):
            json_string = u'{"key_user": "%i", "key_disc":"%s", "description": "%s"}' % (
                key_user+1, key_discussion, description)
            response = self.c.post('/frontpage/create_post', json.loads(json_string), content_type="application/json")
            self.assertEqual(response.status_code, 200)
        json_string = u'{"key_element": "%s"}' % key_discussion
        response = self.c.post('/frontpage/number_of_partecipants', json.loads(json_string),
                               content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Discussion.objects.get(pk=key_discussion).number_of_partecipants(), n_mess)

    def test_number_of_parents(self):
        discussion_title = "discussion_with_posts"
        self.test_create_post()
        key_user = 1
        key_discussion = "r/subreddit/%s" % discussion_title
        description = "This is a comment to the first discussion."
        n_mess = 4
        for k in range(1, n_mess+1):
            json_string = u'{"key_user": "%i", "key_disc":"%s", "key_parent": "%i", "description": "%s"}' % (
                key_user, key_discussion, k, description)
            response = self.c.post('/frontpage/create_post', json.loads(json_string), content_type="application/json")
            self.assertEqual(response.status_code, 200)
        json_string = u'{"key_element": "%s"}' % key_discussion
        response = self.c.post('/frontpage/number_of_messages', json.loads(json_string),
                               content_type="application/json")
        self.assertEqual(response.status_code, 200)
        for k in range(1, n_mess + 1):
            self.assertEqual(Post.objects.get(pk=k).number_of_parents(), k-1)
