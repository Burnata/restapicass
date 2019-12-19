FROM python:3.7.1-alpine
WORKDIR	/code
ENV FLASK_APP app.py
ENV FLASK_RUN_HOST 0.0.0.0
ENV FLASK_RUN_PORT 8080
ENV CASSANDRA_RPC_HOST 0.0.0.0
ENV CASSANDRA_RPC_PORT 9160
ENV CASSANDRA_CQLSH_HOST 0.0.0.0
ENV CASSANDRA_CQLSH_PORT 9042
RUN apk add --update python py-pip
RUN apk add --no-cache gcc musl-dev linux-headers
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .
CMD ["flask", "run"]