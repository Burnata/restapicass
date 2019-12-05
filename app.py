from cassandra.cluster import Cluster
import cassandra
import time
import re

cluster = Cluster('casstest://127.0.0.1:9160')
regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'


def post(self):
    session = cluster.connect('node')
    rows = session.execute("SELECT content")
    return rows

def post(email,title,content,magic):
    if (re.search(regex, email)):
        print()
    else:
        print("Invalid Email")
    session = cluster.connect('node')
    session.execute("INSERT INTO node (email,title,content,magic_number) "
                               "VALUES(email,title,content,magic)")

def get(self):
    session = cluster.connect('node')
    rows = session.execute("SELECT email")
    return rows


def timer():
    session = cluster.connect('node')
    t0 = time.clock()
    x = 1
    if time.clock() / 300 * x == 0:
        session.execute('TRUNCATE node')
        x = x + 1
