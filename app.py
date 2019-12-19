import json
from functools import wraps
import flask
from flask import Flask, Response
from cassandra.cluster import Cluster
from JSON import util
from data.postmagic import Postmagic
from src.keyspace_creation import create

app = Flask(__name__)

# table creation script
cluster = Cluster(["cassandra"], protocol_version=3)
session = cluster.connect()
create()


def json_api(f):
    @wraps(f)
    def decorated_function(*args):
        result = f(*args)
        json_result = util.to_json(result)
        return Response(response=json_result,
                        status=200,
                        mimetype="application/json")

    return decorated_function


@app.route('/api/send', methods=['POST'])
@json_api
def post():
    data = json.loads(flask.request.data)
    rows = session.execute('SELECT %s FROM mode', magic_number=data["magic_number"])
    for data["magic_number"] in rows:
        session.execute('DELETE FROM mode WHERE magic_number IN (%s)', magic_number=data["magic_number"])
        return Postmagic.get_data(session)


@app.route('/api/message', methods=['POST'])
@json_api
def posted():
    data = json.load(flask.request.data)
    Postmagic.create(email=data["email"], title=data["title"], magic_number=data["magic_number"])
    Postmagic.save(session)
    return Postmagic.get_data(session)


@app.route('/api/message/<email>', methods=['GET'])
def get(email):
    x = session.execute("SELECT * WHERE %s", email)
    return print(x)
