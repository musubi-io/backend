from flask import Blueprint
from flask.views import MethodView
from flask import request,g
from flask import jsonify
import sqlite3
import utils

emails = Blueprint('emails', __name__)

class emailsAPI(MethodView):
    def post(self):
        data = request.get_json()
        if 'file' not in request.files:
            
            if not data.get("email",False):
                return jsonify({"message":"Email Where???"}),400
            if not utils.validate_email(data['email']):
                return jsonify({"message":"Invalid email"}),400
            
            
            try:
                cur = g.db.cursor()
                cur.execute("INSERT INTO userEmail (email) VALUES (?)", (data['email'],))
                g.db.commit()
            except sqlite3.Error as e:
                g.db.rollback()  # Rollback in case of error
                return jsonify({"message": f"Database error: {e}"}), 500
            
            
            
            return jsonify({"message": "Email added"}), 201
        
        print("here")
        return jsonify({"test":"test"}),200

emails.add_url_rule('/emails', view_func=emailsAPI.as_view('emailsAPI'),methods = ['POST'])



