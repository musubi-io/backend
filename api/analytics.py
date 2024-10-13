from flask import Blueprint
from flask.views import MethodView
from flask import request,g
from flask import jsonify

analytics = Blueprint('analytics', __name__)

class EmailAnalytics(MethodView):
    def get(self):
        cur = g.db.cursor()
        cur.execute("SELECT * FROM userEmail")
        emails = cur.fetchall()
        return jsonify({"emails":emails}),200