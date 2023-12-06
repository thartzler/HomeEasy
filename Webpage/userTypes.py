# from app import Users, BlogPost, Session
from DB_Object_Creator import db, userAccount, userSession, webSession, person
from datetime import date, datetime



class UserMaker:

    def MakeUser(self, sessionID = None):
        '''
        If the sessionID is valid, find out the type of user based on the username
        Then, create the corresponding type of user by feeding in the DB userAccount object
        '''
        if sessionID is not None:
            # determine what member type this sessionID is and make the corresponding type
            (result, info) = webSession().isSessionValid(sessionID)
            if result:
                # This means info = a valid webSession
                user = info.user

                try:
                    user_account = userAccount.query.filter_by(username = info.username).first()
                    if user_account.accountType == 1:
                        # Admin user type. It's a global access account and is only for me
                        return AdminUser(user, info, user_account)
                    elif user_account.accountType == 2:
                        # Property manager's user type. It is a paid account and can create properties, create tenant users, and enter payments
                        return Property_Manager_User(user, info, user_account)
                    elif user_account.accountType == 3:
                        # Tenant's user type. It gets created by the property manager and can be used to view the payment status, etc.
                        return TenantUser(user, info, user_account)
                except:
                    user_account = userAccount(username = info.username, emailAddress = "", accountType = 2, createDate = datetime.utcnow())
                    db.session.add(user_account)
                    db.session.commit()
                    return TenantUser(user, info, user_account)
        
        return LoggedOutUser()



class User:
    def __init__(self, user = None, this_session = None, user_account = None,) -> None:
        self.User = user
        self.userSession = this_session
        self.userAccount = user_account
        self.message = ""
        self.headerContents = [{'name': "Logout", 'link': "/logout", 'pageID': "logout"}]
    
    # def viewBlogPost(self, id) -> BlogPost:
    #     # Enter some default method to view a blog post (Facade?)
    #     pass
    
    # def viewComments(self, PostID) -> list:
    #     # returns a list of comment items
    #     returnList = []
    #     comments = Comments.query.filter_by(ReviewID = PostID).limit(50).all()
    #     for comment in comments:
    #         returnList.append(comment)
    #     return(returnList)

    # def writeComment(self, postID, title, comment_text, CommentIDReplyingTo = None):
    #     # Enter some default method to write a comment
    #     newComment = Comments(ReviewID = postID, CommentDate = datetime.utcnow(), Title = title, CommentText = comment_text, Username = self.User.Username, ReplyingTo = CommentIDReplyingTo)
    #     try:
    #         db.session.add(newComment)
    #         db.session.commit()
    #         return True, "comment saved successfully"
    #     except:
    #         return False, "There was an error saving the new comment"

    # def deleteComment(self, commentID):
    #     # Enter some default delete method in here
    #     try:
    #         comment = Comments.query.filter_by(CommentID = commentID).first_or_404()
    #         db.session.delete(comment)
    #         db.session.commit()
    #         return True, "the comment was deleted successfully"
    #     except:
    #         return False, "There was a problem trying to delete the comment"
    
    # def likeComment(self, commentID):
    #     # Enter some default comment liking command
    #     comment = Comments.query.filter_by(CommentID = commentID).first_or_404()
    #     print ("{} liked {}'s comment titled {}"%(self.User.Username, comment.Username, comment.Title))
    #     return
    # 
    # def likePost(self, postID):
    #     # enter some default commands for liking a comment
    #     post = BlogPost.query.filter_by(ReviewID = postID).first_or_404()
    #     print ("{} liked the review titled {}!"%(self.User.Username, post.Title))
    #     return

    def Login(self, username, password):
        #the user would login
        ws = webSession()
        if ws.isUsernameValid(username):
            if ws.credentialsValid(username, password):
                newSession = ws.newSession(username, password)[0]
                self = UserMaker().MakeUser(newSession.sessionID)
                return self
            else:
                self.message = "Incorrect Password"
                return self
        else:
            self.message = "Invalid Username"
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

    def Logout(self):
        # Already logged out, so nothing needs done.

        pass

    def createAnAccount(self, username, passHash, firstName, lastName, address, emailAddress, phoneNumber):
        newUser = userAccount(username = username, accountType=2, emailAddress = emailAddress, passHash = passHash)
        try:
            
            db.session.add(newUser)
            db.session.commit()
            newPerson = person(firstName = firstName, lastName = lastName, phoneNumber = phoneNumber, DOB="unknown", createdBy=newUser)
            db.session.add(newPerson)
            db.session.commit()
            newUser.personID = newPerson.personID
            db.session.update(newPerson)
            db.session.commit()
        except:
            return False, "There was an error saving the account to the DB"
        
class TenantUser(User):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.headerContents = [ {'name': "Rent",            'link': "/rent/",                           'pageID': "rent"}, \
                                {'name': "Documents",       'link': "/solutions/",                      'pageID': "solutions"}, \
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
        self.headerContents = [ {'name': "Rent Roll",       'link': "/rent_roll",       'pageID': "rent"}, \
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
        self.userAccount = userAccount.query.filter_by(Username = self.User.Username).first_or_404()
        self.headerContents = [ {'name': "Rent Roll",       'link': "/rent_roll/",                      'pageID': "rent"}, \
                                {'name': "Properties",      'link': "/solutions/",                      'pageID': "solutions"}, \
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