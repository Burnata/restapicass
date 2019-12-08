import re

from flask import Flask
from cassandra.cluster import Cluster
from cassandra.query import tuple_factory

app = Flask(__name__)
cluster = Cluster(["0.0.0.0"])
regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'


@app.route("/api/post")
def post(magic):
    session = cluster.connect(["0.0.0.0"])
    session.row_factory = tuple_factory
    rows = session.execute("SELECT %s FROM node", magic)
    session.execute("DELETE FROM node WHERE magic_number IN (%s)", magic)
    return rows


@app.route("/api/message")
def post(email, title, content, magic):
    if re.search(regex, email):
        session = cluster.connect(["0.0.0.0"])
        session.execute("INSERT INTO node (email,title,content,magic_number) VALUES (%s,%s,%s,%s)",
                        (email, title, content, magic))
    else:
        print("Invalid Email")


@app.route("/api/message/{emailValue}")
def get(self):
    session = cluster.connect(["0.0.0.0"])
    session.row_factory = tuple_factory
    rows = session.execute("SELECT email")
    return rows
