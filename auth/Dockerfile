from python:3.12.4-alpine3.20
LABEL maintainer="codefrantic.com"

# Logs will be outputted to the screen immediately
# when our application is running.
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
COPY ./app /app
WORKDIR /app
EXPOSE 8000

# dev is false by default. The compose.yaml file can override this.
ARG DEV=false

# 1) Use a venv to avoid conflicts within the docker
# base image (i.e. in case we change the image).
# 2) Create a restricted access user that only has
# access to our application and not the rest of the
# container. User does not have a home folder.
# 3) postgresql-client is required for psycopg2 to work.
# 4) build-base, postgresql-dev and musl-dev are needed
# for psycopg2 to compile. We group them into the 
# virtual dependency package with name tmp-build-deps so 
# we can remove them once we have compiled psycopg2.
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    apk add --update --no-cache postgresql-client && \
    apk add --update --no-cache --virtual .tmp-build-deps \
        build-base postgresql-dev musl-dev && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    if [ "$DEV" = "true" ]; \
        then /py/bin/pip install -r /tmp/requirements.dev.txt; \
    fi && \
    rm -rf /tmp && \
    apk del .tmp-build-deps && \
    adduser \
        --disabled-password \
        --no-create-home \
        api-user

ENV PATH="/py/bin:$PATH"

# Every time you run something from this immage,
# it will run as the last user you logged in as.
# So switch the user here.
USER api-user