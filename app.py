import json
from flask import Flask, request
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
    rows = session.execute('SELECT %s FROM test.mode' % data)
    for data in rows:
        de = session.prepare('DELETE FROM test.mode WHERE magic_number IN ?')
        session.execute(de, [data])
    return print(str(rows))


@app.route('/api/message', methods=['POST'])
def posted():
    data = request.get_json(force=True)
    data = json.dumps(data)
    insert = session.prepare('INSERT INTO test.mode JSON ?')
    session.execute(insert, [data])
    pop = session.execute("SELECT * FROM test.mode")
    return print(str(pop))


@app.route('/api/messages/<email>', methods=['GET'])
def get(email):
    req = session.prepare("SELECT* FROM test.mode WHERE email IN ?")
    rows = session.execute(req, [email])
    return print(str(rows))
