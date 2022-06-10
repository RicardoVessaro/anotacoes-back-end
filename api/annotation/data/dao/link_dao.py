from xml.dom.minidom import Document
from ipsum.data.dao.detail_crud_dao import DetailCRUDDAO
from api.annotation.data.model.link import Link

class LinkDAO(DetailCRUDDAO):

    model_name = 'Link'
    
    def __init__(self) -> None:
        super().__init__(model=Link)
