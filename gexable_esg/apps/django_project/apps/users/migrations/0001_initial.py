from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="User",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("email", models.EmailField(max_length=254, unique=True)),
                ("password_hash", models.CharField(max_length=255)),
                ("first_name", models.CharField(blank=True, default="", max_length=150)),
                ("last_name", models.CharField(blank=True, default="", max_length=150)),
                ("is_active", models.BooleanField(default=True)),
                ("is_superuser", models.BooleanField(default=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={"db_table": "users"},
        ),
        migrations.CreateModel(
            name="UserProfile",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("job_title", models.CharField(blank=True, default="", max_length=120)),
                ("department", models.CharField(blank=True, default="", max_length=120)),
                ("phone", models.CharField(blank=True, default="", max_length=50)),
                (
                    "user",
                    models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name="profile", to="users.user"),
                ),
            ],
            options={"abstract": False},
        ),
    ]
