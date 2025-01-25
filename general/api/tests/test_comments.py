from rest_framework.test import APITestCase
from rest_framework import status
import json

from general.factories import CommentFactory, PostFactory, ReactionFactory, UserFactory
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
        
    def test_pass_incorrect_post_id(self):
        data = {
            "post": self.post.pk + 1,
            "body": "comment body",
        }
        response = self.client.post(
            path=self.url,
            data=data,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_delete_own_comment(self):
        comment = CommentFactory(author=self.user)
        response = self.client.delete(
            f"{self.url}{comment.pk}/",
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Comment.objects.count(), 0)
        
    def test_delete_other_comment(self):
        comment = CommentFactory()
        response = self.client.delete(
            f"{self.url}{comment.pk}/",
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Comment.objects.count(), 1)
        self.assertEqual(
            response.data["detail"],
            "Вы не являетесь автором этого коммента.",
        )
        
    def test_comment_list_filtered_by_post_id(self):
        comments = CommentFactory.create_batch(5, post=self.post)
        
        CommentFactory.create_batch(5)
        
        url = f"{self.url}?post__id={self.post.pk}"
        response = self.client.get(path=url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 5)  
        
        comments_ids = {comment.id for comment in comments}
        for comment in response.data["results"]:
            self.assertTrue(comment["id"] in comments_ids)