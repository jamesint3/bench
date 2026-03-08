from pathlib import Path


def test_api_v1_route_configured() -> None:
    urls = Path("gexable_esg/apps/django_project/config/urls.py").read_text()
    assert 'path("api/v1/"' in urls


def test_ui_routes_configured() -> None:
    urls = Path("gexable_esg/apps/django_project/config/urls.py").read_text()
    assert 'path("", views.home' in urls
    assert 'path("ui/data-intake"' in urls
    assert 'path("ui/emissions"' in urls
    assert 'path("ui/disclosures"' in urls
    assert 'path("ui/events"' in urls
    assert 'path("ui/health"' in urls
    assert 'path("ui/admin-portal"' in urls


def test_admin_route_configured() -> None:
    urls = Path("gexable_esg/apps/django_project/config/urls.py").read_text()
    assert 'path("admin/", admin.site.urls)' in urls
