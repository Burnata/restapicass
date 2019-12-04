from cassandra.cluster import Cluster
import cassandra


cluster = Cluster('casstest://localhost:2375')


class message():
    def post(self):
        session = cluster.connect('node')
        rows = session.execute("SELECT content")
        return rows

class write():
    def post(self):
        session = cluster.connect('node')
        rows = session.execute("")
        return rows

class emailValue():
    def get(self):
        session = cluster.connect('node')
        rows = session.execute("SELECT email")
        return rows
class reset():
    def timer():
        t =