# Auth service

### This service is responsible for authentication such as sign up and sign in.

##### Start the server

uvicorn src.main:app --reload

##### Generate random SECRET_KEY for jwt authentication.

openssl rand -hex 32
