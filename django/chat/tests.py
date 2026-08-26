from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Conversation
from reports.models import Report


class ChatNavigationTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('patient', password='A secure test password 123!')
        self.other_user = User.objects.create_user('other', password='A secure test password 123!')
        self.client.force_login(self.user)

    def create_conversation(self, user, name):
        report = Report.objects.create(user=user, name=name, file='reports/test.pdf')
        return Conversation.objects.create(user=user, report=report, title=f'Chat about {name}')

    def test_chats_nav_opens_latest_owned_conversation(self):
        latest = self.create_conversation(self.user, 'Latest report')
        response = self.client.get(reverse('chat_index'))
        self.assertRedirects(response, reverse('conversation', args=[latest.id]))

    def test_chats_nav_does_not_open_another_users_conversation(self):
        other_conversation = self.create_conversation(self.other_user, 'Private report')
        response = self.client.get(reverse('chat_index'))
        self.assertRedirects(response, reverse('home'))
        self.assertNotEqual(response.url, reverse('conversation', args=[other_conversation.id]))