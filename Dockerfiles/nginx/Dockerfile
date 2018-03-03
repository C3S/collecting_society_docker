# For copyright and license terms, see COPYRIGHT.rst (top level of repository)
# Repository: https://github.com/C3S/c3s.ado.repertoire

FROM jwilder/nginx-proxy
RUN { \
      echo 'client_max_body_size 100m;'; \
      echo 'error_log off;'; \
    } > /etc/nginx/conf.d/my_proxy.conf
