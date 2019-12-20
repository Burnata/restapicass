import json
import time
from flask import Flask, request
from cassandra.cluster import Cluster
from src.keyspace_creation import create

# time.sleep(120) #uncommenct on push

app = Flask(__name__)

# table creation script
cluster = Cluster(["cassandra"], protocol_version=3)
session = cluster.connect()
create()


@app.route('/api/send', methods=['POST'])
def post():
    raw = json.dumps(request.json)
    magic_number = raw["magic_number"]
    rows = session.execute('SELECT %s FROM mode' % magic_number)
    for magic_number in rows:
        session.execute('DELETE FROM mode WHERE magic_number IN %s' % magic_number)
    return print(rows)


@app.route('/api/message', methods=['POST'])
def posted():
    data = request.dict_storage_class
    raw = json.dumps(data)
    session.execute("INSERT INTO test.mode JSON %s" % raw)
    return print('1')


@app.route('/api/messages/<email>', methods=['GET'])
def get(email):
    rows = session.execute("SELECT* FROM mode WHERE email in %s" % email)
    return print(rows)
