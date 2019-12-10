FROM python:3.7-alpine
WORKDIR	/code
ENV FLASK_APP ./app.py
ENV FLASK_RUN_HOST 0.0.0.0
RUN apk add --update python py-pip
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
EXPOSE 8080
COPY . .
CMD ["python", "", "-p 8080"]