from django.test import TestCase
from django.urls import reverse


class HealthLensFlowTests(TestCase):
	def setUp(self):
		from django.contrib.auth.models import User

		self.user = User.objects.create_user(
			username='existing', password='A secure test password 123!'
		)

	def test_signup_redirects_to_dashboard(self):
		response = self.client.post(reverse('signup'), {
			'username': 'patient', 'email': 'patient@example.com',
			'password1': 'A secure test password 123!',
			'password2': 'A secure test password 123!',
		})
		self.assertRedirects(response, reverse('home'))

	def test_dashboard_requires_login(self):
		response = self.client.get(reverse('home'))
		self.assertRedirects(response, f'{reverse("login")}?next={reverse("home")}')

	def test_login_and_logout(self):
		response = self.client.post(reverse('login'), {
			'username': 'existing',
			'password': 'A secure test password 123!',
		})
		self.assertRedirects(response, reverse('home'))
		response = self.client.post(reverse('logout'))
		self.assertRedirects(response, reverse('login'))
