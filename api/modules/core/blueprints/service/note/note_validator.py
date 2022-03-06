
from arq.service.arq_crud_validator import ArqCRUDValidator

class NoteValidator(ArqCRUDValidator):

    def __init__(self) -> None:
        super().__init__(
            required_fields=['pinned', 'text', 'created_in']
        )
