
from ipsum.tests.resources.data.dao.fake_test_dao import FakeTestDAO


class FakeEnumTestService:

    def __init__(self) -> None:
        self.save_enums_called = False
        self._dao = FakeTestDAO()

    def save_enums(self):
        self.save_enums_called = True
