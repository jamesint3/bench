from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core_api", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="DomainEventOutbox",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("tenant_id", models.CharField(db_index=True, max_length=100)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("topic", models.CharField(max_length=120)),
                ("payload", models.JSONField(default=dict)),
                ("schema_version", models.CharField(default="v1", max_length=20)),
                ("status", models.CharField(db_index=True, default="pending", max_length=20)),
                ("published_at", models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.AddIndex(
            model_name="activityrecord",
            index=models.Index(fields=["tenant_id", "created_at"], name="act_tenant_created_idx"),
        ),
        migrations.AddIndex(
            model_name="emissionresult",
            index=models.Index(fields=["tenant_id", "created_at"], name="emi_tenant_created_idx"),
        ),
        migrations.AddIndex(
            model_name="disclosurereport",
            index=models.Index(fields=["tenant_id", "period"], name="dis_tenant_period_idx"),
        ),
    ]
