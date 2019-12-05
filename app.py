import re

from cassandra.cluster import Cluster
from cassandra.query import tuple_factory


cluster = Cluster(["0.0.0.0"])
regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'


def post(self):
    session = cluster.connect(["0.0.0.0"])
    session.row_factory = tuple_factory
    rows = session.execute("SELECT *")
    return rows


def post(email, title, content, magic):
    if re.search(regex, email):
        session = cluster.connect(["0.0.0.0"])
        session.execute("INSERT INTO node (email,title,content,magic_number) VALUES (%s,%s,%s,%s)",
                        (email, title, content, magic))
    else:
        print("Invalid Email")


def get(self):
    session = cluster.connect(["0.0.0.0"])
    session.row_factory = tuple_factory
    rows = session.execute("SELECT email")
    return rows
