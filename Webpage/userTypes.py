# from app import Users, BlogPost, Session
from DB_Object_Creator import db, userAccount, userSession, webSession, person
from datetime import date, datetime
from flask import request, make_response, render_template
import requests, json


from wtforms import Form, BooleanField, StringField, validators, DateField, IntegerField, DecimalField

def roundToHalf(value):
    value = value-0.5
    value = value.round(0)
    return value +0.5
# from DB_Object_Creator import 
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
        self = UserMaker().MakeUser()
        return self

    def getLeasesPage(self, sessionInfo):
        resp = make_response(render_template('unauthorized.html', headerData = self.headerContents, loggedOut = self.userSession==None))
        return resp
    
    def getPeoplePage(self, sessionInfo):
        resp = make_response(render_template('unauthorized.html', headerData = self.headerContents, loggedOut = self.userSession==None))
        return resp
    
    def getPropertiesPage(self, sessionInfo):
        resp = make_response(render_template('unauthorized.html', headerData = self.headerContents, loggedOut = self.userSession==None))
        return resp
    
    def saveProperty(self, requestInfo):
        
        return {'status': 401, 'message': 'You must be logged in', 'redirect': '/login'}, 401


class LoggedOutUser(User):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.User = None
        self.userSession = None
        self.userAccount = None
        self.headerContents = [{'name': "Home", 'link': "/", 'pageID': "index"}, {'name': "Login", 'link': "/login", 'pageID': "login"}]
    
    # getPeoplePage() -> parent definition
    # saveProperty() -> parent definition

    def createAnAccount(self, username, passHash, firstName, lastName, address, emailAddress, phoneNumber):
        pass
        #FUTURE: Make this function interact with the API?
        # newUser = userAccount(username = username, accountType=2, emailAddress = emailAddress, passHash = passHash)
        # try:
            
        #     db.session.add(newUser)
        #     db.session.commit()
        #     newPerson = person(firstName = firstName, lastName = lastName, phoneNumber = phoneNumber, DOB="unknown", createdBy=newUser)
        #     db.session.add(newPerson)
        #     db.session.commit()
        #     newUser.personID = newPerson.personID
        #     db.session.update(newPerson)
        #     db.session.commit()
        # except:
        #     return False, "There was an error saving the account to the DB"
        
class TenantUser(User):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.headerContents = [ {'name': "Rent",            'link': "/rent",                           'pageID': "rent"}, \
                                {'name': "Documents",       'link': "/solutions",                      'pageID': "solutions"}, \
                                # {'name': "Maintenance",     'link': "../product_reviews/index.html",    'pageID': "reviews"}, \
                                {'name': "Logout",          'link': "/logout",                     'pageID': "logout"}]

    # getPeoplePage() -> parent definition

    def saveProperty(self, requestInfo):
        requestData = requestInfo.json()
        
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
            "bathroomCount": round(float(requestData['bathroomCount'],0)*2)/2,
            "parkingCount": int(requestData['parkingCount']),
            "garageCount": int(requestData['garageCount']),
            "storiesCount": float(requestData['storiesCount']),
            "homeType": requestData['homeType'],
            "purchasePrice": int(requestData['purchasePrice']),
            "purchaseDate": datetime.strptime(requestData['purchaseDate'],'%m/%d/%Y'),
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
            return {'status': 500, 'message': 'Issue saving the property'}, 500

    # viewBlogPost() -> parent definition
    # viewComments() -> Parent definition
    # writeComment() -> Parent definition
    # deleteComment() -> Parent definition
    # likeComment() -> parent definition
    # likePost() -> Parent definition

    # def becomeProperty_Manager_User(self, membershipLevel, paymentDate, expirationDate, TransactionID):
        
    #     newMembership = Memberships(username = self.User.Username, accountType = membershipLevel, paymentDate = paymentDate, expirationDate = expirationDate, TransactionID = TransactionID)
    #     try:
    #         db.session.add(newMembership)
    #         db.session.commit()
    #         mm = UserMaker()
    #         self = mm.MakeUser(user = self.User, userSession = self.userSession, user_account = newMembership)
    #         return True, self
    #     except:
    #         return False, "There was an error saving the account to the DB"

        
        
class Property_Manager_User(User):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.headerContents = [ {'name': "Rent Roll",       'link': "/rent",            'pageID': "rent"}, \
                                {'name': "Leases",          'link': "/leases",          'pageID': "leases"}, \
                                {'name': "People",          'link': "/people",          'pageID': "people"}, \
                                {'name': "Properties",      'link': "/properties",      'pageID': "properties"}, \
                                # {'name': "Maintenance",     'link': "/maintenance",     'pageID': "maintenance"}, \
                                {'name': "Logout",          'link': "/logout",          'pageID': "logout"}]
        
    def getLeasesPage(self, sessionInfo):
        form = newPropertyForm(request.form)
        resp = make_response(render_template('admin/leases.html', headerData = self.headerContents, form=form))
        return resp
    
    def getPeoplePage(self, sessionInfo):
        form = newPropertyForm(request.form)
        resp = make_response(render_template('admin/people.html', headerData = self.headerContents, form=form))
        return resp
    
    def getPropertiesPage(self, sessionInfo):
        form = newPropertyForm(request.form)
        resp = make_response(render_template('admin/properties.html', headerData = self.headerContents, form=form))
        return resp

    def saveProperty(self, requestInfo):
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
            return {'status': 500, 'message': 'Issue saving the property'}, 500

    # def viewBlogPost(self, id):
    #     return BlogPost.query.filter_by(ReviewID = id).first_or_404()

    def cancelMembership(self):
        try:
            self.userAccount.accountType -= 1
            db.session.commit()
            self = UserMaker().MakeUser(user = self.User, userSession = self.userSession, user_account = self.userAccount)
            return True, self
        except:
            return False, "There was an error saving the account to the DB"


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
        

    def getPeoplePage(self, sessionInfo):

        resp = make_response(render_template('admin/people.html', headerData = self.headerContents, loggedOut = self.userSession==None))
        return resp

    def saveProperty(self, requestInfo):
        requestData = requestInfo.json()
        
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
            "bathroomCount": round(float(requestData['bathroomCount'],0)*2)/2,
            "parkingCount": int(requestData['parkingCount']),
            "garageCount": int(requestData['garageCount']),
            "storiesCount": float(requestData['storiesCount']),
            "homeType": requestData['homeType'],
            "purchasePrice": int(requestData['purchasePrice']),
            "purchaseDate": datetime.strptime(requestData['purchaseDate'],'%m/%d/%Y'),
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
            return {'status': 500, 'message': 'Issue saving the property'}, 500
        
        
    # def viewBlogPost(self, id):
    #     return BlogPost.query.filter_by(ReviewID = id).first_or_404()

    # def approveComment(self, comment_id):
    #     try:
    #         comment = Comments.query.filter_by(CommentID = comment_id).first_or_404()
    #         comment.approvedBy = self.EmployeeInfo.EmployeeID
    #         comment.approveddate = datetime.utcnow()
    #         db.session.commit()
    #         return True, "The comment has been approved"
    #     except:
            
    #         return False, "There was some problem approving the comment"
    
    # def rejectComment(self, comment_id):
    #     try:
    #         comment = Comments.query.filter_by(CommentID = comment_id).first_or_404()
    #         comment.approvedBy = self.EmployeeInfo.EmployeeID
    #         db.session.commit()
    #         return True, "The comment has been removed"
    #     except:
    #         return False, "There was an error taking the comment down"

    # def newPost(self, Product, title, review_text, is_free):
    #     try:
    #         new_post = BlogPost(ProductID = Product.ProductID, ReviewerID = self.EmployeeInfo.EmployeeID, Title = title, ReviewText = review_text, Revision = 0, LastEditDate = datetime.utcnow(), isFree = is_free)
    #         db.session.add(new_post)
    #         db.session.commit()
    #         return True, "The post has been saved"
    #     except:
    #         return False, "There was an error saving the post"

    # def savePost(self, Product, title, review_text, is_free, revision, revision_reason):
    #     try:
    #         new_post = BlogPost(ProductID = Product.ProductID, ReviewerID = self.EmployeeInfo.EmployeeID, Title = title, ReviewText = review_text, OriginalPostDate = datetime.utcnow(), Revision = revision, LastEditDate = datetime.utcnow(), isFree = is_free, RevisionReason = revision_reason)
    #         db.session.add(new_post)
    #         db.session.commit()
    #         return True, "The post has been saved"
    #     except:
    #         return False, "There was an error saving the post"

    # def publishPost(self, blog_post, publish_datetime, approval_editor = None):
    #     try:
    #         blog_post.OriginalPostDate = publish_datetime
    #         #blog_post.ReviewingEditor = approval_editor
    #         db.session.commit()
    #         return True, "The post has been scheduled for publish" # pending editor approval
    #     except:
    #         return False, "There was an error scheduling the post for publishing"