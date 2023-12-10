# from app import Users, BlogPost, Session
from DB_Object_Creator import db, userAccount, userSession, webSession, person
from datetime import date, datetime
from flask import request
import requests, json


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

    


class LoggedOutUser(User):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.User = None
        self.userSession = None
        self.userAccount = None
        self.headerContents = [{'name': "Home", 'link': "/", 'pageID': "index"}, {'name': "Login", 'link': "/login", 'pageID': "login"}]
    
    # def viewBlogPost, viewcomments,

    # def writeComment(self, postID, replyToCommentID):
    #     #This is not feasible. Must be logged in
    #     return False, "Please Login first"

    # def deleteComment(self, commentID):
    #     #This is not feasible. Must be logged in
    #     return False,  "Please Login first"

    # def likeComment(self, commentID):
    #     #This isn't feasible unless logged in
    #     return False, "Please Login first"

    # def likePost(self, postID):
    #     #This isn't feasible unless logged in
    #     return False, "Please Login first"

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
                                {'name': "Properties",      'link': "/solutions",       'pageID': "solutions"}, \
                                {'name': "People",          'link': "/people",          'pageID': "people"}, \
                                # {'name': "Maintenance",     'link': "/maintenance",     'pageID': "maintenance"}, \
                                {'name': "Logout",          'link': "/logout",          'pageID': "logout"}]
        
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
        self.headerContents = [ {'name': "Rent Roll",       'link': "/rent",                            'pageID': "rent"}, \
                                {'name': "Properties",      'link': "/solutions",                       'pageID': "solutions"}, \
                                {'name': "People",          'link': "../product_reviews/index.html",    'pageID': "people"}, \
                                # {'name': "Maintenance",     'link': "../product_reviews/index.html",    'pageID': "maintenance"}, \
                                {'name': "Logout",          'link': "/logout.html",                     'pageID': "logout"}]
        
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