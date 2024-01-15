#!/usr/bin/bash

gunicorn -b 0.0.0.0:8080 --worker-class geventwebsocket.gunicorn.workers.GeventWebSocketWorker -w 1 main:app