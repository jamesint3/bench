from pathlib import Path


def test_api_v1_route_configured() -> None:
    urls = Path("gexable_esg/apps/django_project/config/urls.py").read_text()
    assert 'path("api/v1/"' in urls


def test_ui_home_route_configured() -> None:
    urls = Path("gexable_esg/apps/django_project/config/urls.py").read_text()
    assert 'path("", home' in urls
