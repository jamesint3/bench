FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

# Keep image simple/reliable for local demo builds on Docker Desktop.
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir "Django>=4.2,<6"

# Copy full repository layout as shown in local setup
# (e.g. bench/, docs/, gexable_esg/, pyproject.toml, etc.).
COPY . .

EXPOSE 8000

CMD ["sh", "-c", "python gexable_esg/apps/django_project/manage.py migrate && python gexable_esg/apps/django_project/manage.py runserver 0.0.0.0:8000"]
