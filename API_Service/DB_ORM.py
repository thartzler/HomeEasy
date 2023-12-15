from flask_sqlalchemy import SQLAlchemy

from datetime import datetime, timedelta


db = SQLAlchemy()


#Define classes for each of the tables along with relationships
# """
# Section for all Application common tables
# """

class accountType(db.Model):
    # This is the database relationship object for records in the appAccountTypes table
    # Done
    __tablename__ = 'appAccountTypes'
    accountTypeID =     db.Column(db.Integer, primary_key=True, nullable = False)
    # cost =              db.Column(db.String, nullable = False)
    typeName =          db.Column(db.VARCHAR(40), nullable = False)
    typeDescription =   db.Column(db.VARCHAR(100), nullable = False)

    userAccountsWithAccountType = db.relationship('userAccount', back_populates='accountAuthority') #done
    companyRoleType = db.relationship('companyRole', back_populates='associatedAccountType')    #done

    def __repr__(self) -> str:
        return "<accountType(Account Type Name = '%s')>" % self.typeName

class feeType(db.Model):
    # This is the database relationship object for records in the appFeeTypes table
    # Done
    __tablename__ = 'appFeeTypes'
    feeID =             db.Column(db.Integer, primary_key=True, nullable = False, unique = True)
    feeName =           db.Column(db.Text, nullable = False)
    description =       db.Column(db.Text, nullable = False)
    defaultPrice =      db.Column(db.DECIMAL(8,2), nullable = True)
    defaultOccurrence = db.Column(db.Integer, db.ForeignKey('appOccurrences.occurrenceID'), nullable = True)

    feeTypeLeases =     db.relationship('leaseFee', back_populates='leaseFeeType')          #done
    feeTypeOccurrence = db.relationship('occurrence', back_populates='occurrenceFeeTypes')  #done

    def __repr__(self) -> str:
        return "<feeType(feeID = '%s', Description = '%s')>" %(self.feeID, self.description)

class occurrence(db.Model):
    # This is the database relationship object for records in the appOccurrences table
    # Done
    __tablename__ = 'appOccurrences'
    occurrenceID =  db.Column(db.Integer, primary_key=True, nullable = False)
    occurrence = db.Column(db.Integer, nullable = False)
    perPeriod =     db.Column(db.Integer, db.ForeignKey('appPeriods.periodID'), nullable = True)

    # occurrenceOfLeasePayments = db.relationship('lease', back_populates = 'paymentOccurrence')           #done
    # occurrenceOfPaymentAfterLeases = db.relationship('lease', back_populates = 'paymentOccurrenceAfterLease') #done
    occurrenceFeeTypes = db.relationship('feeType', back_populates='feeTypeOccurrence')     #done
    occurrenceLeaseFees = db.relationship('leaseFee', back_populates='leaseFeeOccurrence')  #done
    occurrencePeriod = db.relationship('period', back_populates='periodOccurrences')        #done

    def __repr__(self) -> str:
        return "<occurrence(occurrenceID = '%s', Occurrence = '%s'/'%s')>" %(self.occurrenceID, self.occurrence, self.perPeriod)

class paymentMethod(db.Model):
    # This is the database relationship object for records in the appPaymentMethods table
    # Done
    __tablename__ = 'appPaymentMethods'
    methodID =   db.Column(db.Integer, primary_key=True, nullable = False)
    methodName = db.Column(db.VARCHAR(30), nullable = False)

    paymentsWithMethod = db.relationship('payment', back_populates='methodOfPayment')   #done

    def __repr__(self) -> str:
        return "<paymentMethod(methodID = '%s', methodName = '%s')>" %(self.methodID, self.methodName)

class paymentStatus(db.Model):
    # This is the database relationship object for records in the appPaymentStatus table
    # Done
    __tablename__ = 'appPaymentStatus'
    statusID =      db.Column(db.Integer, primary_key=True, nullable = False, unique = True)
    statusName =    db.Column(db.VARCHAR(25), nullable = False)
    isCompleted =   db.Column(db.BINARY, nullable = False, server_default=bin(0))

    paymentsWithStatus = db.relationship('payment', back_populates='statusOfPayment')   #done

    def __repr__(self) -> str:
        return "<paymentStatus(statusID = '%s', statusName = '%s', isCompleted = '%s')>" %(self.statusID, self.statusName, self.isCompleted)

class period(db.Model):
    # This is the database relationship object for records in the appPeriods table
    # Done
    __tablename__ = 'appPeriods'
    periodID =      db.Column(db.Integer, primary_key=True, nullable = False, unique = True)
    name =          db.Column(db.VARCHAR(20), nullable = False)
    abbreviation =  db.Column(db.VARCHAR(8), nullable = False)

    periodOccurrences = db.relationship('occurrence', back_populates='occurrencePeriod')    #done
    periodLeaseFees = db.relationship('leaseFee', back_populates='leaseFeePeriod')          #done
    # periodEmploymentHistories = db.relationship('employmentHistory', back_populates = 'employmentSallaryPeriod')    #done - STRETCH

    def __repr__(self) -> str:
        return "<period(periodID = '%s', periodName = '%s', periodAbbr = '%s')>" %(self.periodID, self.periodName, self.periodAbbreviation)


# """
# Section for all User entered tables
# """

class userAccount(db.Model):
    # This is the database relationship object for records in the userAccounts table
    # 
    __tablename__ = 'userAccounts'
    userID =        db.Column(db.Integer, db.ForeignKey("userPeople.personID"), primary_key=True, nullable = True)
    accountTypeID = db.Column(db.Integer, db.ForeignKey("appAccountTypes.accountTypeID"))
    emailAddress =  db.Column(db.Text, nullable = False, unique = True)
    emailVerified = db.Column(db.BINARY, nullable = False, server_default=bin(0))
    passHash =      db.Column(db.VARCHAR(72), nullable = False)
    createDate =    db.Column(db.Date, nullable = False)
    attemptsSinceLastLogin = db.Column(db.Integer, nullable = False, server_default = '0')

    accountAuthority =      db.relationship('accountType', back_populates='userAccountsWithAccountType')     #done
    accountPerson =         db.relationship('person', back_populates='personsAccount')              #done
    authoredPayment =       db.relationship('payment', back_populates='paymentCreator')             #done
    userAccountSessions =   db.relationship('userSession', back_populates='sessionUser')            #done
    authoredProperty =      db.relationship('property', back_populates='propertyAuthor')            #done
    authoredLease =         db.relationship('lease', back_populates='leaseAuthor')                  #done
    authoredPaymentItems =  db.relationship('paymentItem', back_populates='paymentItemCreator')     #done
    authoredLeaseFees =     db.relationship('leaseFee', back_populates='leaseFeeAuthor')            #done
    companyRolePerson =     db.relationship('companyRole', foreign_keys = 'companyRole.userID', back_populates='companyRoleUserAccount') #done
    createdCompanyRoles =   db.relationship('companyRole', foreign_keys = 'companyRole.assignedUser', back_populates='companyRoleCreator')     #done
    removedCompanyRoles =   db.relationship('companyRole', foreign_keys = 'companyRole.endedUser', back_populates='companyRoleRemover')     #done
    authoredCompanies =     db.relationship('company', back_populates='companyCreator')             #done

    def __repr__(self) -> str:
        return "<account(userID  = '%s')>" % self.userID

class address(db.Model):
    # This is the database relationship object for records in the userAddresses table
    # Done
    __tablename__ = "userAddresses"
    addressID =     db.Column(db.Integer, primary_key=True, nullable = False)
    houseNumber =   db.Column(db.Integer, nullable = False)
    streetName =    db.Column(db.VARCHAR(30), nullable = False)
    apptNo =        db.Column(db.VARCHAR(6), nullable = True)
    city =          db.Column(db.VARCHAR(30), nullable = False)
    state =         db.Column(db.VARCHAR(2), nullable = False)
    zipCode =       db.Column(db.Numeric(5,0), nullable = False)

    companiesWithMailingAddress = db.relationship('company', foreign_keys = 'company.mailingAddress', back_populates='companyMailingAddress') #done
    companiesWithBillingAddress = db.relationship('company', foreign_keys = 'company.billingAddress', back_populates='companyBillingAddress') #done
    relatedPerson = db.relationship('person', back_populates='associatedAddress')       #done
    propertyAddress = db.relationship('property', back_populates='fullAddress')         #done
    # currentApplicantAddress = db.relationship('application', back_populates='currentApplicantDetailedAddress')  #missing - STRETCH
    # previousApplicantAddress = db.relationship('application', back_populates='previousApplicantDetailedAddress')  #missing - STRETCH

    def getHouseNStreet(self) -> str:
        if self.apptNo:
            return '%s %s Apt. %s'%(self.houseNumber, self.streetName, self.apptNo)
        else:
            return '%s %s'%(self.houseNumber, self.streetName)
    
    def __repr__(self) -> str:
        return "<address(addressID = '%r', address = '%s %s %s, %s, %s %s')>" %(self.addressID, self.houseNumber, self.streetName, self.apptNo, self.city, self.state, self.zipCode)

class company(db.Model):
    # This is the database relationship object for records in the userCompanies table
    # Done
    __tablename__ = 'userCompanies'
    companyID =         db.Column(db.Integer, primary_key=True, nullable = False)
    companyName =       db.Column(db.VARCHAR(50), nullable = False)
    phoneNumber =       db.Column(db.VARCHAR(10), nullable = False)
    mailingAddress =    db.Column(db.Integer, db.ForeignKey('userAddresses.addressID'), nullable = False)
    billingAddress =    db.Column(db.Integer, db.ForeignKey('userAddresses.addressID'), nullable = True)
    emailInvoiceAddress=db.Column(db.VARCHAR(50), nullable = True)
    EIN =               db.Column(db.Integer, nullable = True)
    createdBy =         db.Column(db.Integer, db.ForeignKey('userAccounts.userID'), nullable = False)
    createDate =        db.Column(db.DateTime, nullable = False)

    companyMailingAddress =    db.relationship('address', foreign_keys=[mailingAddress], back_populates='companiesWithMailingAddress')  #done
    companyBillingAddress =    db.relationship('address', foreign_keys=[billingAddress], back_populates='companiesWithBillingAddress')  #done
    ownedProperty =     db.relationship('property', back_populates='propertyOwner')         #done
    relatedPersonRole = db.relationship('companyRole', back_populates='associatedCompany')       #done
    companyCreator =    db.relationship('userAccount', back_populates='authoredCompanies')    #done
    
    def __repr__(self) -> str:
        return "<company(companyID = '%r', companyName = '%s')>" %(self.companyID, self.companyName)

class paymentItem(db.Model):
    # This is the database relationship object for records in the userPaymentItems table
    # Done
    __tablename__ = 'userPaymentItems'
    paymentItemID = db.Column(db.Integer, primary_key = True, nullable = False, unique = True)
    paymentID =     db.Column(db.Integer, db.ForeignKey('userPayments.paymentID'), nullable = False)
    dueDate =       db.Column(db.Date, nullable = False)
    itemName =      db.Column(db.VARCHAR(50), nullable = False)
    leaseFeeID =    db.Column(db.Integer, db.ForeignKey('userLeaseFees.leaseFeeID'), nullable = False)
    amountPaid =    db.Column(db.Float, nullable = True)
    createUser =    db.Column(db.Integer, db.ForeignKey('userAccounts.userID'), nullable = False)
    createDate =    db.Column(db.DateTime, nullable = False)

    associatedPayment = db.relationship('payment', back_populates='paymentItems')   #done
    paymentItemCreator = db.relationship('userAccount', back_populates='authoredPaymentItems')  #done
    paymentItemLeaseFee =  db.relationship('leaseFee', back_populates='leaseFeePaymentItems')   #done

    def __repr__(self) -> str:
        return "<paymentItem(paymentID = '%r', paymentItemID = '%s')>" %(self.paymentID, self.paymentItemID)

class payment(db.Model):
    # This is the database relationship object for records in the userPayments table
    # Done
    __tablename__ = 'userPayments'
    paymentID =     db.Column(db.Integer, primary_key = True, nullable = False)
    dueDate =       db.Column(db.Date, nullable = False)
    paymentStatus = db.Column(db.Integer, db.ForeignKey("appPaymentStatus.statusID"), nullable = True)
    paymentMethod = db.Column(db.Integer, db.ForeignKey("appPaymentMethods.methodID"), nullable = True)
    amountReceived =db.Column(db.Float, nullable = True)
    dateReceived =  db.Column(db.Date, nullable = False)
    createUser =    db.Column(db.Integer, db.ForeignKey("userAccounts.userID"), nullable = False)
    createDate =    db.Column(db.DateTime, nullable = False)

    paymentCreator =  db.relationship('userAccount', back_populates='authoredPayment')      #done
    paymentItems =    db.relationship('paymentItem', back_populates='associatedPayment')    #done
    statusOfPayment = db.relationship('paymentStatus', back_populates='paymentsWithStatus') #done
    methodOfPayment = db.relationship('paymentMethod', back_populates='paymentsWithMethod') #done

    def __repr__(self) -> str:
        return "<payment(paymentID = '%r', paymentStatus = '%s', amount = '%s')>" %(self.paymentID, self.paymentStatus, self.amountReceived)

class person(db.Model):
    # This is the database relationship object for records in the userPeople table
    # Done
    __tablename__ = "userPeople"
    personID = db.Column(db.Integer, primary_key=True, nullable = False)
    # revision = db.Column(db.Integer, primary_key=True, nullable = False)
    firstName = db.Column(db.VARCHAR(50), nullable = False)
    lastName = db.Column(db.VARCHAR(50), nullable = True)
    phoneNumber = db.Column(db.CHAR(10), nullable = False)
    addressID = db.Column(db.Integer, db.ForeignKey("userAddresses.addressID"), nullable = True)
    createdOn = db.Column(db.DateTime, nullable = False)

    relatedPersonDetails =  db.relationship('personDetail', foreign_keys= 'personDetail.personID', back_populates='associatedPerson')    #done
    personDetailSetPerson = db.relationship('personDetail', foreign_keys= 'personDetail.setPersonID', back_populates='associatedCreator') #done
    # personReference =       db.relationship('reference',    back_populates='referencePerson')   #missing - Stretch
    # personEmploymentHistories = db.relationship('employmentHistory', back_populates='employmentHistoryPerson')   #missing - Stretch
    # personEmploymentSupervisor = db.relationship('employmentHistory', back_populates='employmentSupervisorPerson')   #missing - Stretch
    associatedAddress =     db.relationship('address', back_populates='relatedPerson')    #done
    personsAccount =        db.relationship('userAccount',back_populates='accountPerson')          #done
    personLeases =          db.relationship('leasePerson', back_populates = 'leasePerson')          #done
    # personApplicant =     db.relationship('application', back_populates='applicantPerson')        #missing - Stretch
    # personCoApplicant =   db.relationship('application', back_populates='coApplicantPerson')      #missing - Stretch
    # personCurrentOwner =  db.relationship('application', back_populates='currentOwnerPerson')     #missing - Stretch
    # personPreviousOwner = db.relationship('application', back_populates='previousOwnerPerson')    #missing - Stretch

    def __repr__(self) -> str:
        return "<person(firstName = '%s', lastName = '%s', personID = '%s')>" %(self.firstName, self.lastName, self.personID)
    
class personDetail(db.Model):
    # This is the database relationship object for records in the userPersonDetails table
    # Done
    __tablename__ = 'userPersonDetails'
    personID =      db.Column(db.Integer, db.ForeignKey("userPeople.personID"), primary_key = True, nullable = False)
    detailID =      db.Column(db.Integer, db.ForeignKey("userDetailOptions.detailID"), primary_key = True, nullable = False)
    rev =           db.Column(db.Integer, primary_key = True, nullable = False)
    propertyValue = db.Column(db.VARCHAR(50), nullable = True)
    setDate =       db.Column(db.DateTime, nullable = False)
    setPersonID =   db.Column(db.Integer, db.ForeignKey("userPeople.personID"), nullable = False)

    associatedPerson = db.relationship('person', foreign_keys=[personID], back_populates='relatedPersonDetails')      #done
    associatedDetail = db.relationship('personDetailOption', back_populates='personDetailName') #done
    associatedCreator = db.relationship('person', foreign_keys=[setPersonID], back_populates='personDetailSetPerson')   #done

    def __repr__(self) -> str:
        return "<personDetail(personID = '%i', detailID = '%i', rev = '%i', propertyValue = '%s')>" %(self.personID, self.detailID, self.rev, self.propertyValue)

class personDetailOption(db.Model):
    # This is the database relationship object for records in the userPersonDetailOptions table
    # Done
    __tablename__ = 'userDetailOptions'
    detailID = db.Column(db.Integer, primary_key = True, nullable = False)
    propertyName = db.Column(db.VARCHAR(100), nullable = True)

    personDetailName = db.relationship('personDetail', back_populates='associatedDetail')   #done

    def __repr__(self) -> str:
        return "<personDetailOption(detailID = '%i', propertyName = '%s')>" %(self.detailID, self.propertyName)

class companyRole(db.Model):
    # This is the database relationship object for records in the userCompanyRoles table
    # Done
    __tablename__ = "userCompanyRoles"
    roleID =        db.Column(db.Integer, primary_key = True, nullable = False)
    companyID =     db.Column(db.Integer, db.ForeignKey("userCompanies.companyID"), nullable = False)
    userID =        db.Column(db.Integer, db.ForeignKey("userAccounts.userID"), nullable = False)
    roleTypeID =    db.Column(db.Integer, db.ForeignKey("appAccountTypes.accountTypeID"), nullable = False)
    role_begin =    db.Column(db.Integer, nullable = False)
    assignedUser =  db.Column(db.Integer, db.ForeignKey("userAccounts.userID"), nullable = False)
    role_end =      db.Column(db.Integer, nullable = True)
    endedUser =     db.Column(db.Integer, db.ForeignKey("userAccounts.userID"), nullable = True)
    

    associatedCompany = db.relationship('company', back_populates='relatedPersonRole')          #done
    companyRoleUserAccount = db.relationship('userAccount', foreign_keys=[userID], back_populates='companyRolePerson') #done
    associatedAccountType = db.relationship('accountType', back_populates='companyRoleType')    #done
    companyRoleCreator = db.relationship('userAccount', foreign_keys=[assignedUser], back_populates='createdCompanyRoles')   #done
    companyRoleRemover = db.relationship('userAccount', foreign_keys=[endedUser], back_populates='removedCompanyRoles')   #done

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
    homeType =          db.Column(db.VARCHAR(50), nullable = False)
    yearBuilt =         db.Column(db.Numeric(4,0), nullable = True)
    purchasePrice =     db.Column(db.Integer, nullable = True)
    purchaseDate =      db.Column(db.Date, nullable = True)
    schoolDistrict =    db.Column(db.VARCHAR(50), nullable = False)
    nickname =          db.Column(db.VARCHAR(50), nullable = False)
    createUser =        db.Column(db.Integer, db.ForeignKey('userAccounts.userID'), nullable = False)
    createDate =        db.Column(db.DateTime, nullable = False)
    
    fullAddress = db.relationship('address', back_populates='propertyAddress')          #done
    propertyOwner = db.relationship('company', back_populates='ownedProperty')          #done
    propertyLease = db.relationship('lease', back_populates='leasedProperty')           #done
    propertyAuthor = db.relationship('userAccount', back_populates='authoredProperty')  #done

    def __repr__(self) -> None:
        return "<property(propertyID = '%r', nickname = '%s', address = '%s')>" %(self.propertyID, self.nickname, self.fullAddress)

class lease(db.Model):
    # This is the database relationship object for records in the userLeases table
    # Done
    __tablename__ = 'userLeases'
    leaseID =                   db.Column(db.Integer, primary_key= True, nullable = False)
    propertyID =                db.Column(db.Integer, db.ForeignKey('userProperties.propertyID'), nullable = False)
    leaseStatus =               db.Column(db.VARCHAR(25), nullable = True)
    availableDate =             db.Column(db.Date, nullable = False)
    moveInDate =                db.Column(db.Date, nullable = True)
    terminationDate =           db.Column(db.Date, nullable = True)
    leaseOccurrence =           db.Column(db.Integer, db.ForeignKey('appOccurrences.occurrenceID'), nullable = False)
    leaseSuccessionOccurrence = db.Column(db.Integer, db.ForeignKey('appOccurrences.occurrenceID'), nullable = True)
    securityDeposit =           db.Column(db.Float, nullable = False)
    contractDocID =             db.Column(db.VARCHAR(50), nullable = True)
    createUser =                db.Column(db.Integer, db.ForeignKey('userAccounts.userID'), nullable = False)
    createDate =                db.Column(db.DateTime, nullable = False)

    leasedProperty  = db.relationship('property', back_populates='propertyLease')       #done
    # leaseDependants = db.relationship('dependant', back_populates='dependantOnLease')   #missing - STRETCH
    leasePeople     = db.relationship('leasePerson',back_populates = 'leasePersonIsOn') #done
    leaseFees       = db.relationship('leaseFee', back_populates = 'FeeOnLease')        #done
    leaseAuthor     = db.relationship('userAccount', back_populates = 'authoredLease')  #done
    # applications    = db.relationship('application', back_populates='lease')            #missing - STRETCH
    paymentOccurrence = db.relationship('occurrence', foreign_keys=[leaseOccurrence])           #done
    paymentOccurrenceAfterLease = db.relationship('occurrence', foreign_keys=[leaseSuccessionOccurrence])#back_populates = 'occurrenceOfPaymentAfterLeases') #done

    def __repr__(self) -> None:
        return "<lease(leaseID = '%r', property = '%s', status = '%s')>" %(self.leaseID, self.leasedProperty, self.leaseStatus)

class leasePerson(db.Model):
    # This is the database relationship object for records in the userLeasePeople table
    # Done
    __tablename__ = "userLeasePeople"
    leaseID     = db.Column(db.Integer, db.ForeignKey('userLeases.leaseID'),  primary_key = True, nullable = False)
    personID    = db.Column(db.Integer, db.ForeignKey('userPeople.personID'), primary_key = True, nullable = False)
    role        = db.Column(db.VARCHAR(50), nullable = False)
    
    leasePerson =       db.relationship('person', back_populates = 'personLeases')      #done
    leasePersonIsOn =   db.relationship('lease',back_populates = 'leasePeople')         #done

    def __repr__(self) -> None:
        return "<leasePerson(leaseID = '%s' connects personID = '%s', role = '%s')>" %(self.leaseID, self.personID, self.role)

class leaseFee(db.Model):
    # This is the database relationship object for records in the userLeaseFees table
    # Done
    __tablename__ = "userLeaseFees"
    leaseFeeID =        db.Column(db.Integer, primary_key=True, nullable = False)
    leaseID =           db.Column(db.Integer, db.ForeignKey("userLeases.leaseID"), nullable = False)
    feeID =             db.Column(db.Integer, db.ForeignKey("appFeeTypes.feeID"), nullable = False)
    feeName =           db.Column(db.VARCHAR(30), nullable = False)
    feeAmount =         db.Column(db.Float, nullable = False)
    occurrence =        db.Column(db.Integer, db.ForeignKey("appOccurrences.occurrenceID"), nullable = False)
    startAfterLength =  db.Column(db.String, nullable = False)
    startAfterPeriod =  db.Column(db.Integer, db.ForeignKey("appPeriods.periodID"), nullable = False)
    createdUser =       db.Column(db.Integer, db.ForeignKey("userAccounts.userID"), nullable = False)
    createDate =        db.Column(db.DateTime, nullable = False)

    FeeOnLease =            db.relationship('lease', back_populates = 'leaseFees')              #done
    leaseFeeType =          db.relationship('feeType', back_populates='feeTypeLeases')          #done
    leaseFeeOccurrence =    db.relationship('occurrence', back_populates='occurrenceLeaseFees')  #done
    leaseFeePeriod =        db.relationship('period', back_populates='periodLeaseFees')         #done
    leaseFeeAuthor =        db.relationship('userAccount', back_populates='authoredLeaseFees')  #done
    leaseFeePaymentItems =  db.relationship('paymentItem', back_populates='paymentItemLeaseFee')#done

    def __repr__(self) -> str:
        return "<leaseFee(leaseFeeID = '%s', feeName = '%s', feeAmount = '%s', feeOccurrence = '%s')>" %(self.feeID, self.feeName, self.feeAmount, self.feeOccurrence)

class userSession(db.Model):
    # This is the database relationship object for records in the userSessions table
    # Done
    __tablename__ = 'userSessions'
    sessionID =     db.Column(db.NVARCHAR(50), primary_key=True, nullable=False)
    userID =        db.Column(db.Integer, db.ForeignKey('userAccounts.userID'), nullable=False)
    IPv4_ipAddress =db.Column(db.VARCHAR(15), nullable = False)
    loginDatetime = db.Column(db.DateTime, nullable = False)
    expiredDatetime = db.Column(db.DateTime, nullable = False)
    nextDatetime = db.Column(db.DateTime, nullable = False)

    sessionUser = db.relationship('userAccount', back_populates='userAccountSessions')    #done

    def __repr__(self) -> str:
        return "<Session(ID = '%s')>" % self.sessionID
