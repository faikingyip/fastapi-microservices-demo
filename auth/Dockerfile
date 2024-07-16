from python:3.12.4-alpine3.20
LABEL maintainer="codefrantic.com"

# Logs will be outputted to the screen immediately
# when our application is running.
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
COPY ./alembic.ini ./alembic.ini
COPY ./alembic ./alembic

ARG DEFAULT_PORT=8000
ENV PORT $DEFAULT_PORT
EXPOSE $PORT

RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    rm -rf /tmp 

COPY ./src /app/src

ENV PATH="/py/bin:$PATH"

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]



