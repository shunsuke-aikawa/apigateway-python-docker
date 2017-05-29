#!/bin/bash
source /root/.pyenv/versions/lambda/bin/activate
uwsgi --ini /home/lambda/uwsgi/uwsgi.ini --daemonize /home/lambda/uwsgi/uwsgi.log

/sbin/service nginx start

tail -f /dev/null