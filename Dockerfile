FROM python:3.11-slim
WORKDIR /backend
RUN pip install --upgrade pip
COPY . .
RUN pip install -r requirements.txt --no-cache-dir
ADD entrypoint.sh /entrypoint.sh
RUN chmod a+x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
CMD sh -c "gunicorn parking_backend.wsgi:application --bind 0.0.0.0:8000"
