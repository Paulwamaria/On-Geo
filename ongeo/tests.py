from django.contrib.auth.models import User
from django.test import Client, RequestFactory, SimpleTestCase, TestCase
from django.urls import resolve, reverse

from . import views
from .forms import OnGeoRegistrationForm
from .models import AllAtendees, Notification, Organisation, Post, Profile


class PublicRouteTests(SimpleTestCase):
    def test_home_route_resolves_to_index_view(self):
        match = resolve(reverse("home"))

        self.assertEqual(match.func, views.index)

    def test_about_route_resolves_to_about_view(self):
        match = resolve(reverse("about"))

        self.assertEqual(match.func, views.about)


class PublicViewTests(SimpleTestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_index_view_renders_successfully(self):
        request = self.factory.get(reverse("home"))
        request.user = None

        response = views.index(request)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Welcome to On-Geo Manager")

    def test_about_view_renders_successfully(self):
        request = self.factory.get(reverse("about"))
        request.user = None

        response = views.about(request)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "What is On-Geo Manager")


class RegistrationFormTests(SimpleTestCase):
    def test_registration_form_exposes_expected_fields(self):
        form = OnGeoRegistrationForm()

        self.assertEqual(
            list(form.fields),
            ["email", "first_name", "last_name", "username", "password1", "password2"],
        )


class AccountWorkflowTests(TestCase):
    def test_registration_creates_user_and_profile(self):
        response = self.client.post(
            reverse("register"),
            data={
                "email": "jane@example.com",
                "first_name": "Jane",
                "last_name": "Doe",
                "username": "janedoe",
                "password1": "StrongPass123!",
                "password2": "StrongPass123!",
            },
        )

        self.assertRedirects(response, reverse("login"))
        user = User.objects.get(username="janedoe")
        self.assertEqual(user.first_name, "Jane")
        self.assertEqual(user.last_name, "Doe")
        self.assertTrue(Profile.objects.filter(user=user).exists())

    def test_switch_community_creates_and_assigns_organisation(self):
        user = User.objects.create_user(username="paul", password="StrongPass123!")
        self.client.force_login(user)

        response = self.client.post(reverse("switch-community"), {"community": "Moringa"})

        self.assertRedirects(response, reverse("posts"))
        user.profile.refresh_from_db()
        self.assertEqual(user.profile.community.organisation_name, "Moringa")


class ContentWorkflowTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="creator",
            password="StrongPass123!",
            first_name="Create",
            last_name="User",
        )
        self.organisation = Organisation.objects.create(organisation_name="Moringa")
        self.user.profile.community = self.organisation
        self.user.profile.save()
        self.client = Client()
        self.client.force_login(self.user)

    def test_post_create_uses_logged_in_user_community(self):
        response = self.client.post(
            reverse("post-create"),
            data={
                "title": "Policy update",
                "content": "Read the latest update.",
                "links": "",
            },
        )

        self.assertRedirects(response, "/")
        post = Post.objects.get(title="Policy update")
        self.assertEqual(post.user, self.user)
        self.assertEqual(post.organisation, self.organisation)

    def test_notification_create_uses_logged_in_user_community(self):
        response = self.client.post(
            reverse("notification-create"),
            data={"content": "Team meeting at 4pm."},
        )

        self.assertRedirects(response, "/")
        notification = Notification.objects.get(content="Team meeting at 4pm.")
        self.assertEqual(notification.user, self.user)
        self.assertEqual(notification.organisation, self.organisation)

    def test_attend_does_not_duplicate_same_day_check_in(self):
        self.client.get(reverse("logins"))
        self.client.get(reverse("logins"))

        self.assertEqual(AllAtendees.objects.filter(user=self.user).count(), 1)
