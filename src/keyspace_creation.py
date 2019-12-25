import json
import socket
import time

from cassandra.cluster import Cluster
from cassandra.query import tuple_factory


def create():
    start()
    cluster = Cluster(["cassandra"], protocol_version=3)
    session = cluster.connect()
    session.execute("CREATE KEYSPACE IF NOT EXISTS test WITH REPLICATION = { 'class' : 'SimpleStrategy', "
                    "'replication_factor' : 1 }")
    session.set_keyspace("test")
    session.execute('CREATE TABLE IF NOT EXISTS test.mode ('
                    'email text,'
                    'title text,'
                    'content text PRIMARY KEY,'
                    'magic_number int'
                    ')')
    return True


def delete(datain):
    start()
    cluster = Cluster(["cassandra"], protocol_version=3)
    session = cluster.connect()
    session.row_factory = tuple_factory
    ses = session.prepare('SELECT COUNT(*) FROM test.mode WHERE magic_number=? ALLOW FILTERING')
    cou = session.execute(ses, [datain])
    # noinspection PyTypeChecker
    count = int(list(filter(str.isdigit, json.dumps(list(cou))))[0])
    # recursion to iterate through the primary keys because cassandra doesnt support iteration through secondary keys
    if count >= 1:
        session.row_factory = tuple_factory
        ra = session.prepare('SELECT content FROM test.mode WHERE magic_number=? ALLOW FILTERING ')
        raw = session.execute(ra, [datain])
        rawer = list(raw)[0]
        dede = session.prepare("DELETE FROM test.mode WHERE content=?")
        session.execute(dede, rawer)
        return delete(datain)
    else:
        return 0


def start():
    s = socket.socket()
    try:
        s.connect(("cassandra", 9042))
        return True
    except socket.error as e:
        time.sleep(1)
        return start()
    finally:
        s.close()
