from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("core_api", "0003_roles_outbox_error"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="emissionfactor",
            name="version",
            field=models.CharField(default="v1", max_length=50),
        ),
        migrations.AlterField(
            model_name="disclosurereport",
            name="status",
            field=models.CharField(
                choices=[
                    ("draft", "Draft"),
                    ("in_review", "In review"),
                    ("approved", "Approved"),
                    ("published", "Published"),
                ],
                default="draft",
                max_length=20,
            ),
        ),
        migrations.CreateModel(
            name="BusinessUnit",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("tenant_id", models.CharField(db_index=True, max_length=100)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("name", models.CharField(max_length=255)),
                ("code", models.CharField(max_length=80)),
                (
                    "organization",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="business_units",
                        to="core_api.organization",
                    ),
                ),
                (
                    "parent",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="children",
                        to="core_api.businessunit",
                    ),
                ),
            ],
            options={"unique_together": {("tenant_id", "code")}},
        ),
        migrations.CreateModel(
            name="DisclosureMetric",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("tenant_id", models.CharField(db_index=True, max_length=100)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("metric_code", models.CharField(max_length=100)),
                ("metric_name", models.CharField(max_length=255)),
                ("metric_value", models.DecimalField(decimal_places=6, max_digits=18)),
                ("unit", models.CharField(max_length=30)),
                (
                    "report",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="metrics",
                        to="core_api.disclosurereport",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="EvidenceFile",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("tenant_id", models.CharField(db_index=True, max_length=100)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("file_name", models.CharField(max_length=255)),
                ("file_uri", models.TextField()),
                ("source_ref", models.CharField(blank=True, default="", max_length=120)),
                (
                    "report",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="evidence_files",
                        to="core_api.disclosurereport",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Asset",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("tenant_id", models.CharField(db_index=True, max_length=100)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("name", models.CharField(max_length=255)),
                ("asset_type", models.CharField(max_length=100)),
                ("external_id", models.CharField(max_length=120)),
                (
                    "status",
                    models.CharField(
                        choices=[("active", "Active"), ("retired", "Retired")],
                        default="active",
                        max_length=20,
                    ),
                ),
                ("commissioned_on", models.DateField(blank=True, null=True)),
                (
                    "business_unit",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="assets",
                        to="core_api.businessunit",
                    ),
                ),
                (
                    "site",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="assets",
                        to="core_api.site",
                    ),
                ),
            ],
            options={"unique_together": {("tenant_id", "external_id")}},
        ),
        migrations.CreateModel(
            name="Control",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("tenant_id", models.CharField(db_index=True, max_length=100)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("code", models.CharField(max_length=100)),
                ("title", models.CharField(max_length=255)),
                ("description", models.TextField(blank=True, default="")),
                (
                    "frequency",
                    models.CharField(
                        choices=[
                            ("ad_hoc", "Ad hoc"),
                            ("monthly", "Monthly"),
                            ("quarterly", "Quarterly"),
                            ("annual", "Annual"),
                        ],
                        default="monthly",
                        max_length=20,
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[("active", "Active"), ("inactive", "Inactive")],
                        default="active",
                        max_length=20,
                    ),
                ),
                (
                    "business_unit",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="controls",
                        to="core_api.businessunit",
                    ),
                ),
                (
                    "owner",
                    models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
                ),
            ],
            options={"unique_together": {("tenant_id", "code")}},
        ),
        migrations.CreateModel(
            name="Target",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("tenant_id", models.CharField(db_index=True, max_length=100)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("scope", models.CharField(max_length=20)),
                ("metric", models.CharField(default="co2e_kg", max_length=80)),
                ("baseline_year", models.PositiveIntegerField()),
                ("baseline_value", models.DecimalField(decimal_places=6, max_digits=18)),
                ("target_year", models.PositiveIntegerField()),
                ("target_value", models.DecimalField(decimal_places=6, max_digits=18)),
                ("unit", models.CharField(max_length=30)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("active", "Active"),
                            ("superseded", "Superseded"),
                            ("completed", "Completed"),
                        ],
                        default="active",
                        max_length=20,
                    ),
                ),
                (
                    "business_unit",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="targets",
                        to="core_api.businessunit",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Approval",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("tenant_id", models.CharField(db_index=True, max_length=100)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "status",
                    models.CharField(
                        choices=[("pending", "Pending"), ("approved", "Approved"), ("rejected", "Rejected")],
                        default="pending",
                        max_length=20,
                    ),
                ),
                ("decided_at", models.DateTimeField(blank=True, null=True)),
                ("comment", models.TextField(blank=True, default="")),
                (
                    "decided_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="decided_approvals",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "report",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="approvals",
                        to="core_api.disclosurereport",
                    ),
                ),
                (
                    "requested_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="requested_approvals",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
