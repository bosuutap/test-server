#!/usr/bin/bash

export PORT=${PORT:-8080}

uwsgi --http 0.0.0.0:$PORT --gevent 1000 --http-websockets --master --wsgi-file main.py --callable app
#gunicorn -b 0.0.0.0:$PORT --worker-class geventwebsocket.gunicorn.workers.GeventWebSocketWorker -w 1 --timeout 10000 main:app