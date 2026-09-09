import csv
import io
from datetime import timedelta

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from django.utils import timezone

from .models import ActionItem, Lead


class WebsiteFlowTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user("reviewer", password="test-password-428")
        cls.other = get_user_model().objects.create_user("other", password="test-password-429")

    def test_public_pages_render(self):
        for name in ("home", "login", "thanks"):
            self.assertEqual(self.client.get(reverse(name)).status_code, 200)
        self.assertContains(self.client.get(reverse("home")), 'id="trace-data"')

    def test_lead_validation_and_success(self):
        data = {"name": "Test user", "email": "invalid", "company": "Test company"}
        response = self.client.post(reverse("home"), data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Lead.objects.count(), 0)
        self.assertContains(response, "Please check the highlighted fields")
        data["email"] = "test@example.com"
        self.assertRedirects(self.client.post(reverse("home"), data), reverse("thanks"))
        self.assertEqual(Lead.objects.count(), 1)

    def test_workspace_requires_authentication(self):
        self.assertRedirects(self.client.get(reverse("workspace")), "/login/?next=/workspace/")

    def test_login_rejects_external_redirect_and_preserves_local_redirect(self):
        data = {"username": "reviewer", "password": "test-password-428", "next": "https://example.com"}
        self.assertRedirects(self.client.post(reverse("login"), data), reverse("workspace"))
        self.client.logout()
        data["next"] = "/workspace/?status=open"
        self.assertRedirects(self.client.post(reverse("login"), data), data["next"])

    def test_action_creation_validation_and_ownership(self):
        self.client.force_login(self.user)
        invalid = self.client.post(reverse("workspace"), {"title": "", "priority": "unknown"})
        self.assertEqual(invalid.status_code, 200)
        self.assertContains(invalid, 'data-errors="true"')
        self.assertEqual(ActionItem.objects.count(), 0)
        response = self.client.post(reverse("workspace"), {"title": "Review evidence", "priority": "high", "description": "Supplier report", "due_date": "2026-10-01", "owner": self.other.pk})
        self.assertRedirects(response, reverse("workspace"))
        self.assertEqual(ActionItem.objects.get().owner, self.user)

    def test_filters_metrics_and_isolation(self):
        self.client.force_login(self.user)
        ActionItem.objects.create(owner=self.user, title="Supplier review", priority="high", due_date=timezone.localdate() - timedelta(days=1))
        ActionItem.objects.create(owner=self.user, title="Protocol check", status="done", priority="low")
        ActionItem.objects.create(owner=self.other, title="Private action")
        response = self.client.get(reverse("workspace"), {"q": "Supplier", "status": "open", "priority": "high"})
        self.assertContains(response, "Supplier review")
        self.assertNotContains(response, "Protocol check")
        self.assertNotContains(response, "Private action")
        self.assertEqual(response.context["total"], 2)
        self.assertEqual(response.context["overdue"], 1)
        self.assertEqual(response.context["completion"], 50)

    def test_status_update_restricts_owner_and_values(self):
        item = ActionItem.objects.create(owner=self.user, title="My action")
        url = reverse("update_action", args=[item.pk])
        self.client.force_login(self.other)
        self.assertEqual(self.client.post(url, {"status": "done"}).status_code, 404)
        self.client.force_login(self.user)
        self.assertEqual(self.client.get(url).status_code, 405)
        self.assertEqual(self.client.post(url, {"status": "approved"}).status_code, 400)
        self.assertRedirects(self.client.post(url, {"status": "done"}), reverse("workspace"))
        item.refresh_from_db()
        self.assertEqual(item.status, "done")

    def test_csv_export_is_filtered_and_formula_safe(self):
        self.client.force_login(self.user)
        ActionItem.objects.create(owner=self.user, title="=1+1", description='A "quoted", multiline\nvalue', priority="high")
        ActionItem.objects.create(owner=self.user, title="Excluded", priority="low")
        ActionItem.objects.create(owner=self.other, title="Private action", priority="high")
        response = self.client.get(reverse("workspace"), {"export": "csv", "priority": "high"})
        rows = list(csv.reader(io.StringIO(response.content.decode())))
        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[1][1], "'=1+1")
        self.assertEqual(rows[1][2], 'A "quoted", multiline\nvalue')
        self.assertIn("attachment", response["Content-Disposition"])

    def test_logout_requires_post_and_csrf(self):
        secure = Client(enforce_csrf_checks=True)
        secure.force_login(self.user)
        self.assertEqual(secure.get(reverse("logout")).status_code, 405)
        self.assertEqual(secure.post(reverse("logout")).status_code, 403)
        secure.get(reverse("workspace"))
        token = secure.cookies["csrftoken"].value
        response = secure.post(reverse("logout"), {"csrfmiddlewaretoken": token})
        self.assertRedirects(response, reverse("home"))
        self.assertNotIn("_auth_user_id", secure.session)

    def test_action_updates_require_csrf(self):
        item = ActionItem.objects.create(owner=self.user, title="Protected action")
        secure = Client(enforce_csrf_checks=True)
        secure.force_login(self.user)
        self.assertEqual(secure.post(reverse("update_action", args=[item.pk]), {"status": "done"}).status_code, 403)
        item.refresh_from_db()
        self.assertEqual(item.status, "open")
