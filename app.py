import json
from flask import Flask, request
from flask.json import jsonify
from cassandra.cluster import Cluster
from src.keyspace_creation import create
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
    data = str(request.get_data())
    session.execute("INSERT INTO test.mode JSON '%s'" % data)
    ret = session.execute("SELECT * FROM test.mode")
    return ret


# @app.route('/api/message', methods=['POST'])
# def posted():
#    lm = request.data
#    print(lm)
#    return jsonify({'1'})


@app.route('/api/messages/<email>', methods=['GET'])
def get(email):
    rows = session.execute("SELECT* FROM mode WHERE email IN %s" % email)
    return print(rows)
