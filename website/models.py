from django.db import models


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
