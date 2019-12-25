import json
from flask import Flask, request, jsonify
from cassandra.cluster import Cluster
from src.keyspace_creation import create, start, delete

start()
app = Flask(__name__)
cluster = Cluster(["cassandra"], protocol_version=3)
session = cluster.connect()
create()


@app.route('/api/send', methods=['POST'])
def post():
    start()
    data = request.get_json(force=True)
    datain = data["magic_number"]
    raw = session.prepare('SELECT * FROM test.mode WHERE magic_number=? ALLOW FILTERING')
    res = session.execute(raw, [datain])
    delete(datain)
    return jsonify(list(res))


@app.route('/api/message', methods=['POST'])
def posted():
    start()
    data = request.get_json(force=True)
    data = json.dumps(data)
    insert = session.prepare('INSERT INTO test.mode JSON ? USING TTL 300')
    session.execute(insert, [data])
    pop = session.execute("SELECT * FROM test.mode")
    return jsonify(list(pop))


@app.route('/api/messages/<email>', methods=['GET'])
def get(email):
    start()
    req = session.prepare("SELECT* FROM test.mode WHERE email=? ALLOW FILTERING")
    rows = session.execute(req, [email])
    return jsonify(list(rows))
