FROM node:22.2.0-alpine3.20
LABEL maintainer="codefrantic.com"

WORKDIR /app

# COPY ./package.json .
COPY ./package*.json ./

RUN npm install

COPY . .

ARG DEFAULT_PORT=3000
ENV PORT $DEFAULT_PORT
EXPOSE $PORT


CMD ["npm", "run", "dev"]