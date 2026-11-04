from django.test import TestCase
from django.urls import reverse

from accounts.models import CustomUser


class DashboardViewTests(TestCase):
	def test_dashboard_shows_member_count_and_admin_link(self):
		admin = CustomUser.objects.create_user(
			username="campusadmin",
			password="CampusConnect-password-2026!",
			role=CustomUser.Role.ADMIN,
		)
		CustomUser.objects.create_user(
			username="student",
			password="CampusConnect-password-2026!",
		)
		self.client.force_login(admin)

		response = self.client.get(reverse("dashboard"))

		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.context["member_count"], 2)
		self.assertTrue(response.context["is_admin"])
		self.assertContains(response, reverse("admin_panel"))

	def test_admin_panel_is_for_admins_only(self):
		student = CustomUser.objects.create_user(
			username="student",
			password="CampusConnect-password-2026!",
		)
		self.client.force_login(student)

		response = self.client.get(reverse("admin_panel"))

		self.assertEqual(response.status_code, 403)
