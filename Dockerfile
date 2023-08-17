FROM python:3.11
WORKDIR /backend
RUN pip install --upgrade pip
COPY . .
RUN pip install -r requirements.txt --no-cache-dir
COPY entrypoint.sh .
ENTRYPOINT [ "sh", "entrypoint.sh" ]
