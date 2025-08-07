#!/bin/sh

# Run migrations on container start
echo "Running migrations..."
python3 manage.py makemigrations
python3 manage.py migrate

# Collect static files (optional, remove if not needed)
# python3 manage.py collectstatic --noinput

echo "Starting Gunicorn..."
exec gunicorn TrueFace.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 4 \
    --threads 10 \
    --timeout 120 \
    -k gevent \
    --log-level debug \
    --reload
