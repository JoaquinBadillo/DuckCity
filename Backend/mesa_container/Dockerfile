FROM python:3.10.12-slim-buster
RUN mkdir /app
WORKDIR /app
COPY requirements.txt /app

RUN pip install --no-cache-dir -U pip && \
    pip install -r requirements.txt

EXPOSE 8521

ENTRYPOINT [ "python", "server.py"]