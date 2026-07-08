#!/bin/bash

cd /home/ec2-user/TaskFlow-AWS-DevOps

pkill gunicorn || true

nohup gunicorn \
--workers 3 \
--bind 127.0.0.1:5000 \
app:app \
> gunicorn.log 2>&1 &