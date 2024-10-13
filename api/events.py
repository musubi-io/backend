from flask import Blueprint
from flask.views import MethodView
from flask import request,g
from flask import jsonify
import csv
from io import StringIO
import sqlite3
import utils

events = Blueprint("events", __name__)

class eventsAPI(MethodView):
    def post(self):
        data = request.get_json()
        print(data)
        return jsonify({'message': 'Received!'}), 200 
    
    pass

events.add_url_rule('/events', view_func=eventsAPI.as_view('eventsAPI'), methods=['POST'])