FROM python:3.11-slim
WORKDIR /backend
RUN pip install --upgrade pip
COPY . .
RUN pip install -r requirements.txt --no-cache-dir
CMD sh -c "gunicorn blog_project.wsgi:application --bind 0.0.0.0:8000"
