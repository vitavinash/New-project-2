from django.db import models
from django.conf import settings


class Lead(models.Model):
    COMPANY_SIZES = [
        ("1-50", "1-50"),
        ("51-200", "51-200"),
        ("201-1000", "201-1000"),
        ("1000+", "1000+"),
    ]

    name = models.CharField(max_length=120)
    email = models.EmailField()
    phone = models.CharField(max_length=30, blank=True)
    company = models.CharField(max_length=160)
    company_size = models.CharField(max_length=20, choices=COMPANY_SIZES, blank=True)
    interest = models.CharField(max_length=160, blank=True)
    message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} - {self.company}"


class ActionItem(models.Model):
    PRIORITIES = [("high", "High"), ("medium", "Medium"), ("low", "Low")]
    STATUSES = [("open", "Open"), ("in_progress", "In progress"), ("done", "Done")]

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=160)
    description = models.TextField(blank=True, max_length=4000)
    priority = models.CharField(max_length=10, choices=PRIORITIES, default="medium")
    status = models.CharField(max_length=20, choices=STATUSES, default="open")
    due_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title
