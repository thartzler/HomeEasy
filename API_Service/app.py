from flask import Flask, jsonify, render_template, url_for, request, redirect
from flask_restful import Api, Resource
from azure import identity
import pyodbc, struct, os
import json
import urllib.parse
# from wtforms import Form, BooleanField, StringField, PasswordField, validators

# from datetime import datetime, timedelta
# import secrets
# from userTypes import UserMaker
# from DB_ORM import db#, Department, webSession, property

# from SessionStates import LoggedInState, LoggedOutState


# from DB_Object_Creator import 
# class newUserForm(Form):
#     firstName= StringField('First Name*', [validators.DataRequired(), validators.Regexp('[A-Za-z]+')])
#     lastName= StringField('Last Name*', [validators.DataRequired(), validators.Regexp('[A-Za-z]+')])
#     companyName= StringField('Company Name*', [validators.DataRequired(), validators.Regexp('[A-Za-z]+')])
#     email= StringField('Email Address*', [validators.DataRequired()])
#     address= StringField('Address*', [validators.DataRequired()])
#     city= StringField('City*', [validators.DataRequired()])
#     state= StringField('State*', [validators.DataRequired(), validators.Regexp('[A-Z]{2}')])
#     zipCode= StringField('Zip Code*', [validators.DataRequired(), validators.Regexp('[0-9]+')])
#     phone= StringField('Phone Number*', [validators.DataRequired()])
#     password= PasswordField('Password*', [
#             validators.DataRequired(),\
#             validators.EqualTo('password_confirm', message='Passwords must match!')\
#         ])
#     password_confirm= PasswordField('Verify Password*', [validators.DataRequired()])

connection_string = os.environ["AZURE_SQL_CONNECTIONSTRING"]

# Configure Database URI:
params = urllib.parse.quote_plus(os.environ["AZURE_SQL_CONNECTIONSTRING"])

app = Flask(__name__)


api = Api(app)
app.config['SECRET_KEY'] = 'supersecret'
app.config['SQLALCHEMY_DATABASE_URI'] = "mssql+pyodbc:///?odbc_connect=%s" % params
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

# db.init_app(app)





# current_member = UserMaker().MakeUser()

# current_state = LoggedOutState()

# @app.route('/', methods = ['GET'])
class rentRoll(Resource):

    def get(self):
        data = {
            'name': "Hello",
            'id': "World"
        }
        return (data)
    # return render_template('index.html', headerData = current_member.headerContents)

class getRentRoll(Resource):
    
    def get(self):
        rows=[]
        with get_conn() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM appPaymentStatus")
            
            for row in cursor.fetchall():
                print(row.statusID, row.statusName, row.isCompleted)
                rows.append({
                     'statusID':    row.statusID,
                     'statusName':  row.statusName,
                     'isCompleted': row.isCompleted})
        return rows

api.add_resource(rentRoll, '/rent')
api.add_resource(getRentRoll, '/admin/rent/roll')

def get_conn():
    # credential = identity.DefaultAzureCredential(exclude_interactive_browser_credential=True)
    # token_bytes = credential.get_token("https://database.windows.net/.default").token.encode("UTF-16-LE")
    # token_struct = struct.pack(f'<I{len(token_bytes)}s', len(token_bytes), token_bytes)
    # SQL_COPT_SS_ACCESS_TOKEN = 1256  # This connection option is defined by microsoft in msodbcsql.h
    conn = pyodbc.connect(connection_string)#, attrs_before={SQL_COPT_SS_ACCESS_TOKEN: token_struct})
    return conn

if __name__ == "__main__":
    app.run(debug=True)