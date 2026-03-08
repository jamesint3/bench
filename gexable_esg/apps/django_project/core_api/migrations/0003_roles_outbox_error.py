from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("core_api", "0002_outbox_indexes"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="domaineventoutbox",
            name="error_message",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.CreateModel(
            name="UserRole",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("tenant_id", models.CharField(db_index=True, max_length=100)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "role",
                    models.CharField(
                        choices=[
                            ("preparer", "Preparer"),
                            ("reviewer", "Reviewer"),
                            ("approver", "Approver"),
                            ("admin", "Admin"),
                        ],
                        max_length=20,
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="gexable_roles",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "unique_together": {("tenant_id", "user", "role")},
            },
        ),
    ]
