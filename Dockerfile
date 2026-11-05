FROM python:3.14-slim-bookworm
RUN groupadd -g 1000 appuser && \
    useradd -m -u 1000 -g appuser appuser
RUN mkdir /app && chown appuser:appuser /app

RUN apt update -y && apt install -y curl jq
RUN curl --proto '=https' --tlsv1.2 -sSf https://just.systems/install.sh | bash -s -- --to /usr/local/bin

WORKDIR /app
ENV PYTHONPATH="/app/src:${PYTHONPATH}"

# Copy dependency files and install dependencies (dev group included: CI runs the tests in
# this image, see app-ci's test-command)
COPY --chown=appuser:appuser pyproject.toml uv.lock /app/
RUN pip install uv && \
    uv export --no-hashes --no-emit-project > requirements.txt && \
    pip uninstall uv -y && \
    pip install --requirement requirements.txt && \
    rm requirements.txt

# Copy sources
COPY --chown=appuser:appuser src /app/src
COPY --chown=appuser:appuser tests /app/tests
COPY --chown=appuser:appuser justfile.container /app/justfile
COPY --chown=appuser:appuser pytest.ini /app/pytest.ini

# the image's own tag (the short commit sha), shown by GET /
ARG APP_VERSION=dev
ENV APP_VERSION=${APP_VERSION}

USER 1000
CMD ["uvicorn", "src.main:app", "--port=8080", "--host=0.0.0.0"]
