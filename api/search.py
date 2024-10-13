from flask import Blueprint
from flask.views import MethodView
from flask import request,g
from flask import jsonify

search = Blueprint('search', __name__)


class searchEmail(MethodView):
    def get(self):
        cur = g.db.cursor()
        search_val = request.args.get('email')
        print(search_val)
        cur.execute("SELECT * FROM userEmail WHERE email like ?", (f'%{search_val}%',))
        emails = cur.fetchall()
        if emails:
            return jsonify({"email":emails}),200
        else :return jsonify({"message":"No email found"}),404

class searchScore(MethodView):
    def get(self):
        cur = g.db.cursor()
        search_val = request.args.get('email')
        print(search_val)
        cur.execute("SELECT * FROM phishingEmail WHERE score = ?", (search_val,))
        emails = cur.fetchall()
        if emails:
            return jsonify({"email":emails}),200
        else :return jsonify({"message":"No email found"}),404
search.add_url_rule('/emailSearch', view_func=searchEmail.as_view('searchEmail'),methods = ['GET'])