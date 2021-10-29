/etc/nginx/conf.d/zendp_prod.conf

```

server {
    listen 80;
    server_name www.zendp.cn;
    # gzip config
    gzip on;
    gzip_min_length 1k;
    gzip_comp_level 9;
    gzip_types text/plain application/javascript application/x-javascript text/css application/xml text/javascript application/x-httpd-php image/jpeg image/gif image/png;
    gzip_vary on;
    gzip_disable "MSIE [1-6]\.";

    root /var/www/html/zendp_dist;

    location / {
        # 用于配合 browserHistory使用
        try_files $uri $uri/ /index.html;
    }
    ``
    location /api {
        proxy_pass http://localhost:5050;
        proxy_set_header   X-Forwarded-Proto $scheme;
        proxy_set_header   X-Real-IP         $remote_addr;
    } 
}
```


/etc/supervisor/conf.d/zendp.conf
```
[program:zendp]
directory=/root/projects/zendp/backend/zendp_backend
command=/root/projects/zendp/backend/venv/bin/gunicorn --workers=6 run:app -b 0.0.0.0:5050
autorestart=true
stdout_logfile=/root/projects/zendp/backend/log/out.log
loglevel=info
startsecs = 5
startretries = 3
redirect_stderr=true
environment=PYTHONIOENCODING=utf-8,FLASK_ENV=production

```