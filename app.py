import json
import re
from functools import wraps

import flask
from flask import Flask, Response
from cassandra.cluster import Cluster
from JSON import util
from data.postmagic import postmagi
from src.keyspace_creation import create

app = Flask(__name__)

regex = '/^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
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
@json
def post():
    data = json.loads(flask.request.data)
    rows = session.execute('SELECT %s FROM mode', magic_number=data["magic_number"])
    for data["magic_number"] in rows:
        session.execute('DELETE FROM mode WHERE magic_number IN (%s)', magic_number=data["magic_number"])
        return postmagi.get_data()


@app.route('/api/message', methods=['POST', 'GET'])
@json
def posted(email, title, content, magic):
    if re.search(regex, email):
        x = session.execute('INSERT INTO mode (email,title,content,magic_number) VALUES (%s,%s,%s,%s)',
                            (email, title, content, magic))
        return print(x)
    else:
        return print("invalid email")


@app.route('/api/message/{text:email}', methods=['POST', 'GET'])
@json
def get(email):
    if re.search(regex, email):
        rows = session.execute('SELECT %s FROM mode', email)
        for printed in rows:
            return print(rows.email, rows.title, rows.content, rows.magic)
    else:
        return print("invalid email")
