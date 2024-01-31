#!/bin/sh

gunicorn src.main:app --access-logfile="-" --bind 0.0.0.0:8000 --worker-class uvicorn.workers.UvicornWorker
