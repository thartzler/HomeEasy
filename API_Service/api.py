from flask import Flask, jsonify, render_template, url_for, request, redirect
from flask_restful import Api, Resource
from azure import identity
import pyodbc, struct, os
import json, codecs
import secrets
import bcrypt
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

# class webSession:

def __make_token():
    """
    Creates a cryptographically-secure, URL-safe db.String
    """
    return secrets.token_urlsafe(50) 

def isSessionValid(sessionID, ipAddress = None):
    """ 
    checks if a given sessionID is still valid. If not, then remove it from the DB? (unless it's desired to keep all sessions in the db)
    """

    if ipAddress:
        preExistingSessions = userSession.query.filter_by(sessionID = sessionID, IPv4_ipAddress = ipAddress).all()
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

def deleteUsersSessions(username):
    """
    Blindly delets all the user sessions in the db for a given username
    """
    oldSession = userSession.query.filter_by(username = username).all()
    for sessn in oldSession:
        db.session.delete(sessn)
    db.session.commit()

def isUsernameValid(username_entry):
    User = userAccount.query.filter_by(username = username_entry).all()
    return len(User)==1

def credentialsValid(username, passHash):
    User = userAccount.query.filter_by(username = username, passHash = passHash).all()
    return len(User)==1

def newSession(username, passHash):
    """
    If the input username and passhash correspond to a user account, 
    all existing sessions are wiped out of the DB, it creates a new, unique sessionID and saves it to the db
    """
    
    User = userAccount.query.filter_by(username = username, passHash = passHash).all()
    print (User)
    if len(User)==1:
        deleteUsersSessions(username)
        #Create a new sessionID
        newSessionID = str(__make_token())

        while isSessionValid(newSessionID)[0]:
            # if the sessionID is currently in the DB, make a new one
            newSessionID = str(__make_token())
            print ("HERE")
        newSession = userSession(sessionID = newSessionID, username = str(User[0].username), loginDatetime = datetime.utcnow())
        db.session.add(newSession)
        db.session.commit()
        return newSession, "New session has been made"
    elif len(User) == 0:
        return False, "Incorrect username or password"
    else:
        return False, "Multiple db records exist for the given username and passHash inputs"

def newLandlordAccount(jsonData):

    # 1. make address
    # 2. make person
    # 3. make userAccount
    # 4. make company
    # 5. make companyAuthority

    requiredAttrs = ['addressDetails',
                     'firstName', 'lastName', 'phoneNumber', 
                     'emailAddress', 'passHash',
                     'companyName', 'companyPhone']
    for attribute in requiredAttrs:
        if attribute not in jsonData:
            print (jsonData)
            return False, "Failed to create Landlord Account: Missing %s in jsonData"%attribute
    # try:
        if 'additionalDetails' in jsonData:
            additionalDetails = jsonData['additionalDetails']
        else:
            additionalDetails = None
        __newUser = newPerson(
            firstName = jsonData['firstName'], 
            lastName = jsonData['lastName'], 
            phoneNumber = jsonData['phoneNumber'], 
            addressDetails = jsonData['addressDetails'],
            additionalDetails=additionalDetails,
            createPerson=None
        )
        
        # accountTypeID = accountType.query.filter_by(typeName='landlord').all()
        newUserAccount = userAccount(
            userID = __newUser.personID,
            accountTypeID = 4,#accountTypeID[0].accountTypeID
            emailAddress = jsonData['emailAddress'],
            passHash = jsonData['passHash'],
            createDate = datetime.utcnow()
        )
        db.session.add(newUserAccount)
        db.session.commit()

        newCompany = company(
            companyID = None,
            companyName = jsonData['companyName'],
            phoneNumber = jsonData['companyPhone'],
            mailingAddress = __newUser.addressID,
            billingAddress = __newUser.addressID,
            emailInvoiceAddress = newUserAccount.emailAddress,
            createdBy = newUserAccount.userID,
            createDate = datetime.utcnow()
        )
        db.session.add(newCompany)
        db.session.commit()


        newCompanyRole = companyRole(
            roleID = None,
            companyID = newCompany.companyID,
            userID = newUserAccount.userID,
            roleTypeID = 5, #roleType.accountTypeID
            role_begin = datetime.utcnow(),
            assignedUser = newUserAccount.userID,
            role_end = None
        )
        db.session.add(newCompanyRole)
        db.session.commit()

        return True, newUserAccount
    # except Exception as e:
    #     return False, e


def newPerson(firstName, lastName, phoneNumber, addressDetails = None, additionalDetails = None, createPerson = None):
    newPersonsAddress = address(
        **addressDetails
    )
    db.session.add(newPersonsAddress)
    db.session.commit()
    
    newPerson = person(
        personID = None,
        firstName = firstName,
        lastName = lastName,
        phoneNumber = phoneNumber,
        addressID = newPersonsAddress.addressID,
        createdOn = datetime.utcnow()
    )
    db.session.add(newPerson)
    db.session.commit()
    # print ('additionalDetails: ', additionalDetails)
    if additionalDetails:
        for detailItem in additionalDetails:
            detailOption = personDetailOption.query.filter_by(propertyName = detailItem).all()
            print('Detail Option: ', detailOption)
            if len(detailOption) == 0:
                detailOption = personDetailOption(
                    propertyName = str(detailItem)
                )
                db.session.add(detailOption)
                db.session.commit()
            else:
                detailOption = detailOption[0]
            if createPerson and hasattr(createPerson, 'personID'):
                createPersonID = createPerson.personID
            else: createPersonID = newPerson.personID
            newDetail = personDetail(
                personID =      newPerson.personID,
                detailID =      detailOption.detailID,
                rev =           0,
                propertyValue = additionalDetails[detailItem],
                setDate =       datetime.utcnow(),
                setPersonID =   createPersonID
            )
            db.session.add(newDetail)
            db.session.commit()
    return newPerson

def getUserFromSessionID(requestHeader, ipAddress = None):
    
    if 'userSessionID' in requestHeader:
        isValid, sessionInfo = isSessionValid(requestHeader['userSessionID'], ipAddress)
        
        if isValid:
            #Now check if the person is authorized
            print(sessionInfo.sessionsOfUser)
            # rows=[]
            # appPaymentStatuses = property.query.filter_by().all()
            # for status in appPaymentStatuses:
            #     rows.append({
            #         'statusID':    status.statusID,
            #         'statusName':  status.statusName,
            #         'isCompleted': status.isCompleted!=b''#, 'big')
            #     })
            return True, sessionInfo.sessionsOfUser
        return False, {"response": 401,
                "message": "Unauthorized: %s"%(sessionInfo)}
    else:
        return False, {"response": 401,
                "message": "Unauthorized: You must be logged in to view this request"}


connection_string = os.environ["AZURE_SQL_CONNECTIONSTRING"]

# Configure Database URI:
params = urllib.parse.quote_plus(os.environ["AZURE_SQL_CONNECTIONSTRING"])

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecret'
app.config['SQLALCHEMY_DATABASE_URI'] = "mssql+pyodbc:///?odbc_connect=%s" % params
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True


api = Api(app)

db.init_app(app)





# current_member = UserMaker().MakeUser()

# current_state = LoggedOutState()

# @app.route('/', methods = ['GET'])
class rentRoll(Resource):

    def get(self):

        gotUser, userResponse = getUserFromSessionID(request.headers, request.remote_addr)
        
        if gotUser:
            print (userResponse)
            data = {
                'name': "Hello",
                'id': "World"
            }
            return (data)
        else:
            return userResponse, userResponse["response"]
    # return render_template('index.html', headerData = current_member.headerContents)

class adminPeople(Resource):

    def get(self):
        people = []
        peopleList = person.query.filter_by().all()
        for listedPerson in peopleList:
            people.append({
                'personID':   listedPerson.personID,
                'firstName':   listedPerson.firstName,
                'lastName':  listedPerson.lastName,
                'phoneNumber': listedPerson.phoneNumber
            })
        return {"people": people}
        gotUser, userResponse = getUserFromSessionID(request.headers, request.remote_addr)
        
        if gotUser:
            print (userResponse)
            data = {
                'name': "Hello",
                'id': "World"
            }
            return (data)
        else:
            return userResponse, userResponse["response"]
    # return render_template('index.html', headerData = current_member.headerContents)


class registerNewUser(Resource):
    
    def post(self):
        # Must be sent through function on the webpage (can't be directly submitted)
        # https://dev.to/amjadmh73/submit-html-forms-to-json-apis-easily-137l
        accountJsonData = {}
        requiredItems = ['address','firstName', 'lastName', 'phoneNumber', 'emailAddress', 'password','companyName', 'companyPhone']
        addressRequirements = ['houseNumber', 'streetName','city','state','zipCode']
        requestData = request.get_json()
        for dataItem in requestData:
            if dataItem in requiredItems:
                requiredItems.remove(dataItem)
                if dataItem == 'address':
                    for addressComp in requestData[dataItem]:
                        if addressComp in addressRequirements:
                            addressRequirements.remove(addressComp)
                    if len(addressRequirements)>=1:
                        return {'status': 400, 'message': "Missing component(s) in the address", "missingField(s)": addressRequirements}, 400
                    accountJsonData['addressDetails'] = requestData[dataItem]
                elif dataItem == 'password':
                    accountJsonData['passHash'] = bcrypt.hashpw(requestData[dataItem].encode('utf-8'),bcrypt.gensalt())
                else:
                    accountJsonData[dataItem] = requestData[dataItem]
            
        if len(requiredItems) >=1:
            return {'status': 400, 'message': "Missing necessary information to create a new user", "missingField(s)": requiredItems}, 400

        wasCreated, result = newLandlordAccount(accountJsonData)
        if wasCreated:
            return {'status': 200, 'message':'Success: Person details saved','userID':str(result.userID)}#,'redirectURL':'./home'}
        else:
            print ( dir(result))
            return {'status': 400, 'message':'Failed to save','error':str(result),'traceback':result.args,'redirectURL':'#'}
    


class getRentRoll(Resource):
    
    def get(self):
        if 'userSessionID' in request.headers:
            isValid, sessionInfo = isSessionValid(request.headers['userSessionID'])
            
            if isValid:
                #Now check if the person is authorized
                print(sessionInfo.sessionsOfUser)
                rows=[]
                appPaymentStatuses = property.query.filter_by().all()
                for status in appPaymentStatuses:
                    rows.append({
                        'statusID':    status.statusID,
                        'statusName':  status.statusName,
                        'isCompleted': status.isCompleted!=b''#, 'big')
                    })
                return rows
            return 'Unauthorized: %s'%(sessionInfo), 401
        else:
            return 'Unauthorized: You must be logged in to view this request', 401

class getAccountType(Resource):
    
    def get(self):
        requestData = request.get_json()

        user = userSession.query.filter_by(sessionID = requestData["sessionID"], IPv4_ipAddress = requestData["ipAddress"]).all()
        
        if user:
            userAccountType = user.sessionsOfUser.accountAuthority.typeName
            if userAccountType:
                return {"userType":userAccountType}
        
        return {'userType':''}

api.add_resource(rentRoll, '/rent')
api.add_resource(getRentRoll, '/admin/rent/roll')
api.add_resource(adminPeople, '/admin/people')
api.add_resource(registerNewUser, '/newLandlord')

api.add_resource(getAccountType, '/getAuthority')

def get_conn():
    # credential = identity.DefaultAzureCredential(exclude_interactive_browser_credential=True)
    # token_bytes = credential.get_token("https://database.windows.net/.default").token.encode("UTF-16-LE")
    # token_struct = struct.pack(f'<I{len(token_bytes)}s', len(token_bytes), token_bytes)
    # SQL_COPT_SS_ACCESS_TOKEN = 1256  # This connection option is defined by microsoft in msodbcsql.h
    conn = pyodbc.connect(connection_string)#, attrs_before={SQL_COPT_SS_ACCESS_TOKEN: token_struct})
    return conn

if __name__ == "__main__":
    app.run(debug=True)