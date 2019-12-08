import time
from cassandra.cluster import Cluster

# table creation script

cluster = Cluster(["0.0.0.0"])
session = cluster.connect(["0.0.0.0"])
session.execute("CREATE TABLE node (email text PRIMARY KEY, title text, content text, magic_number int)")
#t0 = time.clock()
#x = 1

#if time.clock() / 300 * x == 0:
#    session.execute('')  # clearing console script 5 min
#    x = x + 1