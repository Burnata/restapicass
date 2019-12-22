import socket
import time

from cassandra.cluster import Cluster


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
