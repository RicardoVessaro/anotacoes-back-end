
from ipsum.service.crud_validator import CRUDValidator

class NoteValidator(CRUDValidator):

    def __init__(self, dao) -> None:
        super().__init__(
            dao, required_fields=['pinned', 'text', 'created_in']
        )
