import time

from cassandra.cluster import Cluster

cluster = Cluster(["cassandra"], protocol_version=3)
session = cluster.connect()
t = time.clock()


def create():
    session.execute("CREATE KEYSPACE IF NOT EXISTS test WITH REPLICATION = { 'class' : 'SimpleStrategy', "
                    "'replication_factor' : 1 }")
    session.set_keyspace("test")
    session.execute('CREATE TABLE IF NOT EXISTS mode ('
                    'email text PRIMARY KEY,'
                    'title text,'
                    'content text,'
                    'magic_number int'
                    ')')


def timed():
    if t / 300 >= 0:
        session.execute('TRUNCATE mode')
        t = 0
