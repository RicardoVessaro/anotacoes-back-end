from xml.dom.minidom import Document
from arq.data.dao.detail_crud_dao import DetailCRUDDAO
from api.annotation.blueprints.data.model.link import Link

class LinkDAO(DetailCRUDDAO):
    
    def __init__(self) -> None:
        super().__init__(model=Link)
