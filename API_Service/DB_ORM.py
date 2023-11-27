from flask_sqlalchemy import SQLAlchemy

from datetime import datetime, timedelta
import secrets


db = SQLAlchemy()


#Define classes for each of the tables along with relationships
# """
# Section for all Application common tables
# """

class accountType(db.Model):
    # This is the database relationship object for records in the Application_Account_Types table
    # 
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
    # 
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
    # 
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
    # 
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
    # 
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
    authoredCompany = db.relationship('company', back_populates='companyCreator')       #done
    authoredPaymentItem = db.relationship("paymentItem", back_populates='author')#
    authoredPayment = db.relationship("payment", back_populates='author')#
    createdPerson = db.relationship("person", back_populates='author')#
    authoredProperty = db.relationship('property', back_populates='propertyAuthor')     #done
    authoredFee = db.relationship("propertyFee", back_populates='author')#
    # personsAccount = db.relationship("person", back_populates='accountForThisPerson')#

    def __repr__(self) -> str:
        return "<account(username  = '%s')>" % self.username

class address(db.Model):
    # This is the database relationship object for records in the userAddresses table
    # Done
    __tablename__ = "userAddresses"
    addressID =     db.Column(db.Integer, primary_key=True, nullable = False)
    houseNumber =   db.Column(db.Integer, nullable = False)
    streetName =    db.Column(db.VarChar(30), nullable = False)
    apptNo =        db.Column(db.varChar(6), nullable = True)
    city =          db.Column(db.VarChar(30), nullable = False)
    state =         db.Column(db.VarChar(2), nullable = False)
    zipCode =       db.Column(db.Numeric(5,0), nullable = False)

    companyMailingAddress = db.relationship('company', back_populates='mailingAddress') #done
    companyBillingAddress = db.relationship('company', back_populates='billingAddress') #done
    relatedPerson = db.relationship('person', back_populates='associatedAddress')       #done
    propertyAddress = db.relationship('property', back_populates='fullAddress')         #done
    currentApplicantAddress = db.relationship('application', back_populates='currentApplicantDetailedAddress')  #missing
    previousApplicantAddress = db.relationship('application', back_populates='previousApplicantDetailedAddress')  #missing

    def __init__(self) -> None:
        return "<address(addressID = '%r', address = '%s %s %s %s, %s, %s %s')>" %(self.addressID, self.houseNumber, self.streetName, self.apptNo, self.city, self.state, self.zipCode)

class company(db.Model):
    # This is the database relationship object for records in the userCompanies table
    # Done
    __tablename__ = "userCompanies"
    companyID =         db.Column(db.Integer, primary_key=True, nullable = False)
    companyName =       db.Column(db.varchar(50), nullable = False)
    phoneNumber =       db.Column(db.varchar(10), nullable = False)
    mailingAddress =    db.Column(db.Integer, db.ForeignKey("userAddresses.addressID"), nullable = False)
    billingAddress =    db.Column(db.Integer, db.ForeignKey("userAddresses.addressID"), nullable = True)
    emailInvoiceAddress=db.Column(db.varchar(50), nullable = True)
    EIN =               db.Column(db.Integer, nullable = True)
    createdBy =         db.Column(db.Integer, db.ForeignKey("userAccounts.userID"), nullable = False)
    createDate =        db.Column(db.DateTime, nullable = False)

    mailingAddress =    db.relationship('address', back_populates='companyMailingAddress')  #done
    billingAddress =    db.relationship('address', back_populates='companyBillingAddress')  #done
    ownedProperty =     db.relationship('property', back_populates='propertyOwner')         #done
    relatedPersonRole = db.relationship('person', back_populates='associatedCompany')       #done
    companyCreator =    db.relationship('userAccount', back_populates='authoredCompany')    #done

    def __init__(self) -> None:
        return "<company(companyID = '%r', companyName = '%s')>" %(self.companyID, self.companyName)

class paymentItem(db.Model):
    # This is the database relationship object for records in the User_Payment_Items table
    # 
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
    # 
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
    # This is the database relationship object for records in the userPeople table
    # Done
    __tablename__ = "userPeople"
    personID = db.Column(db.Integer, primary_key=True, nullable = False)
    # revision = db.Column(db.Integer, primary_key=True, nullable = False)
    firstName = db.Column(db.VarChar(50), nullable = False)
    lastName = db.Column(db.VarChar(50), nullable = True)
    phoneNumber = db.Column(db.Char(10), nullable = False)
    addressID = db.Column(db.Integer, db.ForeignKey("userAddresses.addressID"), nullable = True)
    createdOn = db.Column(db.String, nullable = False)

    associatedAddress = db.relationship('address', back_populates='relatedPerson')    #done
    relatedPersonDetail = db.relationship('personDetail', back_populates='associatedPerson')    #done
    personDetailSetPerson = db.relationship('personDetail', back_populates='associatedCreator') #done
    companyRolePerson = db.relationship('companyRole', back_populates='associatedPerson') #done
    companyRoleAssigner = db.relationship('companyRole', back_populates='associatedCreator') #done
    companyRoleRemover = db.relationship('companyRole', back_populates='associatedRemover') #done

    def __repr__(self) -> str:
        return "<person(firstName = '%s', lastName = '%s', personID = '%s')>" %(self.firstName, self.lastName, self.personID)
    
class personDetail(db.Model):
    # This is the database relationship object for records in the userPersonDetails table
    # Done
    __tablename__ = 'userPersonDetails'
    personID =      db.Column(db.Integer, db.ForeignKey("userPeople.personID"), primary_key = True, nullable = False)
    detailID =      db.Column(db.Integer, db.ForeignKey("userDetilOptions.detailID"), primary_key = True, nullable = False)
    rev =           db.Column(db.Integer, primary_key = True, nullable = False)
    propertyValue = db.Column(db.VarChar(50), nullable = True)
    setDate =       db.Column(db.DateTime, nullable = False)
    setPersonID =   db.Column(db.Integer, db.ForeignKey("userPeople.personID"), nullable = False)

    associatedPerson = db.relationship('person', back_populates='relatedPersonDetail')      #done
    associatedDetail = db.relationship('personDetailOption', back_populates='personDetailName') #done
    associatedCreator = db.relationship('person', back_populates='personDetailSetPerson')   #done

    def __repr__(self) -> str:
        return "<personDetail(personID = '%i', detailID = '%i', rev = '%i', propertyValue = '%s')>" %(self.personID, self.detailID, self.rev, self.propertyValue)

class personDetailOption(db.Model):
    # This is the database relationship object for records in the userPersonDetailOptions table
    # Done
    __tablename__ = 'userDetailOptions'
    detailID = db.Column(db.Integer, primary_key = True, nullable = False)
    propertyName = db.Column(db.Text, nullable = True)

    personDetailName = db.relationship('personDetail', back_populates='associatedDetail')   #done

    def __repr__(self) -> str:
        return "<personDetailOption(detailID = '%i', propertyName = '%s')>" %(self.detailID, self.propertyName)

class companyRole(db.Model):
    # This is the database relationship object for records in the userCompanyRoles table
    # Done
    __tablename__ = "userCompanyRoles"
    roleID =        db.Column(db.Integer, primary_key = True, nullable = False)
    companyID =     db.Column(db.Integer, db.ForeignKey("userCompanies.companyID"), nullable = False)
    userID =        db.Column(db.Integer, db.ForeignKey("userPeople.userID"), nullable = False)
    roleTypeID =    db.Column(db.Integer, db.ForeignKey("appAccountTypes.accountTypeID"), nullable = False)
    role_begin =    db.Column(db.Integer, nullable = False)
    assignedUser =  db.Column(db.Integer, db.ForeignKey("userPeople.userID"), nullable = False)
    role_end =      db.Column(db.Integer, nullable = True)
    endedUser =     db.Column(db.Integer, db.ForeignKey("userPeople.userID"), nullable = True)
    

    associatedCompany = db.relationship('company', back_populates='relatedPersonRole')  #missing
    associatedPerson = db.relationship('person', back_populates='companyRolePerson')  #done
    associatedAccountType = db.relationship('accountType', back_populates='companyRoleType')    #missing
    associatedCreator = db.relationship('person', back_populates='companyRoleAssigner') #done
    associatedRemover = db.relationship('person', back_populates='companyRoleRemover')  #done

    def __repr__(self) -> str:
        return "<companyRole(roleID = '%i', companyID = '%i', roleTypeID = '%i')>" %(self.roleID, self.userID, self.roleTypeID)



class property(db.Model):
    # This is the database relationship object for records in the userProperties table
    # Done
    __tablename__ = 'userProperties'
    propertyID =        db.Column(db.Integer, primary_key=True, nullable = False)
    companyID =         db.Column(db.Integer, db.ForeignKey('userCompanies.companyID'), nullable = False)
    addressID =         db.Column(db.Integer, db.ForeignKey('userAddresses.addressID'), nullable = False)
    bedroomCount =      db.Column(db.Integer, nullable = False)
    bathroomCount =     db.Column(db.Float, nullable = False)
    parkingCount =      db.Column(db.Integer, nullable = True)
    garageCount =       db.Column(db.Integer, nullable = True)
    storiesCount =      db.Column(db.Float, nullable = True)
    homeType =          db.Column(db.VarChar(50), nullable = False)
    yearBuilt =         db.Column(db.Numeric(4,0), nullable = True)
    purchasePrice =     db.Column(db.Integer, nullable = True)
    purchaseDate =      db.Column(db.Date, nullable = True)
    schoolDistrict =    db.Column(db.VarChar(50), nullable = False)
    nickname =          db.Column(db.VarChar(50), nullable = False)
    createUser =        db.Column(db.Integer, db.ForeignKey('userAccounts.userID'), nullable = False)
    createDate =        db.Column(db.DateTime, nullable = False)
    
    fullAddress = db.relationship('address', back_populates='propertyAddress')          #done
    propertyOwner = db.relationship('company', back_populates='ownedProperty')          #done
    propertyLease = db.relationship('person', back_populates='leasedProperty')          #missing
    propertyAuthor = db.relationship('userAccount', back_populates='authoredProperty')  #done

    def __init__(self) -> None:
        return "<property(propertyID = '%r', nickname = '%s', address = '%s')>" %(self.propertyID, self.nickname, self.fullAddress)

class propertyFee(db.Model):
    # This is the database relationship object for records in the User_Property_Fees table
    # 
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
    # 
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

