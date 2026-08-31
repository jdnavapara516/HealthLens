from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class HealthLensFlowTests(TestCase):
	def setUp(self):
		User = get_user_model()
		self.user = User.objects.create_user(
			username='existing', email='existing@example.com', password='A secure test password 123!'
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

	def test_profile_page_requires_login(self):
		response = self.client.get(reverse('profile'))
		self.assertRedirects(response, f'{reverse("login")}?next={reverse("profile")}')

	def test_authenticated_nav_does_not_render_standalone_profile_link(self):
		self.client.login(username='existing', password='A secure test password 123!')
		response = self.client.get(reverse('home'))
		self.assertNotContains(response, 'class="nav-link" href="/profile/"')

	def test_profile_update_changes_user_details(self):
		self.client.login(username='existing', password='A secure test password 123!')
		response = self.client.post(reverse('profile'), {
			'username': 'existing',
			'email': 'updated@example.com',
		})
		self.assertRedirects(response, reverse('profile'))
		self.user.refresh_from_db()
		self.assertEqual(self.user.email, 'updated@example.com')

	def test_password_change_works(self):
		self.client.login(username='existing', password='A secure test password 123!')
		response = self.client.post(reverse('change_password'), {
			'old_password': 'A secure test password 123!',
			'new_password1': 'A new secure test password 456!',
			'new_password2': 'A new secure test password 456!',
		})
		self.assertRedirects(response, reverse('password_change_done'))
		self.user.refresh_from_db()
		self.assertTrue(self.user.check_password('A new secure test password 456!'))
