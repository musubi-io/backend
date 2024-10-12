from flask import Blueprint
from flask.views import MethodView

class emailsAPI(MethodView):
    def get(self):
        return "GET emails"
    def post(self):
        return "POST emails"
    def put(self):
        return "PUT emails"
    def delete(self):
        return "DELETE emails"
emails = Blueprint('emails', __name__)


