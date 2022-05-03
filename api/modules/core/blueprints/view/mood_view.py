
from flask import Blueprint
from arq.view.crud_view import CRUDView
from api.modules.core.blueprints.service.mood.mood_service import MoodService

mood_view_name = 'mood'
mood_blueprint = Blueprint(mood_view_name, __name__)

class MoodView(CRUDView):
    
    def __init__(self) -> None:
        super().__init__(service=MoodService())
    
MoodView.register(mood_blueprint)