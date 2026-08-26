from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse

from chat.models import Conversation, Message
from unittest.mock import patch

from reports.models import Report


class ReportChatFlowTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('patient', password='A secure test password 123!')
        self.other_user = User.objects.create_user('other', password='A secure test password 123!')
        self.client.force_login(self.user)

    def upload(self, name='Blood test'):
        return self.client.post(reverse('home'), {
            'name': name,
            'file': SimpleUploadedFile('blood.pdf', b'%PDF-1.7 test', content_type='application/pdf'),
        })

    @patch('reports.services.time.sleep')
    def test_upload_creates_owned_report_and_conversation(self, sleep):
        response = self.upload()
        conversation = Conversation.objects.get(user=self.user)
        self.assertRedirects(response, reverse('conversation', args=[conversation.id]))
        self.assertEqual(conversation.report.name, 'Blood test')
        self.assertEqual(conversation.report.status, Report.Status.COMPLETED)

    @patch('reports.services.time.sleep')
    def test_chat_stores_user_and_placeholder_messages(self, sleep):
        self.upload()
        conversation = Conversation.objects.get(user=self.user)
        response = self.client.post(reverse('conversation', args=[conversation.id]), {'content': 'What is next?'})
        self.assertRedirects(response, reverse('conversation', args=[conversation.id]))
        self.assertEqual(Message.objects.filter(conversation=conversation).count(), 2)

    @patch('reports.services.time.sleep')
    def test_other_user_cannot_access_conversation(self, sleep):
        self.upload('Private report')
        conversation = Conversation.objects.get(user=self.user)
        self.client.force_login(self.other_user)
        self.assertEqual(self.client.get(reverse('conversation', args=[conversation.id])).status_code, 404)