from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Lead",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=120)),
                ("email", models.EmailField(max_length=254)),
                ("phone", models.CharField(blank=True, max_length=30)),
                ("company", models.CharField(max_length=160)),
                (
                    "company_size",
                    models.CharField(
                        blank=True,
                        choices=[("1-50", "1-50"), ("51-200", "51-200"), ("201-1000", "201-1000"), ("1000+", "1000+")],
                        max_length=20,
                    ),
                ),
                ("interest", models.CharField(blank=True, max_length=160)),
                ("message", models.TextField(blank=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={"ordering": ["-created_at"]},
        ),
    ]
