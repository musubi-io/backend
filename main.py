from email import policy
import re
from flask import Flask,jsonify
from flask import Blueprint
from flask import g
import sqlite3
from flask_cors import cross_origin, CORS
from flask_mail import Mail, Message
import pytracking
from api import emails,phishEmails,search,events
from flask import request
import imaplib,socket,ssl
from threading import Thread
import concurrent.futures
import time
from email.parser import BytesParser, Parser




con = sqlite3.connect('database.db')
app = Flask(__name__)







CORS(app, resources={r"/api/*": {"origins":"*"}})
# with open("schema.sql") as f:
#     con.executescript(f.read())

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'tonytong011235813@gmail.com'
app.config['MAIL_PASSWORD'] = 'rlze bsqr qdms lrsv'
app.config['MAIL_DEFAULT_SENDER'] = 'tonytong011235813@gmail.com'
mail = Mail(app)

def imap_listener():
    user_email = 'tonytong011235813@gmail.com'
    password = 'rlze bsqr qdms lrsv'
    mail = connect_to_imap(user_email, password)

    last_email_id = None
    first = True
    while True:
        # Select the inbox
        mail.select('inbox')

        # Fetch the latest email
        status, data = mail.search(None, 'ALL')
        
        latest_email_id = data[0].split()[-1]

        if latest_email_id != last_email_id:
            # A new email has arrived
            last_email_id = latest_email_id
            status, data = mail.fetch(latest_email_id, '(RFC822)')

            # Process the email data
            email_data = data[0][1]
            # You can parse the email data using libraries like email or imaplib

            # Perform the desired action
            if not first:
                process_email(email_data)
            else:
                first = False

        # Wait for a certain interval before checking for new emails
        time.sleep(1)  # Check for new emails every 60 seconds

def process_email(raw_data):
    """
    This function processes the raw email data and extracts:
    - When the email was sent
    - Who sent the email
    - The last message in the thread
    - The first email in the thread (bottom of the email chain)
    """
    email_id = raw_data.decode('utf-8')[-3]
    msg = BytesParser(policy=policy.default).parsebytes(raw_data)

    # Who sent the email
    sender = msg['From']
    
    # Extracting the email body content
    body = ""
    if msg.is_multipart():
        for part in msg.iter_parts():
            if part.get_content_type() == 'text/plain':
                body = part.get_payload(decode=True).decode(part.get_content_charset(), errors='replace')
                break
    else:
        body = msg.get_payload(decode=True).decode(msg.get_content_charset(), errors='replace')
    
    # Split the email body into lines
    lines = body.splitlines()

    # Initialize a variable to capture the most recent message
    current_message_lines = []
    
    # Look for the most recent message, which is typically above the last quoted reply
    for line in reversed(lines):
        if line.startswith("On ") and "wrote:" in line:  # A typical delimiter for quoted replies
            break  # Stop collecting lines when we hit the previous message
        current_message_lines.append(line)

    # Reverse the collected lines to get the message in the correct order
    current_message_lines.reverse()

    # Join the lines into a single message
    current_message = "\n".join(current_message_lines).strip()

    sender = sender[sender.index("<")-1:sender.index(">")]
    current_message = current_message[:current_message.index("> On")]
 

    











    
    con = sqlite3.connect('database.db')
    cur = con.cursor()
    cur.execute("Select id from userEmail where email = ?",(sender,))
    user_id = cur.fetchone()[0]
    cur.execute("INSERT INTO scoring (user_id,email_id,reply) VALUES (?,?,?)", (user_id,email_id,current_message))
    cur.commit()

def connect_to_imap(user_email, password):
    imap_server = 'imap.gmail.com'
    imap_port = 993
    mail = imaplib.IMAP4_SSL(imap_server, imap_port)
    mail.login(user_email, password)
    return mail

# Start the IMAP listener in a separate thread
imap_thread = Thread(target=imap_listener)
imap_thread.start()

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



@app.route("/send-mail", methods=["POST"])
def send_mail():
    request_data = request.get_json()

    cur = g.db.cursor()
    cur.execute("SELECT * FROM phishingEmail where nickname = ?",(request_data['name'],))
    emails = cur.fetchone()
    id = emails[0]
    
    subject = emails[2]
    body = emails[3]
    cur.execute("SELECT email FROM userEmail")
    emails = cur.fetchall()
    
    for email in emails:
        # print(email[0])
        msg = Message(
            subject = subject.replace('\n', '').replace('\r', ''), recipients=[email[0]],
            )
        
        msg.body = body+str(id)
        
        mail.send(msg)
    
    return "all mail sent!"









app.register_blueprint(emails.emails,url_prefix='/api')
app.register_blueprint(events.events, url_prefix='/api')
app.register_blueprint(phishEmails.phish_emails,url_prefix='/api')
app.register_blueprint(search.search,url_prefix='/api')

if __name__ == '__main__':
    
    # run the app the debug script in pipfile

    app.run()