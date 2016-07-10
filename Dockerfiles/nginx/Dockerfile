FROM jwilder/nginx-proxy
RUN { \
      echo 'client_max_body_size 100m;'; \
      echo 'error_log off;'; \
    } > /etc/nginx/conf.d/my_proxy.conf
