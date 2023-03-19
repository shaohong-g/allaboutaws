# Base image
FROM python:3.9.6-slim-buster

# Set environment varibles
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

COPY ./scripts /app

EXPOSE 5000

CMD ["sh", "-c", "/app/start_wsgi.sh"]