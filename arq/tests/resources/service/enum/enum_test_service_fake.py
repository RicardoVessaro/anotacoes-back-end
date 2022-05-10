
class EnumTestServiceFake:

    def __init__(self) -> None:
        self.save_enums_called = False

    def save_enums(self):
        self.save_enums_called = True
