import re
import time

from flask import Flask
from cassandra.cluster import Cluster
from cassandra.query import tuple_factory

app = Flask(__name__)

cluster = Cluster(["0.0.0.0"])
regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'


# table creation script

@app.route("/")
def table():
    session = cluster.connect(["0.0.0.0"])
    session.execute("CREATE TABLE node (email text PRIMARY KEY, title text, content text, magic_number int)")


# t0 = time.clock()
# x = 1

# if time.clock() / 300 * x == 0:
#    session.execute('')  # clearing console script 5 min
#    x = x + 1


@app.route("/api/send/")
def post(magic):
    session = cluster.connect(["0.0.0.0"])
    session.row_factory = tuple_factory
    rows = session.execute("SELECT %s FROM node", magic)
    session.execute("DELETE FROM node WHERE magic_number IN (%s)", magic)
    return rows


@app.route("/api/message/")
def post(email, title, content, magic):
    if re.search(regex, email):
        session = cluster.connect(["0.0.0.0"])
        session.execute("INSERT INTO node (email,title,content,magic_number) VALUES (%s,%s,%s,%s)",
                        (email, title, content, magic))
    else:
        return "Invalid Email"


@app.route("/api/message/{text:email}")
def get(email):
    if re.search(regex, email):
        session = cluster.connect(["0.0.0.0"])
        rows = session.execute("SELECT %s", email)
        return rows
    else:
        return "Invalid Email"
