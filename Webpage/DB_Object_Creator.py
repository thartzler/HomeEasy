from flask_sqlalchemy import SQLAlchemy


# from sqlalchemy import create_engine, Column, Integer, String, Date, MetaData, ForeignKey, DateTime
# from sqlalchemy.orm import sessionmaker, declarative_base, relationship
# # from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.ext.automap import automap_base
# from sqlalchemy.orm import Session
# from sqlalchemy.sql.expression import false, null

# from sqlalchemy.sql.schema import PrimaryKeyConstraint
from datetime import datetime, timedelta
import secrets




db = SQLAlchemy()


#Define classes for each of the tables along with relationships
# """
# Section for all Application common tables
# """

class accountType(db.Model):
    # This is the database relationship object for records in the Application_Account_Types table
    # Done
    __tablename__ = "Application_Account_Types"
    accountTypeID = db.Column(db.Integer, primary_key=True, nullable = False, unique = True)
    cost = db.Column(db.String)
    accountTypeName = db.Column(db.String)
    typeDescription = db.Column(db.String)

    accountType = db.relationship("userAccount", back_populates='accountAuthority')#

    def __init__(self) -> None:
        return "<accountType(Account Type Name = '%r')>" % self.accountTypeName

class feeType(db.Model):
    # This is the database relationship object for records in the Application_Fee_Types table
    # Done
    __tablename__ = "Application_Fee_Types"
    feeID = db.Column(db.Integer, primary_key=True, nullable = False, unique = True)
    feeName = db.Column(db.String, nullable = False)
    feeDescription = db.Column(db.String, nullable = False)
    defaultAmount = db.Column(db.Integer, nullable = False)
    defaultOccurrence = db.Column("Application_Occurrences", db.String, db.ForeignKey("Application_Occurrences.occurrenceID"), nullable = False)

    occurrence = db.relationship("occurrence", back_populates='defaultFeeOccurrence')#
    propertyFeeType = db.relationship("propertyFee", back_populates='feeType')#

    def __repr__(self) -> str:
        return "<feeType(feeID = '%s', Description = '%s')>" %(self.feeID, self.feeDescription)

class occurrence(db.Model):
    # This is the database relationship object for records in the Application_Occurrences table
    # Done
    __tablename__ = "Application_Occurrences"
    occurrenceID = db.Column(db.Integer, primary_key=True, nullable = False, unique = True)
    occurrenceNum = db.Column(db.Integer)
    perPeriod = db.Column(db.Integer, db.ForeignKey("Application_Periods.periodID"))

    occurrencePeriod = db.relationship("period", back_populates='periodUnit')#
    propertyFeeOccurrence = db.relationship("propertyFee", back_populates='feeOccurrence')#
    defaultFeeOccurrence = db.relationship("feeType", back_populates='occurrence')#

    def __repr__(self) -> str:
        return "<occurrence(occurrenceID = '%s', Description = '%s'/'%s')>" %(self.feeID, self.occurrenceNum, self.perPeriod)

class paymentMethod(db.Model):
    # This is the database relationship object for records in the Application_Payment_Methods table
    # 
    # Waiting to be connected to payment
    __tablename__ = "Application_Payment_Methods"
    methodID = db.Column(db.Integer, primary_key=True, nullable = False, unique = True)
    methodName = db.Column(db.String)

    specificPayment = db.relationship("payment", back_populates='paymentType')#

    def __repr__(self) -> str:
        return "<paymentMethod(methodID = '%s', methodName = '%s')>" %(self.methodID, self.methodName)

class paymentState(db.Model):
    # This is the database relationship object for records in the Application_Payment_States table
    # 
    # Waiting to be connected to payment
    __tablename__ = "Application_Payment_States"
    stateID = db.Column(db.Integer, primary_key=True, nullable = False, unique = True)
    stateName = db.Column(db.String)
    isCompleteState = db.Column(db.String)

    specificPayment = db.relationship("payment", back_populates='paymentStatus')#

    def __repr__(self) -> str:
        return "<paymentState(stateID = '%s', stateName = '%s', isComplete = '%s')>" %(self.stateID, self.stateName, self.isCompleteState)

class period(db.Model):
    # This is the database relationship object for records in the Application_Periods table
    # done
    __tablename__ = "Application_Periods"
    periodID = db.Column(db.Integer, primary_key=True, nullable = False, unique = True)
    periodName = db.Column(db.String)
    periodAbbreviation = db.Column(db.String)

    periodUnit = db.relationship("occurrence", back_populates='occurrencePeriod')#
    feePeriod = db.relationship("propertyFee", back_populates='applicablePeriod')#

    def __repr__(self) -> str:
        return "<feePeriod(periodID = '%s', periodName = '%s', periodAbbr = '%s')>" %(self.periodID, self.periodName, self.periodAbbreviation)


# """
# Section for all User entered tables
# """

class userAccount(db.Model):
    # This is the database relationship object for records in the User_Accounts table
    # Done
    __tablename__ = 'User_Accounts'
    username = db.Column(db.String, primary_key=True, nullable = True, unique = True)
    accountType = db.Column(db.Integer, db.ForeignKey("Application_Account_Types.accountTypeID"))
    emailAddress = db.Column(db.Text, nullable = False)
    passHash = db.Column(db.String, nullable = False)
    salt = db.Column(db.String)
    personID = db.Column(db.Integer)#, db.ForeignKey("User_People.personID"))
    createDate = db.Column(db.String, nullable = False)

    accountAuthority = db.relationship("accountType", back_populates="accountType")#
    user_session = db.relationship("userSession", back_populates="user")#
    authoredCompany = db.relationship("company", back_populates='author')#
    authoredPaymentItem = db.relationship("paymentItem", back_populates='author')#
    authoredPayment = db.relationship("payment", back_populates='author')#
    createdPerson = db.relationship("person", back_populates='author')#
    authoredProperty = db.relationship("property", back_populates='author')#
    authoredFee = db.relationship("propertyFee", back_populates='author')#
    # personsAccount = db.relationship("person", back_populates='accountForThisPerson')#

    def __repr__(self) -> str:
        return "<account(username  = '%s')>" % self.username

class address(db.Model):
    # This is the database relationship object for records in the User_Addresses table
    # Done
    __tablename__ = "User_Addresses"
    addressID = db.Column(db.Integer, primary_key=True, nullable = False, unique = True)
    houseNumber = db.Column(db.Integer)
    streetName = db.Column(db.String, nullable = False)
    city = db.Column(db.String, nullable = False)
    state = db.Column(db.String, nullable = False)
    zipCode = db.Column(db.Integer, nullable = False)

    companyAddress = db.relationship("company", back_populates='detailedAddress')#
    propertyAddress = db.relationship("property", back_populates='detailedAddress')#

    def __init__(self) -> None:
        return "<address(addressID = '%r', address = '%s %s %s, %s, %s %s')>" %(self.addressID, self.houseNumber, self.streetName, self.city, self.state, self.zipCode)

class company(db.Model):
    # This is the database relationship object for records in the User_Companies table
    # Done
    __tablename__ = "User_Companies"
    companyID = db.Column(db.Integer, primary_key=True, nullable = False, unique = True)
    companyName = db.Column(db.String, nullable = False)
    phoneNumber = db.Column(db.String, nullable = False)
    mailingAddress = db.Column(db.Integer, db.ForeignKey("User_Addresses.addressID"), nullable = False)
    emailAddress = db.Column(db.String, nullable = False)
    EIN = db.Column(db.String)
    createdBy = db.Column(db.String, db.ForeignKey("User_Accounts.username"), nullable = False)
    createDate = db.Column(db.String, nullable = False)

    author = db.relationship("userAccount", back_populates='authoredCompany')#
    detailedAddress = db.relationship("address", back_populates='companyAddress')#
    ownedProperty = db.relationship("property", back_populates='owner')#
    relatedPerson = db.relationship("person", back_populates='associatedCompany')#

    def __init__(self) -> None:
        return "<company(companyID = '%r', companyName = '%s')>" %(self.companyID, self.companyName)

class paymentItem(db.Model):
    # This is the database relationship object for records in the User_Payment_Items table
    # Done
    __tablename__ = "User_Payment_Items"
    paymentItemID = db.Column(db.Integer, primary_key = True, nullable = False, unique = True)
    paymentID = db.Column(db.Integer, db.ForeignKey("User_Payments.paymentID"))
    dueDate = db.Column(db.String)
    itemName = db.Column(db.String)
    leaseFeeID = db.Column(db.Integer, db.ForeignKey("User_Property_Fees.leaseFeeID"))
    amountPaid = db.Column(db.String)
    createdBy = db.Column(db.String, db.ForeignKey("User_Accounts.username"))
    createDate = db.Column(db.String)

    author = db.relationship("userAccount", back_populates='authoredPaymentItem')#
    associatedPropertyFee = db.relationship("propertyFee", back_populates="createdPaymentItem")#
    associatedPayment = db.relationship("payment", back_populates="specificPaymentItem")#

    def __init__(self) -> None:
        return "<paymentItem(paymentID = '%r', paymentItemID = '%s')>" %(self.paymentID, self.paymentItemID)

class payment(db.Model):
    # This is the database relationship object for records in the User_Payments table
    # Done
    __tablename__ = "User_Payments"
    paymentID = db.Column(db.Integer, primary_key = True, nullable = False, unique = True)
    dueDate = db.Column(db.String)
    paymentState = db.Column(db.Integer, db.ForeignKey("Application_Payment_States.stateID"), nullable = False)
    paymentMethod = db.Column(db.Integer, db.ForeignKey("Application_Payment_Methods.methodID"), nullable = False)
    amountReceived = db.Column(db.String)
    dateReceived = db.Column(db.String)
    createdBy = db.Column(db.String, db.ForeignKey("User_Accounts.username"))
    createDate = db.Column(db.String)

    author = db.relationship("userAccount", back_populates='authoredPayment')#
    specificPaymentItem = db.relationship("paymentItem", back_populates="associatedPayment")#
    paymentStatus = db.relationship("paymentState", back_populates='specificPayment')#
    paymentType = db.relationship("paymentMethod", back_populates='specificPayment')#

    def __init__(self) -> None:
        return "<payment(paymentID = '%r', paymentStatus = '%s', amount = '%s')>" %(self.companyID, self.paymentStatus, self.amountReceived)

class person(db.Model):
    # This is the database relationship object for records in the User_People table
    # Done
    __tablename__ = "User_People"
    personID = db.Column(db.Integer, primary_key=True, nullable = False)
    revision = db.Column(db.Integer, primary_key=True, nullable = False)
    firstName = db.Column(db.String, nullable = False)
    lastName = db.Column(db.String, nullable = False)
    phoneNumber = db.Column(db.Integer)
    DOB = db.Column(db.String, nullable = False)
    annualIncome = db.Column(db.String)
    companyID = db.Column(db.Integer, db.ForeignKey("User_Companies.companyID"))
    createdBy = db.Column(db.String, db.ForeignKey("User_Accounts.username"))
    createDate = db.Column(db.String, nullable = False)

    author = db.relationship("userAccount", back_populates='createdPerson')#
    associatedCompany = db.relationship("company", back_populates='relatedPerson')#
    # accountForThisPerson = db.relationship("userAccount", back_populates='personsAccount')#
    leasedProperty = db.relationship("property", back_populates='tenant')#

    def __repr__(self) -> str:
        return "<person(firstName = '%s', lastName = '%s', username = '%s')>" %(self.firstName, self.lastName, self.username)

class property(db.Model):
    # This is the database relationship object for records in the User_Properties table
    # Done
    __tablename__ = "User_Properties"
    propertyID = db.Column(db.Integer, primary_key=True, nullable = False, unique = True)
    companyID = db.Column(db.Integer, db.ForeignKey("User_Companies.companyID"), nullable = False)
    addressID = db.Column(db.Integer, db.ForeignKey("User_Addresses.addressID"), nullable = False)
    bedroomCount = db.Column(db.String, nullable = False)
    bathroomCount = db.Column(db.String, nullable = False)
    parkingSpotCount = db.Column(db.String, nullable = False)
    storyCount = db.Column(db.String, nullable = False)
    homeType = db.Column(db.String, nullable = False)
    description = db.Column(db.String, nullable = False)
    defaultRentAmount = db.Column(db.String, nullable = False)
    renter = db.Column(db.Integer, db.ForeignKey("User_People.personID"))
    purchasePrice = db.Column(db.String)
    purchaseDate = db.Column(db.String)
    nickname = db.Column(db.String)
    schoolDistrict = db.Column(db.String)
    createdBy = db.Column(db.String, db.ForeignKey("User_Accounts.username"), nullable = False)
    createDate = db.Column(db.String, nullable = False)

    author = db.relationship("userAccount", back_populates='authoredProperty')#
    detailedAddress = db.relationship("address", back_populates='propertyAddress')#
    owner = db.relationship("company", back_populates='ownedProperty')#
    tenant = db.relationship("person", back_populates='leasedProperty')#
    applicableFee = db.relationship("propertyFee", back_populates='applicableProperty')#

    def __init__(self) -> None:
        return "<property(propertyID = '%r', nickname = '%s', address = '%s')>" %(self.propertyID, self.nickname, self.detailedAddress)

class propertyFee(db.Model):
    # This is the database relationship object for records in the User_Property_Fees table
    # Done
    __tablename__ = "User_Property_Fees"
    leaseFeeID = db.Column(db.Integer, primary_key=True, nullable = False, unique = True)
    propertyID = db.Column(db.Integer, db.ForeignKey("User_Properties.propertyID"), nullable = False)
    feeID = db.Column(db.Integer, db.ForeignKey("Application_Fee_Types.feeID"), nullable = False)
    feeName = db.Column(db.String, nullable = False)
    feeAmount = db.Column(db.String, nullable = False)
    occurrence = db.Column(db.String, db.ForeignKey("Application_Occurrences.occurrenceID"), nullable = False)
    startAfterLength = db.Column(db.String, nullable = False)
    startAfterPeriod = db.Column(db.String, db.ForeignKey("Application_Periods.periodID"), nullable = False)
    createdBy = db.Column(db.String, db.ForeignKey("User_Accounts.username"), nullable = False)
    createDate = db.Column(db.String, nullable = False)

    applicableProperty = db.relationship("property", back_populates='applicableFee')#
    feeType = db.relationship("feeType", back_populates='propertyFeeType')#
    feeOccurrence = db.relationship("occurrence", back_populates='propertyFeeOccurrence')#
    applicablePeriod = db.relationship("period", back_populates='feePeriod')#
    author = db.relationship("userAccount", back_populates='authoredFee')#
    createdPaymentItem = db.relationship("paymentItem", back_populates='associatedPropertyFee')#


    def __repr__(self) -> str:
        return "<propertyFee(leaseFeeID = '%s', feeName = '%s', feeAmount = '%s', feeOccurrence = '%s')>" %(self.feeID, self.feeName, self.feeAmount, self.feeOccurrence)

class userSession(db.Model):
    # This is the database relationship object for records in the User_Sessions table
    # Done
    __tablename__ = 'User_Sessions'
    sessionID = db.Column(db.String, primary_key=True, nullable=False, unique=True)
    username = db.Column(db.String, db.ForeignKey('User_Accounts.username'), nullable=False)
    loginDatetime = db.Column(db.DateTime, nullable = False)
    expiredDatetime = db.Column(db.DateTime, nullable = False)
    nextDatetime = db.Column(db.DateTime, nullable = False)

    user = db.relationship("userAccount", back_populates="user_session")#

    def __repr__(self) -> str:
        return "<Session(ID = '%s')>" % self.sessionID








# class Product(db.Model):
#     __tablename__ = 'Products'
#     ProductID = db.Column(db.Integer, primary_key=True)
#     Brand = db.Column(db.String)
#     Model = db.Column(db.String)

#     posts = db.relationship("BlogPost", back_populates='products')

#     def __repr__(self) -> str:
#         return "<Product(ProductID = '%s', Brand = '%s', Model = '%s')>" %(self.ProductID, self.Brand, self.Model)


# class Employee(db.Model):
#     __tablename__ = 'Employees'
#     EmployeeID = db.Column (db.Integer, primary_key=True)
#     FirstName = db.Column (db.String)
#     LastName = db.Column (db.String)
#     DOB = db.Column (db.Date)
#     EmpDept = db.Column ('Department', db.Integer, db.ForeignKey('Departments.DepartmentID'))
#     Manager = db.Column (db.Integer, db.ForeignKey('Employees.EmployeeID'))
#     Username = db.Column (db.String, unique = True)

#     employee_dept = db.relationship("Department", back_populates='department_id')
#     employee_id = db.relationship("Comments", back_populates='approver')

#     def __repr__(self) -> str:
#         return "<Employee(EmployeeID = '%s', FirstName = '%s', LastName = '%s')>" %(self.EmployeeID, self.FirstName, self.LastName)


# class BlogPost(db.Model):
#     __tablename__ = 'ProductReviews'
#     ReviewID = db.Column(db.Integer, primary_key=True)
#     ProductID = db.Column(db.Integer, db.ForeignKey('Products.ProductID'))
#     ReviewerID = db.Column(db.Integer, db.ForeignKey('Employees.EmployeeID'))
#     Title = db.Column(db.String(100), nullable=False)
#     ReviewText = db.Column(db.String, nullable=False)
#     OriginalPostDate = db.Column(db.String, nullable=False)
#     Revision = db.Column(db.Integer, nullable = False)
#     LatestEditDate = db.Column(db.String, nullable = False)
#     RevisionReason = db.Column(db.String)
#     isFree = db.Column(db.Integer)

#     products = db.relationship("Product", back_populates='posts')

#     def __init__(self) -> None:
#         super().__init__()
#         commentsShown=0
#         self.__comments = []

#     def getMoreComments(self, count=20):
#         self.commentsShown+=count
#         commts = Comments.query.filter_by(ReviewID = self.ReviewID).limit(count).all()
#         for comment in commts:
#             self.__comments.append(comment)
#         return self.__comments



#     def __repr__(self) -> str:
#         return "<BlogPost(ReviewID = '%s', ProductID = '%s', Title = '%s')>" %(self.ReviewID, self.ProductID, self.Title)


class Department(db.Model):
    __tablename__ = "Departments"
    DepartmentID = db.Column(db.Integer, primary_key=True)
    DepartmentName = db.Column(db.String)
    PageID = db.Column(db.String)
    IsSolution = db.Column(db.Integer)
    Icon = db.Column(db.String)
    Description = db.Column(db.String)

    # department_id = db.relationship("Employee", back_populates='employee_dept')

    def __repr__(self) -> str:
        return "<Department(DepartmentID = '%s', Description = '%s')>" %(self.DepartmentID, self.Description)

# class Comments(db.Model):
#     __tablename__ = "Comments"
#     CommentID = db.Column(db.Integer, primary_key=True, nullable = False, unique = True)
#     ReviewID = db.Column(db.Integer, db.ForeignKey('ProductReviews.ReviewID'))
#     CommentDate = db.Column(db.DateTime, nullable = False)
#     Title = db.Column(db.String, nullable = False)
#     CommentText = db.Column(db.String, nullable = False)
#     Username = db.Column(db.String, nullable = False)
#     approvedBy = db.Column(db.Integer, db.ForeignKey('Employees.EmployeeID'))
#     approveddate = db.Column(db.DateTime)
#     ReplyingTo = db.Column(db.Integer, db.ForeignKey('Comments.CommentID'))

#     approver = db.relationship("Employee", back_populates='employee_id')

#     def __repr__(self) -> str:
#         return "<Comment(Title = '%s', Date = '%r', Author = '%r')>" % (self.Title, self.CommentDate, self.Username)

# class UserType(db.Model):
#     __tablename__ = "UserType"
#     UserTypeID = db.Column(db.Integer, primary_key=True, nullable = False, unique = True)
#     Cost = db.Column(db.Integer)
#     MembershipName = db.Column(db.String)

#     member_type = db.relationship("Memberships", back_populates='memberships')

#     def __init__(self) -> None:
#         return "<UserType(Membership Name = '%r')>" % self.MembershipName

# class Memberships(db.Model):
#     __tablename__ = "Membership"
#     Username = db.Column(db.String, primary_key=True)
#     UserTypeID = db.Column(db.Integer, db.ForeignKey('UserType.UserTypeID'), primary_key = True)
#     PaymentDate = db.Column(db.String)
#     ExpirationDate = db.Column(db.String)
#     TransactionID = db.Column(db.String, nullable = False)
    
#     memberships = db.relationship("UserType", back_populates='member_type')

#     def __repr__(self) -> str:
#         return "<Membership(Owner = '%s', Subscription Level = '%r', Expiration Date = '%r')>" % (self.Username, self.UserTypeID, self.ExpirationDate)

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

