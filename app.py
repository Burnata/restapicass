import json
import time
from flask import Flask, request, jsonify
from cassandra.cluster import Cluster
from src.keyspace_creation import create
from werkzeug.datastructures import ImmutableMultiDict

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
    data = dict(request.form)
    kpop = data.keys()
    pop = str(list(kpop))
    onepop = pop.replace("[", "")
    twopop = onepop.replace('{', "")
    threepop = twopop.replace(']', "")
    fourpop = threepop.replace('}', "")
    fivepop = fourpop.replace('"', "")
    sixpop = fivepop.replace("'", "")
    rpop = sixpop.split(",")
    rw = json.dumps(rpop)
    #hw = jsonify(rw)
    #session.execute("INSERT INTO test.mode JSON %s" % hw)
    return rw


# @app.route('/api/message', methods=['POST'])
# def posted():
#    lm = request.data
#    print(lm)
#    return jsonify({'1'})


@app.route('/api/messages/<email>', methods=['GET'])
def get(email):
    rows = session.execute("SELECT* FROM mode WHERE email IN %s" % email)
    return print(rows)
