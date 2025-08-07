FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN apt-get update && \
  apt-get install -y \
  cmake \
  build-essential \
  python3-dev \
  default-libmysqlclient-dev \
  pkg-config \
  && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir -r requirements.txt

RUN mkdir -p /app/staticfiles

COPY . .

RUN python3 manage.py makemigrations
RUN python3 manage.py migrate

EXPOSE 8000

CMD ["gunicorn", "TrueFace.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "4", "--threads", "10", "--timeout", "120", "-k", "gevent", "--log-level", "debug", "--reload"]
