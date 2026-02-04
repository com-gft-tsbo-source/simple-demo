# FROM node:18 AS build
# RUN useradd -d /opt/frontend frontend
# USER frontend
# WORKDIR /opt/frontend
# COPY --chown=frontend . .
# RUN npm install 
# # RUN npm audit fix --force
# RUN npm run build

FROM nginx:alpine
RUN mkdir /opt/frontend
WORKDIR /opt/frontend
COPY nginx.conf /etc/nginx/nginx.conf
COPY index.html config.template.js /opt/frontend/
COPY 20-runtime-config.sh /docker-entrypoint.d/20-runtime-config.sh
RUN rm -f /docker-entrypoint.d/10-listen-on-ipv6-by-default.sh
