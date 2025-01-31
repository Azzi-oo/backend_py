from rest_framework.test import APITestCase
from rest_framework import status
import json

from general.factories import ChatFactory, MessageFactory, UserFactory
from general.models import Comment, Message, Post, Chat


class MessageTestCase(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.client.force_authenticate(user=self.user)
        self.url = "/api/messages/"
        
    def test_create_message(self):
        chat = ChatFactory(user_1=self.user)
        data = {
            "chat": chat.pk,
            "content": "Тестовое сообщение",
        }
        response = self.client.post(self.url, data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        message = Message.objects.last()
        self.assertEqual(message.author, self.user)
        self.assertEqual(message.chat, chat)
        self.assertEqual(message.content, data["content"])
        
    def test_try_to_create_message_for_other_chat(self):
        chat = ChatFactory()
        data = {
            "chat": chat.pk,
            "content": "Тестовое сообщение.",
        }
        response = self.client.post(self.url, data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        self.assertEqual(Message.objects.count(), 0)