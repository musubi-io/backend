from flask import Flask 
from flask import Blueprint
from flask import g
import sqlite3
import os
from api import emails,phishEmails

con = sqlite3.connect('database.db')
app = Flask(__name__)


with open("schema.sql") as f:
    con.executescript(f.read())


@app.before_request
def get_db():
    
    if "db" not in g:
        
        try:
            
            con = sqlite3.connect('database.db')
            g.db = con
        except:
            print("fail")
    


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

app.register_blueprint(emails.emails,url_prefix='/api')
app.register_blueprint(phishEmails.phish_emails,url_prefix='/api')
if __name__ == '__main__':
    
    # run the app the debug script in pipfile

    app.run()