
from arq.service.crud_validator import CRUDValidator

class NoteValidator(CRUDValidator):

    def __init__(self) -> None:
        super().__init__(
            required_fields=['pinned', 'text', 'created_in']
        )
