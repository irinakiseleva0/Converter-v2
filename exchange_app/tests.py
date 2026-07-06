from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse
from unittest.mock import patch


def mock_rates_response(mock_get):
    mock_response = mock_get.return_value
    mock_response.raise_for_status.return_value = None
    mock_response.json.return_value = {
        "rates": {"USD": 1.0, "EUR": 0.9, "GBP": 0.8}
    }
    return mock_response


class ExchangeViewTests(TestCase):
    @patch("exchange_app.views.requests.get")
    def test_converter_page_loads(self, mock_get):
        mock_rates_response(mock_get)

        response = self.client.get(reverse("converter"))

        self.assertEqual(response.status_code, 200)

    @patch("exchange_app.views.requests.get")
    def test_valid_conversion(self, mock_get):
        mock_rates_response(mock_get)

        response = self.client.post(reverse("converter"), {
            "from-amount": "100",
            "from-curr": "USD",
            "to-curr": "EUR",
        })

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["converted_amount"], 90.0)

    @patch("exchange_app.views.requests.get")
    def test_negative_amount_rejected(self, mock_get):
        mock_rates_response(mock_get)

        response = self.client.post(reverse("converter"), {
            "from-amount": "-50",
            "from-curr": "USD",
            "to-curr": "EUR",
        })

        self.assertEqual(response.status_code, 200)
        self.assertIn("greater than zero", response.context["error"])

    @patch("exchange_app.views.requests.get")
    def test_zero_amount_rejected(self, mock_get):
        mock_rates_response(mock_get)

        response = self.client.post(reverse("converter"), {
            "from-amount": "0",
            "from-curr": "USD",
            "to-curr": "EUR",
        })

        self.assertEqual(response.status_code, 200)
        self.assertIn("greater than zero", response.context["error"])

    @patch("exchange_app.views.requests.get")
    def test_unreasonably_large_amount_rejected(self, mock_get):
        mock_rates_response(mock_get)

        response = self.client.post(reverse("converter"), {
            "from-amount": "99999999999",
            "from-curr": "USD",
            "to-curr": "EUR",
        })

        self.assertEqual(response.status_code, 200)
        self.assertIn("too large", response.context["error"])

    @patch("exchange_app.views.requests.get")
    def test_invalid_currency_code_rejected(self, mock_get):
        mock_rates_response(mock_get)

        response = self.client.post(reverse("converter"), {
            "from-amount": "100",
            "from-curr": "XXX",
            "to-curr": "EUR",
        })

        self.assertEqual(response.status_code, 200)
        self.assertIn("Unknown currency", response.context["error"])

    @patch("exchange_app.views.requests.get")
    def test_non_numeric_amount_rejected(self, mock_get):
        mock_rates_response(mock_get)

        response = self.client.post(reverse("converter"), {
            "from-amount": "abc",
            "from-curr": "USD",
            "to-curr": "EUR",
        })

        self.assertEqual(response.status_code, 200)
        self.assertIn("Invalid amount", response.context["error"])


class RegistrationTests(TestCase):
    def test_successful_registration(self):
        response = self.client.post(reverse("register"), {
            "username": "testuser1",
            "password1": "Str0ngP@ssword123",
            "password2": "Str0ngP@ssword123",
            "email": "test1@example.com",
        })

        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username="testuser1").exists())

    def test_weak_password_rejected(self):
        response = self.client.post(reverse("register"), {
            "username": "testuser2",
            "password1": "12345678",
            "password2": "12345678",
            "email": "test2@example.com",
        })

        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username="testuser2").exists())

    def test_mismatched_passwords_rejected(self):
        response = self.client.post(reverse("register"), {
            "username": "testuser3",
            "password1": "GoodPassword123",
            "password2": "DifferentPassword456",
            "email": "test3@example.com",
        })

        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username="testuser3").exists())

    def test_duplicate_username_rejected(self):
        User.objects.create_user(
            username="existinguser",
            email="existing@example.com",
            password="Str0ngP@ssword123",
        )

        response = self.client.post(reverse("register"), {
            "username": "existinguser",
            "password1": "Str0ngP@ssword123",
            "password2": "Str0ngP@ssword123",
            "email": "new@example.com",
        })

        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.filter(username="existinguser").count(), 1)
