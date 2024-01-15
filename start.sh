#!/usr/bin/bash

export PORT=${PORT:-8080}

gunicorn -b 0.0.0.0:$PORT --worker-class geventwebsocket.gunicorn.workers.GeventWebSocketWorker -w 1 --timeout 10000 main:app