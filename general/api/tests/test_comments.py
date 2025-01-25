from rest_framework.test import APITestCase
from rest_framework import status
import json

from general.factories import PostFactory, ReactionFactory, UserFactory
from general.models import Comment, Post, Reaction


class CommentTestCase(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.client.force_authenticate(user=self.user)
        self.post = PostFactory()
        self.url = "/api/comments/"
        
    def test_create_comment(self):
        data = {
            "post": self.post.pk,
            "body": "comment body",
        }
        response = self.client.post(
            path=self.url,
            data=data,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        comment = Comment.objects.last()
        self.assertEqual(data["post"], comment.post.id)
        self.assertEqual(data["body"], comment.body)
        self.assertEqual(self.user, comment.author)
        self.assertIsNotNone(comment.created_at)