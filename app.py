import json
import time
from functools import wraps
import flask
from flask import Flask, Response
from cassandra.cluster import Cluster
from JSON import util
from data.postmagic import Postmagic
from src.keyspace_creation import create
import requests

# time.sleep(120) #uncommenct on push

app = Flask(__name__)

# table creation script
cluster = Cluster(["cassandra"], protocol_version=3)
session = cluster.connect()
create()


# def json_api(f):
#     @wraps(f)
#     def decorated_function(*args):
#         json.load(*args)
#
#     return decorated_function


@app.route('/api/send', methods=['POST'])
def post():
    data = json.loads(flask.request.stream, encoding=dict)
    magic_number = data["magic_number"]
    rows = session.execute('SELECT %s FROM mode', magic_number)
    for data["magic_number"] in rows:
        session.execute('DELETE FROM mode WHERE magic_number IN (%s)', magic_number)
    return print(rows)


@app.route('/api/message', methods=['POST'])
def posted():
    data = json.loads(flask.request.stream, encoding=dict)
    email = data["email"]
    title = data["title"]
    content = data["content"]
    magic_number = data["magic_number"]
    session.execute("INSERT INTO test.mode (email, title, content, magic_number) VALUES %s, %s, %s, %s);", (email, title, content, magic_number))
    rows = session.execute("SELECT* FROM mode")
    return print(rows)


@app.route('/api/message/<email>', methods=['GET'])
def get():
    data = json.load(flask.request.stream, encoding=dict)
    email = data["<email>"]
    rows = session.execute("SELECT* FROM mode WHERE email in %s", email)
    return print(rows)
