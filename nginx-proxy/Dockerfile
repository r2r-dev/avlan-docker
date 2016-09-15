FROM nginx:1.11

MAINTAINER Artur Stachecki <artur.stachecki@gmail.com>

COPY nginx.tmpl /etc/nginx/

EXPOSE 80 443

CMD ["nginx", "-g", "daemon off;"]
