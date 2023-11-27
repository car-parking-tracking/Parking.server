FROM --platform=linux/amd64 python:3.11-slim
WORKDIR /backend
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD [ "gunicorn", "parking_backend.wsgi:application", "--bind", "0.0.0.0:8000", "--log-level", "debug" ]