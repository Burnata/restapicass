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
    res = session.execute(raw, [datain])
    count = session.prepare('SELECT COUNT(*) FROM test.mode WHERE magic_number=? ALLOW FILTERING')
    li = json.dumps(list(session.execute(count, [datain])))
    a = int(re.search(r'\d+', li).group())
    a = a-1
    ral = session.prepare('SELECT content FROM test.mode WHERE magic_number=? ALLOW FILTERING')
    rek = session.execute(ral, [datain])
    x = 0
    while a > x:
        race = json.dumps(list(rek)[x])
        dede = session.prepare("UPDATE test.mode USING TTL 1 SET title = 'x' WHERE content=?")
        session.execute(dede, [race])
        x = x + 1
    return jsonify(list(res))


@app.route('/api/message', methods=['POST'])
def posted():
    data = request.get_json(force=True)
    data = json.dumps(data)
    insert = session.prepare('INSERT INTO test.mode JSON ? USING TTL 300')
    session.execute(insert, [data])
    pop = session.execute("SELECT * FROM test.mode")
    return jsonify(list(pop))


@app.route('/api/messages/<email>', methods=['GET'])
def get(email):
    req = session.prepare("SELECT* FROM test.mode WHERE email=? ALLOW FILTERING")
    rows = session.execute(req, [email])
    return jsonify(list(rows))
