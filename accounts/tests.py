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
		self.assertContains(response, "Account created successfully. Please log in.")
		self.assertContains(response, "alert-success")
		user = CustomUser.objects.get(username="newstudent")
		self.assertEqual(user.role, CustomUser.Role.STUDENT)
		self.assertTrue(user.check_password("CampusConnect-password-2026!"))

	def test_login_form_uses_bootstrap_and_csrf(self):
		response = self.client.get(reverse("login"))

		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'class="form-control"')
		self.assertContains(response, 'name="csrfmiddlewaretoken"')

	def test_profile_updates_only_the_signed_in_users_editable_fields(self):
		student = CustomUser.objects.create_user(
			username="profileuser",
			password="CampusConnect-password-2026!",
		)
		self.client.force_login(student)
		profile_page = self.client.get(reverse("profile"))

		self.assertEqual(profile_page.status_code, 200)
		self.assertContains(profile_page, 'class="form-control"')
		self.assertContains(profile_page, 'name="csrfmiddlewaretoken"')

		response = self.client.post(
			reverse("profile"),
			{
				"first_name": "Updated",
				"last_name": "Student",
				"email": "updated@example.com",
				"course": "Biology",
			},
		)

		self.assertRedirects(response, reverse("profile"))
		student.refresh_from_db()
		self.assertEqual(student.first_name, "Updated")
		self.assertEqual(student.email, "updated@example.com")
		self.assertEqual(student.course, "Biology")
		self.assertEqual(student.role, CustomUser.Role.STUDENT)

	def test_profile_requires_login(self):
		response = self.client.get(reverse("profile"))

		self.assertRedirects(
			response,
			f"{reverse('login')}?next={reverse('profile')}",
		)

	def test_profile_post_updates_only_the_signed_in_user(self):
		owner = CustomUser.objects.create_user(username="owner", first_name="Original")
		other_user = CustomUser.objects.create_user(username="other")
		self.client.force_login(other_user)

		response = self.client.post(
			reverse("profile"),
			{"first_name": "Changed", "last_name": "User", "email": "changed@example.com", "course": "Biology"},
		)

		self.assertRedirects(response, reverse("profile"))
		owner.refresh_from_db()
		other_user.refresh_from_db()
		self.assertEqual(owner.first_name, "Original")
		self.assertEqual(other_user.first_name, "Changed")


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
