from cassandra.cqlengine import columns
from data.Base import Base
import uuid


class Postmagic(Base):
    id = columns.UUID(primary_key=True, default=uuid.uuid4())
    email = columns.Text()
    title = columns.Text()
    content = columns.Text()
    magic_number = columns.Integer()

    def get_data(self):
        return {
            'id': str(self.id),
            'email': self.email,
            'title': self.title,
            'content': self.content,
            'magic_number': self.magic_number,
        }
