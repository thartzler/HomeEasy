from datetime import date, datetime
from flask import request, make_response, render_template
import requests, json


from wtforms import Form, SelectField, StringField, validators, DateField, IntegerField, DecimalField, PasswordField

def roundToHalf(value):
    value = value-0.5
    value = value.round(0)
    return value +0.5

class newUserForm(Form):
    firstName= StringField('First Name*', [validators.DataRequired(), validators.Regexp('[A-Za-z]+'),validators.Length(max=50)])
    lastName= StringField('Last Name*', [validators.DataRequired(), validators.Regexp('[A-Za-z]+'),validators.Length(max=50)])
    companyName= StringField('Company Name*', [validators.DataRequired(), validators.Regexp('[A-Za-z]+'),validators.Length(max=50)])
    emailAddress= StringField('Email Address*', [validators.DataRequired(),validators.Length(max=50)])
    houseNumber= StringField('House No.*', [validators.DataRequired()])
    streetName= StringField('Street*', [validators.DataRequired(),validators.Length(max=30)])
    apptNo= StringField('Appt No.',[validators.Length(max=6)])
    city= StringField('City*', [validators.DataRequired(),validators.Length(max=30)])
    state= StringField('State*', [validators.DataRequired(), validators.Regexp('[A-Z]{2}'), validators.Length(min=2, max=2)])
    zipCode= StringField('Zip Code*', [validators.DataRequired(), validators.Regexp('[0-9]+'), validators.Length(min=5, max=5)])
    companyPhone= StringField('Company Phone*', [validators.DataRequired(), validators.Regexp('[0-9]{3}-[0-9]{3}-[0-9]{4}'), validators.Length(min=10, max=12)])
    phoneNumber= StringField('Personal Phone Number*', [validators.DataRequired(), validators.Regexp('[0-9]+'), validators.Length(min=10, max=10)])
    password= PasswordField('Password*', [
            validators.DataRequired(),\
            validators.EqualTo('password_confirm', message='Passwords must already match!')\
        ])
    password_confirm= PasswordField('Verify Password*', [validators.DataRequired()])




class newLeaseForm(Form):

    # def __init__(self, sessionID:str, formdata: _MultiDictLike | None = None, obj: object | None = None, prefix: str = "", data: Mapping[str, Any] | None = None, meta: Mapping[str, Any] | None = None, *, extra_filters: Mapping[str, Sequence[Any]] | None = None, **kwargs: object) -> None:
    #     super().__init__(formdata, obj, prefix, data, meta, extra_filters=extra_filters, **kwargs)
    
    # # 1: Get the comboBox Option data from the API
    # print (args['sessionID'])

    # 2: setup the comboBoxes
    property= SelectField('Property*',[validators.DataRequired(), validators.Length(max=50)])
    tenant= SelectField('Tenant(s) on lease*', [validators.DataRequired()])
    
    availableDate= DateField('Avail. Date*', [validators.DataRequired()])
    moveInDate= DateField('Move-in Date*', [validators.DataRequired()])
    terminateDate= DateField('Termination Date')
    
    leaseStatus= StringField('Lease Status*', [validators.DataRequired(),validators.Length(max=50)])
    
    leasePeriod= SelectField('Lease Term*', [validators.DataRequired()])
    leaseSuccessionPeriod= SelectField('New Term After Initial Lease Term*', [validators.DataRequired()])
    # monthlyRent= IntegerField('Monthly Rent*', [validators.DataRequired(), validators.Regexp('[0-9]+'), validators.NumberRange(min=0)])
    # securityDeposit= IntegerField('Security Deposit*', [validators.DataRequired(), validators.Regexp('[0-9]+'), validators.NumberRange(min=0)])

    feeName= SelectField('fee Name*')
    feeAmount = IntegerField('fee Amount*', [validators.Regexp('[0-9.]+'), validators.NumberRange(min=0)])
    feeOccurrence = SelectField('fee Occurrence*')
    startAfterLength = IntegerField('Fee Begins After Amount*', [validators.Regexp('[0-9]+'), validators.NumberRange(min=0)])
    startAfterPeriod = SelectField('Fee Begins After Period*')
    
class newPropertyForm(Form):
    nickname= StringField('Nickname*', [validators.DataRequired(), validators.Length(max=50)])
    houseNumber= IntegerField('House No.*', [validators.DataRequired()])
    streetName= StringField('Street*', [validators.DataRequired(),validators.Length(max=30)])
    apptNo= StringField('Appt No.', [validators.Length(max=6)])
    city= StringField('City*', [validators.DataRequired(),validators.Length(max=30)])
    state= StringField('State*', [validators.DataRequired(), validators.Regexp('[A-Z]{2}'), validators.Length(min=2, max=2)])
    zipCode= IntegerField('Zip Code*', [validators.DataRequired(), validators.Regexp('[0-9]+'), validators.Length(min=5, max=5)])
    
    bedroomCount= IntegerField('Bedrooms*', [validators.DataRequired(), validators.Regexp('[0-9]+'), validators.NumberRange(min=0)])
    bathroomCount= DecimalField('Bathrooms*', [validators.DataRequired(), validators.Regexp('[0-9.]+'), validators.NumberRange(min=0)], places=1, rounding=roundToHalf)
    parkingCount= IntegerField('Parking Spots*', [validators.DataRequired(), validators.Regexp('[0-9]+'), validators.NumberRange(min=0)])
    garageCount= IntegerField('Garage Spaces*', [validators.DataRequired(), validators.Regexp('[0-9]+'), validators.NumberRange(min=0)])
    homeType = StringField('Home Type*', [validators.DataRequired(), validators.Length(max=50)])
    storiesCount= StringField('Stories*', [validators.DataRequired(), validators.Regexp('[0-9.]+')])
    yearBuilt = IntegerField('Year Built*', [validators.DataRequired(), validators.Regexp('[0-9]+'), validators.Length(max=4)])
    purchaseDate = DateField('Purchase Date*', [validators.DataRequired()])
    purchasePrice = IntegerField('Purchase Price*', [validators.DataRequired(), validators.Regexp('[0-9]+')])
    schoolDistrict = StringField('School District*', [validators.DataRequired(), validators.Length(max=50)])
    
class newTenantUserForm(Form):
    firstName= StringField('First Name*', [validators.DataRequired(), validators.Regexp('[A-Za-z]+'),validators.Length(max=50)])
    middleName= StringField('Middle Name*', [validators.DataRequired(), validators.Regexp('[A-Za-z]+'),validators.Length(max=50)])
    lastName= StringField('Last Name*', [validators.DataRequired(), validators.Regexp('[A-Za-z]+'),validators.Length(max=50)])
    
    emailAddress= StringField('Email Address*', [validators.DataRequired(),validators.Length(max=50)])
    
    phoneNumber= StringField('Daytime Phone Number*', [validators.DataRequired(), validators.Regexp('[0-9]+'), validators.Length(min=10, max=10)])
    cellPhoneNumber= StringField('Cell Phone Number*', [validators.DataRequired(), validators.Regexp('[0-9]+'), validators.Length(min=10, max=10)])
    
    DOB = DateField('Birth Date*', [validators.DataRequired()])
    cars= StringField('Vehicle(s)*', [validators.DataRequired(),validators.Length(max=50)])
    
    comments= StringField('Comments*',[validators.DataRequired(),validators.Length(max=50)])



def getUser(sessionID: str = None, ipAddress: str = None):
    userType = None
    if sessionID and ipAddress:
        url = 'http://api.hartzlerhome.solutions/getAuthority'
        payload = json.dumps({"sessionID": sessionID, "ipAddress": ipAddress})
        headers = {
        'Content-Type': 'application/json'
        }
        responseData = requests.request("GET",url, headers=headers, data=payload).json()
        print ("jsonResponse from getAuthority: ", responseData)
        userType =  responseData['userType']
        print ("UserType: ", userType)
    return UserMaker().MakeUser(userType = userType, sessionID = sessionID)

def _newLandlord(requestInfo):
    requestData = requestInfo.get_json()

    url = 'http://api.hartzlerhome.solutions/newLandlord'
    jsonData = { 'additionalDetails':{ } , 'address': { } }
    addressInfo = ['houseNumber', 'streetName','city','state','zipCode','apptNo']
    details = ['address','firstName', 'lastName', 'phoneNumber', 'emailAddress', 'password','companyName', 'companyPhone']
    junk = ['password_confirm']
    
    for key,values in requestData.items():
        if key in addressInfo:
            jsonData['address'][key] = values
        elif key in details:
            jsonData[key] = values
        elif key not in junk:
            jsonData['additionalDetails'][key] = values
    payload = json.dumps(jsonData)

    headers = {'Content-Type': 'application/json'}
    responseData = requests.request("POST", url, headers=headers, data=payload).json()
    # {'status': 200, 'message': "New session has been made", 'sessionID': session2Add.sessionID}
    if responseData:
        return responseData
    else:
        return {'status': 500, 'message': 'Issue creating an account'}
    
def _newLease(requestInfo):
    requestData = requestInfo.get_json()
    
    url = 'http://api.hartzlerhome.solutions/admin/leases'
    
    fees = []
    for fee in requestData['fees']:
        newFee = {
            "feeID": fee['feeName'],
            "feeAmount": fee['feeAmount'],
            "occurrence": fee['feeOccurrence'],
            "startAfterLength": fee['startAfterLength'],
            "startAfterPeriod": fee["startAfterPeriod"]
        }
        fees.append(newFee)
    payload = json.dumps({
        'propertyID': int(requestData['property']),
        'people': [{
            'personID': int(requestData['tenant']),
            'role': 'tenant'
        }],
        'leaseStatus': requestData['leaseStatus'],
        'availableDate': requestData['availableDate'],
        'moveInDate': requestData['moveInDate'],
        'terminationDate': requestData['terminateDate'],
        'leasePeriod': int(requestData['leasePeriod']),
        'leaseSuccessionPeriod': int(requestData['leaseSuccessionPeriod']),
        # 'monthlyRent': requestData['monthlyRent'],
        # 'securityDeposit': requestData['securityDeposit'],
        'contractDocID': '',
        'fees': fees,
        "sessionID": requestInfo.cookies['sessionID'],
        "ipAddress": requestInfo.remote_addr
    })
    
    headers = {'Content-Type': 'application/json'}
    responseData = requests.request("POST", url, headers=headers, data=payload).json()
    if responseData:
        return responseData
    else:
        return {'status': 500, 'message': 'Issue saving the lease'}


def _saveProperty(requestInfo):
    requestData = requestInfo.get_json()
    
    url = 'http://api.hartzlerhome.solutions/admin/properties'
    payload = json.dumps({
        "address": {
            "houseNumber": int(requestData['houseNumber']),
            "streetName": requestData['streetName'],
            "city": requestData['city'],
            "state": requestData['state'],
            "zipCode": int(requestData['zipCode'])
        },
        "bedroomCount": int(requestData['bedroomCount']),
        "bathroomCount": round(float(requestData['bathroomCount'])*2,0)/2,
        "parkingCount": int(requestData['parkingCount']),
        "garageCount": int(requestData['garageCount']),
        "homeType": requestData['homeType'],
        "storiesCount": float(requestData['storiesCount']),
        "yearBuilt": int(requestData['yearBuilt']),
        "purchasePrice": int(requestData['purchasePrice']),
        "purchaseDate": requestData['purchaseDate'],
        "schoolDistrict": requestData['schoolDistrict'],
        "nickname": requestData['nickname'],
        "sessionID": requestInfo.cookies['sessionID'],
        "ipAddress": requestInfo.remote_addr
    })
    
    headers = {'Content-Type': 'application/json'}
    responseData = requests.request("POST", url, headers=headers, data=payload).json()
    # {'status': 200, 'message': "New session has been made", 'sessionID': session2Add.sessionID}
    if responseData:
        return responseData
    else:
        return {'status': 500, 'message': 'Issue saving the property'}

def _savePerson(requestInfo):
    
    requestData = requestInfo.get_json()
    print ('requestData: ',requestData)
    coreItems = ['firstName', 'lastName', 'emailAddress', 'phoneNumber']
    addlDets = {}
    for key in requestData:
        if key not in coreItems:
            addlDets[key] = requestData[key]
    url = 'http://api.hartzlerhome.solutions/admin/people'
    payload = json.dumps({
        "firstName": requestData['firstName'],
        "lastName": requestData['lastName'],
        "emailAddress": requestData['emailAddress'],
        "phoneNumber": requestData['phoneNumber'],
        "additionalDetails": addlDets,
        "sessionID": requestInfo.cookies['sessionID'],
        "ipAddress": requestInfo.remote_addr
    })
    headers = {'Content-Type': 'application/json'}
    responseData = requests.request("POST", url, headers=headers, data=payload).json()
    print ("Response: ", responseData)
    if responseData:
        return responseData
    else:
        return {'status': 500, 'message': 'There was an issue and the person was not saved'}
    


class UserMaker:

    def MakeUser(self, userType = None, sessionID = None):
        '''
        If the userType is not none, then it's already been validated with the db and the user is currently logged in
        Then, create the corresponding type of user is created
        '''
        print ("Making User of type : ", userType)
        if userType:
            # determine what member type this sessionID is and make the corresponding type
            if userType == 'level1Admin':
                # Admin user type. It's a global access account and is only for me
                return AdminUser(sessionID = sessionID)
            elif userType == 'landlord':
                # Property manager's user type. It is a paid account and can create properties, create tenant users, and enter payments
                return Property_Manager_User(sessionID = sessionID)
            elif userType == 'tenant':
                # Tenant's user type. It gets created by the property manager and can be used to view the payment status, etc.
                return TenantUser(sessionID = sessionID)
        
        return LoggedOutUser()



class User:
    def __init__(self, user = None, sessionID = None, user_account = None,) -> None:
        self.User = user
        self.userSession = sessionID
        self.userAccount = user_account
        self.message = ""
        self.headerContents = [{'name': "Logout", 'link': "/logout", 'pageID': "logout"}]
    
    def Login(self, username, password, ipAddress):
        #the user would login
        
        url = 'http://api.hartzlerhome.solutions/createSessionID'
        payload = json.dumps({"username": username, "password": password, "ipAddress": ipAddress})
        headers = {'Content-Type': 'application/json'}
        responseData = requests.request("POST",url, headers=headers, data=payload).json()
        # {'status': 200, 'message': "New session has been made", 'sessionID': session2Add.sessionID}
        if responseData:
            self.message = responseData['message']
        else:
            self.message = 'Error getting data'
        if responseData['status'] == 200:
            # print('authentication is valid')
            # write a return the data
            userType =  responseData['userType']
            sessionID = responseData['sessionID']
            self = UserMaker().MakeUser(userType=userType, sessionID= sessionID)
            print ("This is me:", self)
        
        
        return self
    
    def Logout(self):
        # Already logged out, so nothing needs done.
        print ("I'm HERE")
        newUser = UserMaker().MakeUser()
        resp = make_response(render_template('logout.html', headerData = newUser.headerContents))
        resp.set_cookie('sessionID','', expires = 0)
        return resp

    def newLandlord(self, requestInfo):
        return _newLandlord(requestInfo)

    def getHomePage(self, sessionInfo):
        return render_template('')
    
    def getNewLandlordPage(self, sessionInfo):
        form = newUserForm(request.form)
        return render_template('newUser.html', headerData = self.headerContents, form=form)

    def getRentPage(self, sessionInfo):
        resp = make_response(render_template('unauthorized.html', headerData = self.headerContents, loggedOut = self.userSession==None))
        return resp
    
    def getLeasesPage(self, sessionInfo):
        resp = make_response(render_template('unauthorized.html', headerData = self.headerContents, loggedOut = self.userSession==None))
        return resp
    
    def getPeoplePage(self, sessionInfo):
        resp = make_response(render_template('unauthorized.html', headerData = self.headerContents, loggedOut = self.userSession==None))
        return resp
    
    def getPropertiesPage(self, sessionInfo):
        resp = make_response(render_template('unauthorized.html', headerData = self.headerContents, loggedOut = self.userSession==None))
        return resp
    
    def saveLease(self, requestInfo):
        return {'status': 401, 'message': 'You must be logged in', 'redirect': '/login'}
    
    def savePerson(self, requestInfo):
        return {'status': 401, 'message': 'You must be logged in', 'redirect': '/login'}
    
    def saveProperty(self, requestInfo):
        return {'status': 401, 'message': 'You must be logged in', 'redirect': '/login'}


class LoggedOutUser(User):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.User = None
        self.userSession = None
        self.userAccount = None
        self.headerContents = [{'name': "Home", 'link': "/", 'pageID': "index"}, {'name': "Login", 'link': "/login", 'pageID': "login"}]
    
    # getRentPage()    -> parent definition
    # getLeasePage()   -> parent definition
    # getPeoplePage()   -> parent definition
    # saveLease()       -> parent definition
    # savePerson()      -> parent definition
    # saveProperty()    -> parent definition

    def createAnAccount(self, username, passHash, firstName, lastName, address, emailAddress, phoneNumber):
        pass
        #FUTURE: Make this function interact with the API? issue #44
        
class TenantUser(User):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.headerContents = [ {'name': "Rent",            'link': "/rent",                       'pageID': "rent"}, \
                                {'name': "Documents",       'link': "/leases",                     'pageID': "solutions"}, \
                                # {'name': "Maintenance",     'link': "../product_reviews/index.html",    'pageID': "reviews"}, \
                                {'name': "Logout",          'link': "/logout",                     'pageID': "logout"}]

    def getRentPage(self, sessionInfo):
        resp = make_response(render_template('underConstruction.html', headerData = self.headerContents))
        return resp

    def getLeasesPage(self, sessionInfo):
        resp = make_response(render_template('underConstruction.html', headerData = self.headerContents))
        return resp
    
    # getPeoplePage() -> parent definition

    # def saveLease(self, requestInfo):
    #     return _newLease(requestInfo= requestInfo)
    
    # def savePerson(self, requestInfo):
    #     return _savePerson(requestInfo= requestInfo)
    
    # def saveProperty(self, requestInfo):
    #     return _saveProperty(requestInfo= requestInfo)

        
class Property_Manager_User(User):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.headerContents = [ {'name': "Rent Roll",       'link': "/rent",            'pageID': "rent"}, \
                                {'name': "Leases",          'link': "/leases",          'pageID': "leases"}, \
                                {'name': "People",          'link': "/people",          'pageID': "people"}, \
                                {'name': "Properties",      'link': "/properties",      'pageID': "properties"}, \
                                # {'name': "Maintenance",     'link': "/maintenance",     'pageID': "maintenance"}, \
                                {'name': "Logout",          'link': "/logout",          'pageID': "logout"}]
    def getRentPage(self, sessionInfo):
        monthlist = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']
        rentRollList = []
        return render_template('admin/rent_roll.html', headerData = self.headerContents, rentRollList = rentRollList, monthlist=monthlist)

    def getLeasesPage(self, sessionInfo):
        form = newLeaseForm(request.form, sessionID = self.userSession)
        resp = make_response(render_template('admin/leases.html', headerData = self.headerContents, form=form))
        return resp
    
    def getPeoplePage(self, sessionInfo):
        form = newTenantUserForm(request.form)
        resp = make_response(render_template('admin/people.html', headerData = self.headerContents, form=form))
        return resp
    
    def getPropertiesPage(self, sessionInfo):
        form = newPropertyForm(request.form)
        resp = make_response(render_template('admin/properties.html', headerData = self.headerContents, form=form))
        return resp

    def saveLease(self, requestInfo):
        print ("newLease Req: ", requestInfo)
        return _newLease(requestInfo)
    
    def savePerson(self, requestInfo):
        return _savePerson(requestInfo= requestInfo)
    
    def saveProperty(self, requestInfo):
        print ("saveProperty Req: ", requestInfo)
        return _saveProperty(requestInfo)


class AdminUser(User):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        # self.userAccount = userAccount.query.filter_by(Username = self.User.Username).first_or_404()
        self.headerContents = [ {'name': "Rent Roll",       'link': "/rent",            'pageID': "rent"}, \
                                {'name': "Leases",          'link': "/leases",          'pageID': "leases"}, \
                                {'name': "People",          'link': "/people",          'pageID': "people"}, \
                                {'name': "Properties",      'link': "/properties",      'pageID': "properties"}, \
                                # {'name': "Maintenance",     'link': "/maintenance",     'pageID': "maintenance"}, \
                                {'name': "Logout",          'link': "/logout",          'pageID': "logout"}]
        
    def getLeasesPage(self, sessionInfo):
        form = newLeaseForm(request.form, sessionID = self.userSession)
        resp = make_response(render_template('admin/leases.html', headerData = self.headerContents, form=form))
        return resp
    
    def getPeoplePage(self, sessionInfo):
        form = newTenantUserForm(request.form)
        resp = make_response(render_template('admin/people.html', headerData = self.headerContents, form=form))
        return resp

    def saveLease(self, requestInfo):
        print ("newLease Req: ", requestInfo)
        return _newLease(requestInfo)
    
    def savePerson(self, requestInfo):
        return _savePerson(requestInfo= requestInfo)
    
    def saveProperty(self, requestInfo):
        return _saveProperty(requestInfo= requestInfo)