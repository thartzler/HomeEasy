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
from DB_ORM import *#db, userSession, webSession, property


def __make_token():
    """
    Creates a cryptographically-secure, URL-safe db.String
    """
    return secrets.token_urlsafe(37) 

def isSessionValid(sessionID, ipAddress = None):
    """ 
    checks if a given sessionID is still valid. If not, then remove it from the DB? (unless it's desired to keep all sessions in the db)
    """
    print ("CHECKING SESSION")
    if ipAddress:
        print ('sessionID: ', sessionID)
        print ('IPAddress: ', ipAddress)
        preExistingSessions = userSession.query.filter_by(sessionID = sessionID, IPv4_ipAddress = ipAddress).all()
    else:
        preExistingSessions = userSession.query.filter_by(sessionID = sessionID).all()
    # tuple of all sessions in the db with the same session ID (should only be max 1)
    print ("PES: ",preExistingSessions)
    if len(preExistingSessions) > 0:
        # If the session exists, check the validity of it's date
        validUserSession = None
        
        for PES in preExistingSessions:
            if datetime.utcnow() <= PES.expiredDatetime:
                # less than 7 days after initial signin
                if datetime.utcnow() <= PES.nextDatetime:
                    # less than 1 day since the last usage
                    if validUserSession is not None:
                        db.session.delete(validUserSession)
                    validUserSession = PES
                    # print ("Welcome, last activity was: ",PES.nextDateTime - timedelta(days= 1))
                    PES.nextDatetime = datetime.utcnow() + timedelta(days= 1)
                else:
                    # print ("Deleting session since it wasn't used in the last 24 hrs")
                    db.session.delete(PES)
            else:
                # print ("Deleting session since it has been 7 days since login")
                db.session.delete(PES)
                
        db.session.commit()
        if validUserSession:
            return True, validUserSession
        return False, "Session has expired"
    return False, "No such session"

def deleteUsersSessions(user):
    """
    Blindly delets all the user sessions in the db for a given username
    """
    userAccountSessions = userSession.query.filter_by(userID = user.userID).all()
    for session in userAccountSessions:
        db.session.delete(session)
    db.session.commit()

def newSession(username, password, ipAddress):
    """
    If the given username and passhash correspond to a user account, 
    all existing sessions are wiped out of the DB, it creates a new, unique sessionID and saves it to the db
    """
    User = None
    UsersWithEmail = userAccount.query.filter_by(emailAddress = username).all()
    for userWithEmail in UsersWithEmail:
        if bcrypt.checkpw(password.encode('utf-8'), userWithEmail.passHash.encode('utf-8')):
            if User:
                print("ERROR: Multiple db records exist for the given username and passHash inputs")
            User = userWithEmail
    if User:
        print (User)
        deleteUsersSessions(User)
        #Create a new sessionID
        newSessionID = str(__make_token())

        while isSessionValid(newSessionID)[0]:
            # if the sessionID is currently in the DB, make a new one
            print ("Duplicate SessionID found")
            newSessionID = str(__make_token())
        session2Add = userSession(sessionID = newSessionID, userID = str(User.userID), IPv4_ipAddress = ipAddress, loginDatetime = datetime.utcnow(), expiredDatetime = datetime.utcnow()+timedelta(days = 7), nextDatetime = datetime.utcnow()+timedelta(days = 1))
        # Basically the session expires after 7 days regardless. If the usersession gets queried, the nextDatetime gets changed to current time + 1 day. The session expires when current time is after either nextDatetime or expiredDatetime
        db.session.add(session2Add)
        db.session.commit()
        return {'status': 200, 'message': "New session has been made", 'sessionID': session2Add.sessionID, 'userType': User.accountAuthority.typeName}
    elif UsersWithEmail:
        return {'status': 400, 'message': "Incorrect password"}
    else:
        return {'status': 400, 'message': "Incorrect username"}

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
    addressID = createNewAddress(**jsonData['addressDetails'])

    __newUser = newPerson(
        firstName = jsonData['firstName'], 
        lastName = jsonData['lastName'], 
        phoneNumber = jsonData['phoneNumber'], 
        addressID = addressID,
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
        mailingAddress = addressID,
        billingAddress = addressID,
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

def createTenant(jsonData):

    # 1. make person
    # 2. make userAccount

    requiredAttrs = ['additionalDetails',
                     'firstName', 'lastName', 'phoneNumber', 
                     'emailAddress', 'passHash', 'createdBy']
    for attribute in requiredAttrs:
        if attribute not in jsonData:
            print (jsonData)
            return False, "Failed to create Tenant Account: Missing %s in jsonData"%attribute

    __newUser = newPerson(
        firstName = jsonData['firstName'], 
        lastName = jsonData['lastName'], 
        phoneNumber = jsonData['phoneNumber'], 
        addressID = None,
        additionalDetails=jsonData['additionalDetails'],
        createPerson=jsonData['createdBy']
    )
    
    # accountTypeID = accountType.query.filter_by(typeName='landlord').all()
    newUserAccount = userAccount(
        userID = __newUser.personID,
        accountTypeID = 3,#accountTypeID[0].accountTypeID
        emailAddress = jsonData['emailAddress'],
        passHash = jsonData['passHash'],
        createDate = datetime.utcnow()
    )
    db.session.add(newUserAccount)
    db.session.commit()

    return True, newUserAccount
    # except Exception as e:
    #     return False, e


def createProperty(jsonData):

    # 1. make property

    requiredAttrs = ['companyID', 'addressID','bedroomCount','bathroomCount',
                         'parkingCount', 'garageCount', 'storiesCount', 'homeType', 'yearBuilt',
                         'purchasePrice', 'purchaseDate', 'schoolDistrict', 'nickname', 'createUser']
    filteredJson = {}
    for attribute in requiredAttrs:
        if attribute not in jsonData:
            print (jsonData)
            print ("Failed to create Property: Missing %s in jsonData"%attribute)
            return False
        filteredJson[attribute] = jsonData[attribute]
    filteredJson['createDate'] = datetime.utcnow()
    print ("FilteredJson: ", filteredJson)
    newProperty = property(**filteredJson)
    print ("New Property: ", newProperty)
    db.session.add(newProperty)
    db.session.commit()

    return newProperty.propertyID


def createNewAddress(houseNumber, streetName, city, state, zipCode, apptNo = None):
    newAddress = address(
        houseNumber = houseNumber,
        streetName = streetName,
        apptNo = apptNo,
        city = city, 
        state = state,
        zipCode = zipCode
    )
    db.session.add(newAddress)
    db.session.commit()

    return newAddress.addressID


def newPerson(firstName, lastName, phoneNumber, addressID = None, additionalDetails = None, createPerson = None):
    
    newPerson = person(
        personID = None,
        firstName = firstName,
        lastName = lastName,
        phoneNumber = phoneNumber,
        addressID = addressID,
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
            if createPerson:
                if hasattr(createPerson, 'personID'):
                    createPersonID = createPerson.personID
                elif hasattr(createPerson, 'userID'):
                    createPersonID = createPerson.userID
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
            print(sessionInfo.sessionUser)
            # rows=[]
            # appPaymentStatuses = property.query.filter_by().all()
            # for status in appPaymentStatuses:
            #     rows.append({
            #         'statusID':    status.statusID,
            #         'statusName':  status.statusName,
            #         'isCompleted': status.isCompleted!=b''#, 'big')
            #     })
            return True, sessionInfo.sessionUser
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




class getAccountType(Resource):
    
    def get(self):
        requiredItems = ['sessionID', 'ipAddress']
        requestData = request.get_json()
        jsonData = {}
        for dataItem in requestData:
            if dataItem in requiredItems:
                requiredItems.remove(dataItem)
                jsonData[dataItem] = requestData[dataItem]

        if len(requiredItems) >=1:
            return {'status': 400, 'message': "Missing necessary information to check sessionID", "missingField(s)": requiredItems}, 400
        # print ("REQ: ", requestData)
        # print ('Jsondata: ', jsonData)
        # print ('Reqdata: ', requiredItems)
        
        user = userSession.query.filter_by(sessionID = requestData["sessionID"], IPv4_ipAddress = requestData["ipAddress"]).first()
        
        if user:
            userAccountType = user.sessionUser.accountAuthority.typeName
            if userAccountType:
                return {"userType":userAccountType}
        
        return {'userType':''}

class createSessionID(Resource):
    
    def post(self):
        requiredItems = ['username', 'password', 'ipAddress']
        requestData = request.get_json()
        accountJsonData = {}
        for dataItem in requestData:
            if dataItem in requiredItems:
                requiredItems.remove(dataItem)
                if dataItem == 'username':
                    accountJsonData['emailAddress'] = requestData[dataItem]
                else:
                    accountJsonData[dataItem] = requestData[dataItem]
            
        if len(requiredItems) >=1:
            return {'status': 400, 'message': "Missing necessary information to create a new user", "missingField(s)": requiredItems}, 400
        session = newSession(accountJsonData['emailAddress'], accountJsonData['password'], accountJsonData['ipAddress'])
        return session, session['status']

class registerNewUser(Resource):
    
    def post(self):
        # Must be sent through function on the webpage (can't be directly submitted)
        # FUTURE: SEND THROUGH WEBSITE TO PREVENT PUT REQUESTS BEING SENT ACROSS SERVER ADDRESSES
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
        similarUsers = userAccount.query.filter_by(emailAddress = accountJsonData['emailAddress']).all()
        if similarUsers:
            return {'status': 403, 'message': "This username already exists: '%s'"%str(accountJsonData['emailAddress'])}, 403
        wasCreated, result = newLandlordAccount(accountJsonData)
        if wasCreated:
            return {'status': 201, 'message':'Success: User account has been created!','userID':str(result.userID)}, 201#,'redirectURL':'./home'}
        else:
            print ( dir(result))
            return {'status': 400, 'message':'Failed to save','error':str(result),'traceback':result.args,'redirectURL':'#'}

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

class getRentRoll(Resource):
    
    def get(self):
        if 'userSessionID' in request.cookies:
            isValid, sessionInfo = isSessionValid(request.cookies['userSessionID'])
            
            if isValid:
                #Now check if the person is authorized
                print(sessionInfo.sessionUser)
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

class adminPeople(Resource):

    def get(self):
        # 'GET' request comes directly from the webpage on a client's browser.
        # print(request.args)
        if 'sessionID' in request.args:
            ipAddress = request.remote_addr
            # print (ipAddress)
            # ipAddress = request.headers['ipAddress']
            isValid, sessionOrComment = isSessionValid(request.args['sessionID'], ipAddress=ipAddress)
            if isValid:
                sessn = sessionOrComment
                accntType = sessn.sessionUser.accountAuthority.typeName

                # print(sessn.sessionUser.accountAuthority.typeName)
                if accntType in ['landlord'] or 'admin' in accntType.lower():
                    #Now check if the person is authorized
                    cRP = sessn.sessionUser.companyRolePerson
                    if len(cRP) >0:
                        people = []
                        cmpny = cRP[0].associatedCompany
                        print ("company(s): ", cmpny)

                        # Find a list of landlord users for the company who can make people
                        companyUsers = companyRole.query.filter_by(companyID = cmpny.companyID).all()
                        for companyUser in companyUsers:
                            # get a list of the people created by the company's landlord users
                            peopleCreatedByUser = personDetail.query.filter_by(setPersonID = companyUser.userID).join(personDetail.associatedDetail).filter_by(propertyName='creator').all()
                            for personCreatedByUser in peopleCreatedByUser:
                                # print ("personCreatedByUser: ", personCreatedByUser)
                                people.append(personCreatedByUser.associatedPerson)
                        print ("PeopleList: ", people)
                        # Now get a list the people details
                        returnData = {'status': 200, 'people': []}
                        for person_i in people:

                            if "personID" in request.args and request.args["personID"] != person_i.personID:
                                pass
                            else:
                                # Now build return data
                                addedDetails = {}
                                # print("RElated Person: ", person_i)
                                # print("RElated PersonDetails: ", person_i.relatedPersonDetails)
                                for additionalDetail in person_i.relatedPersonDetails:
                                    if additionalDetail.associatedDetail.propertyName != 'creator':
                                        addedDetails[additionalDetail.associatedDetail.propertyName] = additionalDetail.propertyValue
                                data = {
                                    'personID':     person_i.personID,
                                    'firstName':    person_i.firstName,
                                    'lastName':     person_i.lastName,
                                    'emailAddress': person_i.personsAccount[0].emailAddress,
                                    'phoneNumber':  person_i.phoneNumber,
                                    'additionalDetails': addedDetails
                                }
                                
                                returnData['people'].append(data)
                        
                        return returnData, returnData['status']
                    else:
                        sessionOrComment = "Error with your account"
                else:
                    sessionOrComment = "Insufficient Authority to view this data"
            return {'status': 401, 'message': 'Unauthorized: %s'%(sessionOrComment)}, 401
        else:
            return {'status': 401, 'message': 'Unauthorized: You must be logged in to view this request'}, 401
        
    def post(self):
        # 'POST' request comes from the HomeEasy webserver (form post gets processed on the webserver and requests the API to save the data).
        if request.remote_addr != '20.228.226.251' and request.remote_addr != '127.0.0.1' and request.remote_addr != '24.101.69.174':
            return {'status': 403, 'message': 'Forbidden: You cannot view this request'}, 403

        peopleJsonData = {}
        requiredItems = ['sessionID', 'ipAddress', 'firstName', 'lastName', 'emailAddress', 'phoneNumber', 'additionalDetails']
        additionalRequirements = ['cellPhoneNumber', 'DOB','middleName','cars','comments']
        
        requestData = request.get_json()
        for dataItem in requestData:
            if dataItem in requiredItems:
                requiredItems.remove(dataItem)
                if dataItem == 'additionalDetails':
                    # FUTURE: Add some code to check for previous address and make new addressID
                    for addressComp in requestData[dataItem]:
                        if addressComp in additionalRequirements:
                            additionalRequirements.remove(addressComp)
                    if len(additionalRequirements)>=1:
                        return {'status': 400, 'message': "Missing additiona user detail(s)", "missingField(s)": additionalRequirements}, 400
                    peopleJsonData['additionalDetails'] = requestData[dataItem]
                elif dataItem in ['sessionID', 'ipAddress']:
                    pass
                else:
                    peopleJsonData[dataItem] = requestData[dataItem]
            
        if len(requiredItems) >=1:
            return {'status': 400, 'message': "Missing necessary information to create a new person", "missingField(s)": requiredItems}, 400
        # All the data pieces needed is verified to be here. now verify authority

        sessionID = requestData['sessionID']
        ipAddress = requestData['ipAddress']
        isValid, sessionOrComment = isSessionValid(sessionID=sessionID, ipAddress=ipAddress)
        if isValid:
            sessn = sessionOrComment
            accntType = sessn.sessionUser.accountAuthority.typeName
            companyAuthority = sessn.sessionUser.companyRolePerson[0].associatedAccountType.typeName

            if (accntType in ['landlord'] and companyAuthority!= 'companyRead') or 'admin' in accntType.lower():
                #Now we know the user is authorized to do this operation

                # 1. Check for duplicates? - Not MVP; FUTURE but the idea is below
                # similarUsers = userAccount.query.filter_by(emailAddress = accountJsonData['emailAddress']).all()
                # if similarUsers:
                #     return {'status': 403, 'message': "This username already exists: '%s'"%str(accountJsonData['emailAddress'])}, 403
                
                peopleJsonData['companyID'] = sessn.sessionUser.companyRolePerson[0].associatedCompany.companyID
                peopleJsonData['additionalDetails']['creator'] = ""
                peopleJsonData['createdBy']=sessn.sessionUser
                peopleJsonData['passHash'] = bcrypt.hashpw(peopleJsonData['additionalDetails']['DOB'].encode('utf-8'),bcrypt.gensalt())

                wasCreated, reslt = createTenant(peopleJsonData)
                if wasCreated:
                    return {'status': 201, 'message':'Success: User account has been created!','userID':str(reslt.userID)}, 201#,'redirectURL':'./home'}
                else:
                    print ( dir(reslt))
                    return {'status': 500, 'message':'Failed to create new person','error':str(reslt),'traceback':reslt.args,'redirectURL':'#'}, 500
            else:
                return {'status': 403, 'message': 'Forbidden: Insufficient authority to add a property'}, 403
        return {'status': 401, 'message': 'Unauthorized: %s'%(sessionOrComment)}, 401



class adminProperties(Resource):

    def get(self):
        # 'GET' request comes directly from the webpage on a client's browser.
        print(request.args)
        if 'sessionID' in request.args:
            ipAddress = request.remote_addr
            print (ipAddress)
            # ipAddress = request.headers['ipAddress']
            isValid, sessionOrComment = isSessionValid(request.args['sessionID'], ipAddress=ipAddress)
            if isValid:
                sessn = sessionOrComment
                accntType = sessn.sessionUser.accountAuthority.typeName

                print(sessn.sessionUser.accountAuthority.typeName)
                if accntType in ['landlord'] or 'admin' in accntType.lower():
                    #Now check if the person is authorized
                    cmpny = sessn.sessionUser.companyRolePerson[0].associatedCompany
                    print ("company(s): ", cmpny)
                    
                    if "propertyID" in request.args:
                        properties = property.query.filter_by(propertyID = request.args["propertyID"],companyID = cmpny.companyID).all()
                    else:
                        properties = property.query.filter_by(companyID = cmpny.companyID).all()
                    print ('properties: ', properties)

                    # Now build return data
                    returnData = {'status': 200, 'properties': []}
                    for prprty in properties:
                        
                        data = {
                            'propertyID':   prprty.propertyID,
                            'nickname':     prprty.nickname,
                            'address':      prprty.fullAddress.getHouseNStreet(),
                            'city':         prprty.fullAddress.city,
                            'state':        prprty.fullAddress.state,
                            'bedrms':       prprty.bedroomCount,
                            'bathrms':      prprty.bathroomCount,
                            'parkSpaces':   prprty.parkingCount,
                            'garageSpaces':     prprty.garageCount,
                            'stories':          prprty.storiesCount,
                            'homeType':         prprty.homeType,
                            'yearBuilt':        int(prprty.yearBuilt),
                            'purchasePrice':    prprty.purchasePrice,
                            'purchaseDate':     prprty.purchaseDate.strftime("%Y-%m-%d"),
                            'schoolDistrict':   prprty.schoolDistrict,
                        }
                        # for propertyk in data:
                        #     print (propertyk, type(data[propertyk]))
                        returnData['properties'].append(data)
                    return returnData, returnData['status']
                else:
                    sessionOrComment = "Insufficient Authority to view this data"
            return {'status': 401, 'message': 'Unauthorized: %s'%(sessionOrComment)}, 401
        else:
            return {'status': 401, 'message': 'Unauthorized: You must be logged in to view this request'}, 401

    def post(self):
        # print ("RemoteAddr: ",request.remote_addr)
        # 'POST' request comes from the HomeEasy webserver (form post gets processed and requests to be saved here).
        if request.remote_addr != '20.228.226.251' and request.remote_addr != '127.0.0.1' and request.remote_addr != '24.101.69.174':
            return {'status': 403, 'message': 'Forbidden: You cannot view this request'}, 403

        propertyJsonData = {}
        requiredItems = ['sessionID', 'ipAddress', 'address','bedroomCount','bathroomCount',
                         'parkingCount', 'garageCount', 'storiesCount', 'homeType', 'yearBuilt',
                         'purchasePrice', 'purchaseDate', 'schoolDistrict', 'nickname']
        # FUTURE: Add ownerID as required item and make the user select the owner from the list
        addressRequirements = ['houseNumber', 'streetName','city','state','zipCode']
        requestData = request.get_json()
        for dataItem in requestData:
            if dataItem in requiredItems:
                requiredItems.remove(dataItem)
                if dataItem == 'address':
                    if 'addressID' not in requestData['address']:
                        for addressComp in requestData[dataItem]:
                            if addressComp in addressRequirements:
                                addressRequirements.remove(addressComp)
                        if len(addressRequirements)>=1:
                            return {'status': 400, 'message': "Missing component(s) in the address", "missingField(s)": addressRequirements}, 400
                        else:
                            propertyJsonData['addressID'] = createNewAddress(**requestData['address'])
                    else:
                        propertyJsonData['addressID'] = requestData[dataItem]['addressID']
                    if not(propertyJsonData['addressID']):
                        return {'status': 400, 'message': "Failed to get the addressID"}, 400
                elif dataItem in ['sessionID', 'ipAddress']:
                    pass
                elif dataItem == 'purchaseDate':
                    propertyJsonData[dataItem] = datetime.strptime(requestData[dataItem], '%Y-%m-%d').date()
                else:
                    propertyJsonData[dataItem] = requestData[dataItem]
            
        if len(requiredItems) >=1:
            return {'status': 400, 'message': "Missing necessary information to create a new user", "missingField(s)": requiredItems}, 400
        
        # All the data pieces needed is verified to be here. now verify authority
        sessionID = requestData['sessionID']
        ipAddress = requestData['ipAddress']
        isValid, sessionOrComment = isSessionValid(sessionID=sessionID, ipAddress=ipAddress)
        if isValid:
            sessn = sessionOrComment
            accntType = sessn.sessionUser.accountAuthority.typeName
            companyAuthority = sessn.sessionUser.companyRolePerson[0].associatedAccountType.typeName

            if (accntType in ['landlord'] and companyAuthority!= 'companyRead') or 'admin' in accntType.lower():
                #Now the person is authorized to do this
                propertyJsonData['companyID'] = sessn.sessionUser.companyRolePerson[0].associatedCompany.companyID
                propertyJsonData['createUser'] = sessn.sessionUser.userID
                
                newPropertyID = createProperty(propertyJsonData)
                    
                if newPropertyID:
                    return {'status': 201, 'message': 'Success: Property created', 'propertyID': newPropertyID}, 201
                else:
                    return {'status': 500, 'message': 'issue creating property'}, 500
            else:
                return {'status': 403, 'message': 'Forbidden: Insufficient authority to add a property'}, 403
        return {'status': 401, 'message': 'Unauthorized: %s'%(sessionOrComment)}, 401

    


api.add_resource(getAccountType, '/getAuthority')
api.add_resource(registerNewUser, '/newLandlord')
api.add_resource(createSessionID, '/createSessionID')

# Rent Page
api.add_resource(rentRoll, '/rent')
api.add_resource(getRentRoll, '/admin/rent/roll')

# Leases Page
# api.add_resource(adminLeases, '/admin/leases')


# People
api.add_resource(adminPeople, '/admin/people')


# Properties Page
api.add_resource(adminProperties, '/admin/properties')


if __name__ == "__main__":
    app.run(debug=True)