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

    @patch('reports.services.requests.post')
    def test_upload_creates_owned_report_and_conversation(self, post):
        post.return_value.json.return_value = {'status': 'completed'}
        post.return_value.raise_for_status.return_value = None
        response = self.upload()
        conversation = Conversation.objects.get(user=self.user)
        self.assertRedirects(response, reverse('conversation', args=[conversation.id]))
        self.assertEqual(conversation.report.name, 'Blood test')
        self.assertEqual(conversation.report.status, Report.Status.COMPLETED)

    @patch('reports.services.requests.post')
    def test_chat_stores_user_and_placeholder_messages(self, post):
        post.return_value.json.return_value = {'status': 'completed'}
        post.return_value.raise_for_status.return_value = None
        self.upload()
        conversation = Conversation.objects.get(user=self.user)
        response = self.client.post(reverse('conversation', args=[conversation.id]), {'content': 'What is next?'})
        self.assertRedirects(response, reverse('conversation', args=[conversation.id]))
        self.assertEqual(Message.objects.filter(conversation=conversation).count(), 2)

    @patch('reports.services.requests.post')
    def test_other_user_cannot_access_conversation(self, post):
        post.return_value.json.return_value = {'status': 'completed'}
        post.return_value.raise_for_status.return_value = None
        self.upload('Private report')
        conversation = Conversation.objects.get(user=self.user)
        self.client.force_login(self.other_user)
        self.assertEqual(self.client.get(reverse('conversation', args=[conversation.id])).status_code, 404)

    def test_reports_page_shows_only_owned_reports(self):
        report = Report.objects.create(
            user=self.user,
            name='My report',
            file=SimpleUploadedFile('mine.pdf', b'%PDF-1.7 test', content_type='application/pdf'),
        )
        Report.objects.create(
            user=self.other_user,
            name='Private report',
            file=SimpleUploadedFile('private.pdf', b'%PDF-1.7 test', content_type='application/pdf'),
        )

        response = self.client.get(reverse('reports_index'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'My report')
        self.assertNotContains(response, 'Private report')
        report.file.delete(save=False)

    def test_owner_can_delete_report_and_file(self):
        report = Report.objects.create(
            user=self.user,
            name='Delete me',
            file=SimpleUploadedFile('delete-me.pdf', b'%PDF-1.7 test', content_type='application/pdf'),
        )
        file_name = report.file.name

        response = self.client.post(reverse('delete_report', args=[report.id]))

        self.assertRedirects(response, reverse('reports_index'))
        self.assertFalse(Report.objects.filter(id=report.id).exists())
        self.assertFalse(report.file.storage.exists(file_name))

    def test_other_user_cannot_delete_report(self):
        report = Report.objects.create(
            user=self.user,
            name='Keep private',
            file=SimpleUploadedFile('keep.pdf', b'%PDF-1.7 test', content_type='application/pdf'),
        )
        self.client.force_login(self.other_user)

        response = self.client.post(reverse('delete_report', args=[report.id]))

        self.assertEqual(response.status_code, 404)
        self.assertTrue(Report.objects.filter(id=report.id).exists())
        report.file.delete(save=False)