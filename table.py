import time
from cassandra.cluster import Cluster

cluster = Cluster(["127.0.0.1"])


session = cluster.connect(["127.0.0.1"])
session.execute("CREATE TABLE node (email text PRIMARY KEY, title text, content text, magic_number int)")


session = cluster.connect(["127.0.0.1"])
t0 = time.clock()
x = 1
if time.clock() / 300 * x == 0:
    session.execute('TRUNCATE node')
    x = x + 1
