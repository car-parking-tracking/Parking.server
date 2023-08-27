FROM python:3.11-slim
WORKDIR /backend
RUN apt-get update && apt-get install -y libpq-dev build-essential
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD [ "gunicorn", "parking_backend.wsgi:application", "--bind", "0.0.0.0:8000" ]
