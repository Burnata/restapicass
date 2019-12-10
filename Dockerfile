FROM python:3.7-alpine
WORKDIR	/code
ENV FLASK_APP ./src/app.py
ENV FLASK_RUN_HOST 0.0.0.0
RUN apk add --update python py-pip
RUN pip install Flask:0.12.2
RUN pip install cassandra-driver:3.20.2
RUN pip install Cluster:1.4.1
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
EXPOSE 8080
COPY . .
CMD ["python", "./src/app.py", "-p 8080"]