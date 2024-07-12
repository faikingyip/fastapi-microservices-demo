# Accounts service

### This service is responsible for Accounts information.

##### Start the server

uvicorn src.main:app --reload

##### Generate random SECRET_KEY for jwt items.

openssl rand -hex 32


##### Create requires an authenticated user.