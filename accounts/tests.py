from django.test import TestCase
from django.urls import reverse

from .models import CustomUser


class SignUpViewTests(TestCase):
	def test_signup_creates_student_account(self):
		response = self.client.post(
			reverse("signup"),
			{
				"username": "newstudent",
				"first_name": "New",
				"last_name": "Student",
				"email": "student@example.com",
				"course": "Computer Science",
				"password1": "CampusConnect-password-2026!",
				"password2": "CampusConnect-password-2026!",
			},
			follow=True,
		)

		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.redirect_chain, [(reverse("login"), 302)])
		user = CustomUser.objects.get(username="newstudent")
		self.assertEqual(user.role, CustomUser.Role.STUDENT)
		self.assertTrue(user.check_password("CampusConnect-password-2026!"))


class AdminAccessTests(TestCase):
	def test_student_gets_forbidden_at_admin_and_admin_login(self):
		student = CustomUser.objects.create_user(
			username="student",
			password="CampusConnect-password-2026!",
	)
		self.client.force_login(student)

		for path in ("/admin/", "/admin/login/?next=/admin/"):
			with self.subTest(path=path):
				self.assertEqual(self.client.get(path).status_code, 403)

	def test_admin_keeps_access(self):
		admin_user = CustomUser.objects.create_user(
			username="campusadmin",
			password="CampusConnect-password-2026!",
			role=CustomUser.Role.ADMIN,
			is_staff=True,
		)
		self.client.force_login(admin_user)

		self.assertEqual(self.client.get("/admin/").status_code, 200)
