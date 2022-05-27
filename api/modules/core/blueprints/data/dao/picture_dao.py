
from arq.data.dao.detail_crud_dao import DetailCRUDDAO
from api.modules.core.blueprints.data.model.picture import Picture

class PictureDAO(DetailCRUDDAO):

    def __init__(self) -> None:
        super().__init__(Picture)
