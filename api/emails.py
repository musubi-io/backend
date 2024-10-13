from flask import Blueprint
from flask.views import MethodView
from flask import request,g
from flask import jsonify
import csv
from io import StringIO
import sqlite3
import utils

emails = Blueprint('emails', __name__)

class emailsAPI(MethodView):
    def post(self):
        
        if 'emailFile' not in request.files:
            
            data = request.get_json()
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
        file = request.files['emailFile']
        if not file.filename.endswith('.csv'):
            return jsonify({"message":"Invalid file type"}),400
        else:
            stream = StringIO(file.stream.read().decode("UTF8"))
            csv_reader = csv.reader(stream)
            cur = g.db.cursor()
            errors = []
            for email in csv_reader:
                if utils.validate_email(email[0]):
                    cur.execute("INSERT INTO userEmail (email) VALUES (?)", (email[0],))
                    
                else:
                    errors.append(email[0])
            g.db.commit()
        if errors:
            return jsonify({"message":"Some emails were not added","errors":errors}),201
        else: return jsonify({"message":"all emails added"}),200
    
    def get(self):
        cur = g.db.cursor()
        cur.execute("SELECT * FROM userEmail")
        emails = cur.fetchall()
        return jsonify({"emails":emails}),200

emails.add_url_rule('/emails', view_func=emailsAPI.as_view('emailsAPI'),methods = ['POST','GET'])



