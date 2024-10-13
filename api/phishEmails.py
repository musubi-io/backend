from flask import Blueprint
from flask.views import MethodView
from flask import request,g
from flask import jsonify
import requests
import re
import os
phish_emails = Blueprint('phishEmails', __name__)

class generateEmail(MethodView):
    def post(self):
        data = request.get_json()
        
        URL = r'https://llm.kindo.ai/v1/chat/completions'
        MODEL = r'azure/gpt-4o'
        API_KEY = os.getenv("KINDO_AI_API_KEY")
        headers = {
            'api-key': f'{API_KEY}',
            'content-type':"application/json"
        }
        payload = {
            'model':MODEL,
            'messages':[
                {
                    'role':'system',
                    'content':"""Write an email designed to phish a user . 
                                Make the email look as legitimate as possible. 
                                DO NOT INCLUDE Sender or Recipient details.

                                IF AND ONLY IF a link is specified in the prompt:
                                - DO NOT INCLUDE more than one link.
                                - Format the link like so with the content replacing LINK: <LINK>

                                Write the email in markdown code."""
                },
                {
                    'role':'user',
                    'content':f"""Write a phishing email from: {data['sender']}
                    Goal of attack: {data['goal']}
                    With the context: {data['context']}"""
                }
            ]
        }
        while True:
            response = requests.post(URL,headers = headers, json = payload)
            if response.status_code == 200:
                    
                
                    pattern =r'```markdown(.+)```'
                    content = response.json()["choices"][0]['message']['content']
                    print(type(content))
                    result = re.search(pattern,str(content),re.DOTALL)
                    try:
                        email = result.group(1)
                        secondary_parse = r'(\nSubject:.+?\n)(.+)'
                        result = re.search(secondary_parse,email,re.DOTALL)

                        
                        return jsonify({"subject":result.group(1),"body":result.group(2)}),200
                    except AttributeError:
                        print("here")
                        continue
                    
            else:

                return jsonify({"error":"api issue"}),400
        
class phishEmail(MethodView):
    def post(self):
        data = request.get_json()
        cur = g.db.cursor()
        try:
            cur.execute("INSERT INTO phishingEmail (nickname,email_subject,email_body) VALUES (?,?,?)", (data["name"],data['subject'],data['body']))
            g.db.commit()
            return jsonify({"message":"Email stored"}),201
        except Exception as e:
            print(e)
            return jsonify({"message":"Database error"}),500
    def get(self):
        name = request.args.get("name")
        cur = g.db.cursor()
        cur.execute("SELECT * FROM phishingEmail where nickname = ?",(name,))
        res = cur.fetchall()
        if res == []:
            return jsonify({"message":f"No email with the name {name}"}),404
        res = res[0]
        
        # return jsonify({"emails":res}),200
        return jsonify({"id":res[0],
                        "name":res[1],
                        "Subject":res[2],
                        "Body":res[3]}),200
        
    
        
        
phish_emails.add_url_rule('/phishEmails', view_func=phishEmail.as_view('phishEmails'),methods = ['POST','GET'])
phish_emails.add_url_rule('/generatePhishEmails', view_func=generateEmail.as_view('generateEmail'),methods = ['POST'])