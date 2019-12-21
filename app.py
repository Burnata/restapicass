import json
import re
import time

from flask import Flask, request, jsonify
from cassandra.cluster import Cluster
from src.keyspace_creation import create
app = Flask(__name__)

# table creation script
cluster = Cluster(["cassandra"], protocol_version=3)
session = cluster.connect()
create()


@app.route('/api/send', methods=['POST'])
def post():
    data = request.get_json(force=True)
    data = json.dumps(data)
    datain = int(re.search(r'\d+', data).group())
    raw = session.prepare('SELECT * FROM test.mode WHERE magic_number=? ALLOW FILTERING')
    session.execute(raw, [datain])
    de = session.prepare('DELETE FROM test.mode WHERE magic_number IN ?')
    session.execute(de, [datain])
    return jsonify(list(raw))


@app.route('/api/message', methods=['POST'])
def posted():
    data = request.get_json(force=True)
    data = json.dumps(data)
    insert = session.prepare('INSERT INTO test.mode JSON ?')
    session.execute(insert, [data])
    pop = session.execute("SELECT * FROM test.mode")
    timer = time.clock()

    return jsonify(list(pop))


@app.route('/api/messages/<email>', methods=['GET'])
def get(email):
    req = session.prepare("SELECT* FROM test.mode WHERE email=? ALLOW FILTERING")
    rows = session.execute(req, [email])
    return jsonify(list(rows))
