# Deploy Django server to EC2 with Github

1.  remote to the EC2 server
    [real one1]`ssh -i "20220703.pem" ubuntu@ec2-34-230-29-73.compute-1.amazonaws.com`
2.  `sudo apt-get update`
    [real one]`ssh -i "20220703.pem" ubuntu@ec2-107-20-26-70.compute-1.amazonaws.com`
3.  `sudo apt-get update`
4.  install dependencies
    `sudo apt-get install python3 python3-pip python-is-python3 nginx git python3-dev libapache2-mod-wsgi-py3`

    gunicorn : Depends: python3-gunicorn (= 20.1.0-2) but it is not going to be installed
    linux-headers-aws : Depends: linux-headers-5.15.0-1015-aws but it is not going to be installed
    linux-image-aws : Depends: linux-image-5.15.0-1015-aws but it is not going to be installed

5.  clone project
    `git clone https://github.com/fungjojo/django-server.git`
6.  install virtual environment
    `sudo pip install virtualenv`
7.  `cd django-server/backend`
8.  switch to virtual environment "venv"
    `virtualenv venv`
9.  source venv
    `source venv/bin/activate`
10. install django dependencies
    `pip install gunicorn django django-cors-headers djangorestframework`
11. `cd backend`
12. modify settings.py
    `vim settings.py`

    - add IP4 public IP to allowed host, find the IP from EC2 instance page
    - `ALLOWED_HOSTS = ['107.20.26.70']`
    - add this to the top of the file `import os`
    - add the line below to the bottom of the file
      `STATIC_ROOT = os.path.join(BASE_DIR, "static/")`

13. `cd ..`
14. `python manage.py collectstatic`
15. `gunicorn --bind 0.0.0.0:8000 --timeout 60 backend.wsgi`
16. stop the process as you see "Booting work with pid: xxx" by pressing ctrl + c
17. `sudo vim /etc/systemd/system/gunicorn.service`

        - add the below lines

    <!-- /home/ubuntu/django-server/backend/venv/lib/python3.10/site-packages/gunicorn/app/wsgiapp.py -->

    [Unit]
    Description=gunicorn daemon
    After=network.target
    [Service]
    User=ubuntu
    Group=www-data
    WorkingDirectory=/home/ubuntu/django-server/backend
    ExecStart=/home/ubuntu/django-server/backend/venv/bin/gunicorn --workers 3 --timeout 120 --bind unix:/home/ubuntu/django-server/backend/backend.sock backend.wsgi:application
    [Install]
    WantedBy=multi-user.target

18. `sudo systemctl daemon-reload`
19. `sudo systemctl start gunicorn`
20. `sudo systemctl enable gunicorn`
21. `sudo mkdir /etc/nginx/sites-available/django-server`
22. `sudo vim /etc/nginx/sites-available/django-server/backend`

        - add the below lines

    server {
    listen 80;
    server_name 107.20.26.70;
    location = /favicon.ico { access_log off; log_not_found off; }
    location /static/ {
    root /home/ubuntu/django-server/backend;
    }
    location / {
    include proxy_params;
    proxy_read_timeout 300s;
    proxy_connect_timeout 75s;
    proxy_pass http://unix:/home/ubuntu/django-server/backend/backend.sock;
    }
    }

23. `sudo ln -s /etc/nginx/sites-available/django-server/backend /etc/nginx/sites-enabled`
24. `sudo nginx -t`
25. `sudo rm /etc/nginx/sites-enabled/default`
26. `sudo service nginx restart`
27. type in the IP in the browser dto check whether the deployment is success
    107.20.26.70

## Troubleshoot

1. from django.core.wsgi import get_wsgi_application
   ModuleNotFoundError: No module named 'django'

`deactivate`
`sudo apt-get remove gunicorn`
`source venv/bin/activate`
`pip install gunicorn`
`pip install django`
`pip install django-cors-headers`
`pip install djangorestframework`

2. 502 bad gateway
   `pip install backports.functools-lru-cache altgraph`

   - check the logs
     `cat /var/log/nginx/access.log`
     `cat /var/log/nginx/error.log`
   - see the process related to gunicorn
     `ps aux | grep gunicorn`
     `sudo systemctl enable gunicorn.service`
     `sudo systemctl list-unit-files | grep gunicorn`
     `sudo systemctl is-active gunicorn`
     `sudo service gunicorn start`
     `sudo systemctl status gunicorn.service`
     `sudo chown ubuntu gunicorn`
   - change the user from www-data to ubuntu
     `sudo vim /etc/nginx/nginx.conf`
     `user ubuntu;`

     gunicorn backend.wsgi:application --bind=172.31.21.65:8000
     gunicorn --bind 0.0.0.0:8000 backend.wsgi

- if err connection
  `ps aux | grep gunicorn`
  `kill -9 [pid]`

- if updated code, refresh in server
  `sudo systemctl restart gunicorn`

# NGINX Error log for troubleshoot problem 2

2022/07/10 13:20:00 [notice] 2698#2698: using inherited sockets from "6;7;"
2022/07/10 14:21:11 [emerg] 4692#4692: open() "/etc/nginx/sites-enabled/backend" failed (2: No such file or directory) in /etc/nginx/nginx.conf:60
2022/07/10 14:25:13 [emerg] 4775#4775: open() "/etc/nginx/sites-enabled/backend" failed (20: Not a directory) in /etc/nginx/nginx.conf:60
2022/07/10 14:29:26 [crit] 4837#4837: pread() "/etc/nginx/sites-enabled/django-test" failed (21: Is a directory)
2022/07/10 14:31:38 [crit] 4890#4890: *1 connect() to unix:/home/ubuntu/django-test/backend/backend.sock failed (13: Permission denied) while connecting to upstream, client: 124.244.164.66, server: 3.80.35.163, request: "GET / HTTP/1.1", upstream: "http://unix:/home/ubuntu/django-test/backend/backend.sock:/", host: "3.80.35.163"
2022/07/10 14:32:36 [crit] 4890#4890: *1 connect() to unix:/home/ubuntu/django-test/backend/backend.sock failed (13: Permission denied) while connecting to upstream, client: 124.244.164.66, server: 3.80.35.163, request: "GET / HTTP/1.1", upstream: "http://unix:/home/ubuntu/django-test/backend/backend.sock:/", host: "3.80.35.163"
2022/07/10 14:32:43 [crit] 4890#4890: *1 connect() to unix:/home/ubuntu/django-test/backend/backend.sock failed (13: Permission denied) while connecting to upstream, client: 124.244.164.66, server: 3.80.35.163, request: "GET / HTTP/1.1", upstream: "http://unix:/home/ubuntu/django-test/backend/backend.sock:/", host: "3.80.35.163"
2022/07/10 14:33:15 [crit] 4890#4890: *1 connect() to unix:/home/ubuntu/django-test/backend/backend.sock failed (13: Permission denied) while connecting to upstream, client: 124.244.164.66, server: 3.80.35.163, request: "GET / HTTP/1.1", upstream: "http://unix:/home/ubuntu/django-test/backend/backend.sock:/", host: "3.80.35.163"
2022/07/10 14:35:05 [crit] 4890#4890: *8 connect() to unix:/home/ubuntu/django-test/backend/backend.sock failed (13: Permission denied) while connecting to upstream, client: 124.244.164.66, server: 3.80.35.163, request: "GET /api/todos HTTP/1.1", upstream: "http://unix:/home/ubuntu/django-test/backend/backend.sock:/api/todos", host: "3.80.35.163"
2022/07/10 14:42:14 [crit] 4890#4890: *11 connect() to unix:/home/ubuntu/django-test/backend/backend.sock failed (13: Permission denied) while connecting to upstream, client: 124.244.164.66, server: 3.80.35.163, request: "GET /api/todos HTTP/1.1", upstream: "http://unix:/home/ubuntu/django-test/backend/backend.sock:/api/todos", host: "3.80.35.163"
2022/07/10 14:42:42 [alert] 4890#4890: *13 open socket #10 left in connection 3
2022/07/10 14:42:42 [alert] 4890#4890: aborting
2022/07/10 14:42:44 [crit] 4932#4932: *1 connect() to unix:/home/ubuntu/django-test/backend/backend.sock failed (13: Permission denied) while connecting to upstream, client: 124.244.164.66, server: 3.80.35.163, request: "GET /api/todos HTTP/1.1", upstream: "http://unix:/home/ubuntu/django-test/backend/backend.sock:/api/todos", host: "3.80.35.163"
2022/07/10 14:55:38 [crit] 4932#4932: *6 connect() to unix:/home/ubuntu/django-test/backend/backend.sock failed (13: Permission denied) while connecting to upstream, client: 124.244.164.66, server: 3.80.35.163, request: "GET /api/todos HTTP/1.1", upstream: "http://unix:/home/ubuntu/django-test/backend/backend.sock:/api/todos", host: "3.80.35.163"
2022/07/10 14:55:43 [crit] 4932#4932: *6 connect() to unix:/home/ubuntu/django-test/backend/backend.sock failed (13: Permission denied) while connecting to upstream, client: 124.244.164.66, server: 3.80.35.163, request: "GET / HTTP/1.1", upstream: "http://unix:/home/ubuntu/django-test/backend/backend.sock:/", host: "3.80.35.163"
2022/07/10 14:57:10 [crit] 4932#4932: \*10 connect() to unix:/home/ubuntu/django-test/backend/backend.sock failed (13: Permission denied) while connecting to upstream, client: 124.244.164.66, server: 3.80.35.163, request: "GET / HTTP/1.1", upstream: "http://unix:/home/ubuntu/django-test/backend/backend.sock:/", host: "3.80.35.163"
