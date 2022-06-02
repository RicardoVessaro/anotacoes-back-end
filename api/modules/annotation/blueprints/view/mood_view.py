
from flask import Blueprint
from api.modules.annotation.blueprints.general.module_constants import REST_API_V1_BASE_URL
from arq.view.crud_view import CRUDView
from api.modules.annotation.blueprints.service.mood.mood_service import MoodService

mood_view_name = MoodService.NAME
mood_blueprint = Blueprint(mood_view_name, __name__)

class MoodView(CRUDView):

    route_prefix = REST_API_V1_BASE_URL

    route_base = mood_view_name
    
    def __init__(self) -> None:
        super().__init__(service=MoodService())
    
MoodView.register(mood_blueprint)