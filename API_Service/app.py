from flask import Flask, jsonify, render_template, url_for, request, redirect
from flask_restful import Api, Resource
from azure import identity
import pyodbc, struct, os
import json
import secrets
import urllib.parse
# from wtforms import Form, BooleanField, StringField, PasswordField, validators

from datetime import datetime, timedelta
# import secrets
# from userTypes import UserMaker
from DB_ORM import *#db, userSession, webSession, property

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

class webSession:

    def __make_token(self):
        """
        Creates a cryptographically-secure, URL-safe db.String
        """
        return secrets.token_urlsafe(24) 

    def isSessionValid(self, sessionID, username = None):
        """ 
        checks if a given sessionID is still valid. If not, then remove it from the DB? (unless it's desired to keep all sessions in the db)
        """

        if username:
            preExistingSessions = userSession.query.filter_by(sessionID = sessionID, username = username).all()
        else:
            preExistingSessions = userSession.query.filter_by(sessionID = sessionID).all()
        # tuple of all sessions in the db with the same session ID (should only be max 1)

        if len(preExistingSessions) > 0:
            # If the session exists, check the validity of it's date
            validUserSession = None
            
            for PES in preExistingSessions:
                if datetime.utcnow() - timedelta(days=1) > PES.loginDatetime:
                    # print ("Removing old session - ", PES)
                    db.session.delete(PES)
                elif validUserSession is not None:
                    # for some reason if there is more than 1 valid session, delete the previous valid session and mark the newly found session as valid user session
                    # print (validUserSession)
                    db.session.delete(validUserSession)
                    validUserSession = PES
                else:
                    validUserSession = PES

            db.session.commit()
            return True, validUserSession
        else:
            # print ("Session has expired")
            return False, "Session has expired"

    def deleteUsersSessions(self, username):
        """
        Blindly delets all the user sessions in the db for a given username
        """
        oldSession = userSession.query.filter_by(username = username).all()
        for sessn in oldSession:
            db.session.delete(sessn)
        db.session.commit()

    def isUsernameValid(self, username_entry):
        User = userAccount.query.filter_by(username = username_entry).all()
        return len(User)==1

    def credentialsValid(self, username, passHash):
        User = userAccount.query.filter_by(username = username, passHash = passHash).all()
        return len(User)==1
    
    def newSession(self, username, passHash):
        """
        If the input username and passhash correspond to a user account, 
        all existing sessions are wiped out of the DB, it creates a new, unique sessionID and saves it to the db
        """
        
        User = userAccount.query.filter_by(username = username, passHash = passHash).all()
        print (User)
        if len(User)==1:
            self.deleteUsersSessions(username)
            #Create a new sessionID
            newSessionID = str(self.__make_token())

            while self.isSessionValid(newSessionID)[0]:
                # if the sessionID is currently in the DB, make a new one
                newSessionID = str(self.__make_token())
                print ("HERE")
            newSession = userSession(sessionID = newSessionID, username = str(User[0].username), loginDatetime = datetime.utcnow())
            db.session.add(newSession)
            db.session.commit()
            return newSession, "New session has been made"
        elif len(User) == 0:
            return False, "Incorrect username or password"
        else:
            return False, "Multiple db records exist for the given username and passHash inputs"

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