import json
import time
from functools import wraps
import flask
from flask import Flask, Response
from cassandra.cluster import Cluster
from JSON import util
from data.postmagic import magic
from src.keyspace_creation import create
import requests

# time.sleep(120) #uncommenct on push

app = Flask(__name__)

# table creation script
cluster = Cluster(["cassandra"], protocol_version=3)
session = cluster.connect()
create()


def json_api(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        result = f(*args, **kwargs)  # Call Function
        json_result = util.to_json(result)
        return Response(response=json_result,
                        status=200,
                        mimetype="application/json")

    return decorated_function


@app.route('/api/send', methods=['POST'])
def post():
    data = json.loads(flask.request.from_values, encoding=dict)
    magic_number = data["magic_number"]
    rows = session.execute('SELECT %s FROM mode', magic_number)
    for data["magic_number"] in rows:
        session.execute('DELETE FROM mode WHERE magic_number IN (%s)', magic_number)
    return print(rows)


@app.route('/api/message', methods=['POST'])
@json_api
def posted():
    data = json.load(flask.request.stream)
    magic.create(email=data["email"], title=data["title"], content=data["content"], magic_number=data["magic_number"])
    magic.save()
    return magic.get_data()


@app.route('/api/message/<email>', methods=['GET'])
def get():
    data = json.load(flask.request.from_values, encoding=dict)
    email = data["<email>"]
    rows = session.execute("SELECT* FROM mode WHERE email in %s", email)
    return print(rows)
