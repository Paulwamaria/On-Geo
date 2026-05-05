from django.test import RequestFactory, SimpleTestCase
from django.urls import resolve, reverse

from . import views
from .forms import OnGeoRegistrationForm


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
