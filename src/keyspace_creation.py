import time

from cassandra.cluster import Cluster
from cassandra.cqlengine.connection import session


def create():
    session.execute("CREATE KEYSPACE IF NOT EXISTS test WITH REPLICATION = { 'class' : 'SimpleStrategy', "
                    "'replication_factor' : 1 }")
    session.set_keyspace("test")
    session.execute('CREATE TABLE IF NOT EXISTS mode  ('
                    'email text PRIMARY KEY,'
                    ' title text,'
                    ' content text,'
                    ' magic_number int'
                    ')')


t0 = time.clock()
y = 1

if time.clock() / 300 * y == 0:
    session.execute('TRUNCATE mode')
    y = y + 1
