FROM node:18-slim as builder

ARG APP_NAME
ENV APP_NAME=${APP_NAME}
WORKDIR /${APP_NAME}

COPY ui/ .

RUN npm install

RUN npm run build

FROM node:18-slim as dev

ARG APP_NAME
ENV APP_NAME=${APP_NAME}
WORKDIR /${APP_NAME}

COPY ui/ .

RUN npm install

EXPOSE 3000

CMD ["npm", "run", "dev", "--", "--port", "3000", "--host", "0.0.0.0"]

FROM nginx:alpine as prod

ARG APP_NAME
ENV APP_NAME=${APP_NAME}

COPY --from=builder /${APP_NAME}/dist /usr/share/nginx/html

COPY docker/ui/nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
