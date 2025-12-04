FROM python:3.14-slim

ENV DJANGO_SETTINGS_MODULE=config.settings
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV VIRTUAL_ENV=/home/djangoapp/.venv
ENV PATH=/home/djangoapp/.venv/bin:/home/djangoapp/.local/bin:$PATH

RUN useradd --create-home --home-dir /home/djangoapp djangoapp
RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential libpq-dev curl && \
    apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /home/djangoapp

USER djangoapp

RUN curl -LsSf https://astral.sh/uv/install.sh | sh

COPY --chown=djangoapp:djangoapp ./pyproject.toml ./uv.lock ./
RUN uv sync --locked --no-dev

COPY --chown=djangoapp:djangoapp ./app ./app
COPY --chown=djangoapp:djangoapp ./config ./config
COPY --chown=djangoapp:djangoapp ./manage.py .

EXPOSE 8000
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "4", "config.wsgi:application"]