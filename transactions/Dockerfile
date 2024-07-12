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

ARG DEFAULT_PORT=8003
ENV PORT $DEFAULT_PORT
EXPOSE $PORT

RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    rm -rf /tmp && \
    adduser \
        --disabled-password \
        --no-create-home \
        api-user


COPY ./src /app/src

ENV PATH="/py/bin:$PATH"

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8003"]

# Every time you run something from this immage,
# it will run as the last user you logged in as.
# So switch the user here.
USER api-user



