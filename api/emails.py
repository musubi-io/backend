from flask import Blueprint
from flask.views import MethodView
from flask import request,g
from flask import jsonify
import utils
emails = Blueprint('emails', __name__)

class emailsAPI(MethodView):
    def post(self):
        data = request.get_json()
        

        # with g.db.cursor() as cur:
        #     cur.execute("INSERT INTO emails (email) VALUES (%s)", (data['email'],))
        print(data)
        # return"hello"
        return jsonify({"message": "Email added"}), 201

emails.add_url_rule('/emails', view_func=emailsAPI.as_view('emailsAPI'),methods = ['POST'])



