
from collections import namedtuple


class FakeTestDAO:

    def __init__(self) -> None:
        pass

    def find(self):
        fake_model = namedtuple('FakeModel', 'id')

        return [
            fake_model(1),
            fake_model(2)
        ]

    def delete(self, id):
        pass