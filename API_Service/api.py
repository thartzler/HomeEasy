from flask import Flask, request
from flask_restful import Api, Resource
import os
import secrets
import bcrypt
import urllib.parse
from sqlalchemy.sql import exists

from datetime import datetime, timedelta, date
from DB_ORM import *


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

def filterPhoneNumber(phoneNumber):
    filteredPN = ""
    for chara in str(phoneNumber):
        if chara in ["0","1","2","3","4","5","6","7","8","9","x"]:
            filteredPN += chara
    return filteredPN

def newPerson(firstName, lastName, phoneNumber, addressID = None, additionalDetails = None, createPerson = None):
    
    newPerson = person(
        personID = None,
        firstName = firstName,
        lastName = lastName,
        phoneNumber = filterPhoneNumber(phoneNumber),
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

def getDateXPeriodsLater(periodBegin:datetime, period_abbreviation:str, numPeriods: int = 1) -> date:
    
    if periodBegin:
        if type(periodBegin) == date:
            periodBegin = datetime.combine(periodBegin, datetime.min.time())
        if period_abbreviation == 'wk':
            tD = periodBegin + timedelta(weeks = numPeriods)
            tD = tD.strftime("%Y-%m-%d")
        elif period_abbreviation == 'mo':
            loops = 0
            while loops < numPeriods:
                month = int(periodBegin.strftime('%m'))+1
                year = int(periodBegin.strftime("%Y"))
                if month >12:
                    month -= 12
                    year += 1
                periodBegin = datetime.strptime(str(year)+"-"+str(month)+periodBegin.strftime("-%d"), "%Y-%m-%d")
                loops +=1
            tD = periodBegin.strftime("%Y-%m-%d")
        elif period_abbreviation == 'day':
            tD = (periodBegin + timedelta(days = numPeriods)).strftime("%Y-%m-%d")
        elif period_abbreviation == 'yr':
            tD = str(int(periodBegin.strftime("%Y"))+numPeriods)+periodBegin.strftime("-%m-%d")
        else:
            return "unknown:abbr"
    else:
        return "unknown:begin"
    return datetime.strptime(tD, "%Y-%m-%d").date()

def getDateOnePeriodEarlier(periodBegin:datetime, period_abbreviation:str):
    if periodBegin:
        if period_abbreviation == 'wk':
            tD = periodBegin - timedelta(weeks = 1)
            tD = tD.strftime("%Y-%m-%d")
        elif period_abbreviation == 'mo':
            month = int(periodBegin.strftime('%m'))-1
            year = int(periodBegin.strftime("%Y"))
            if month == 0:
                month += 12
                year -= 1
            tD = str(year)+"-"+str(month)+periodBegin.strftime("-%d")
        elif period_abbreviation == 'day':
            tD = (periodBegin - timedelta(days = 1)).strftime("%Y-%m-%d")
        elif period_abbreviation == 'yr':
            tD = str(int(periodBegin.strftime("%Y"))-1)+periodBegin.strftime("-%m-%d")
        else:
            return "unknown:abbr"
    else:
        return "unknown:begin"
    return datetime.strptime(tD, "%Y-%m-%d").date()

def getBasePeriodPayment(leaseID: int):
  
    x = "No Lease"
    paymentBreakdown = []
    rentPeriodAbbr = 'mo'

    if type(leaseID) == int:
        x = 0
        leaseFees = leaseFee.query.filter_by(leaseID = leaseID).all()
        for leaseFee_i in leaseFees:
            oPN = leaseFee_i.leaseFeeOccurrence.occurrencePeriod.abbreviation
            if leaseFee_i.startAfterLength == 0 and oPN != "occr":
                paymentBreakdown.append({
                    "feeName": leaseFee_i.feeName,
                    'feeAmount': leaseFee_i.feeAmount
                })
                x += float(leaseFee_i.feeAmount)
                if leaseFee_i.feeName.lower() == 'rent':
                    rentPeriodAbbr = oPN

    return {'leaseID': leaseID,
            'payentBreakdown':paymentBreakdown,
            'paymentAmount': x,
            'rentPeriod': rentPeriodAbbr}

def calculatePayment(paymentObj:payment, payDate:datetime) -> float:
    # Calculates a payment amount given the paymentObject and the date it would be paid.

    x = "No Lease"
    applicableFees = []
    rentPeriodAbbr = 'mo'

    if type(paymentObj) == payment:
        x = 0.0
        leaseFees = leaseFee.query.filter_by(leaseID = paymentObj.leaseID).join(leaseFee.leaseFeeType).order_by(feeType.displayOrder.asc()).all()
        for leaseFee_i in leaseFees:
            qty = 0
            feesOccurrance = leaseFee_i.leaseFeeOccurrence.occurrencePeriod.abbreviation
            if leaseFee_i.feeName.lower() == 'rent':
                rentPeriodAbbr = feesOccurrance

            if feesOccurrance != "occr":
                lenActivation = leaseFee_i.startAfterLength
                if lenActivation == 0:
                    qty = 1
                else:
                    # aD = activationDate

                    activationPeriod = leaseFee_i.leaseFeePeriod.abbreviation
                    qtyFeeOccr = leaseFee_i.leaseFeeOccurrence.occurrence
                    aD = getDateXPeriodsLater(paymentObj.dueDate, activationPeriod, lenActivation)# step 1: is the fee active yet?
                    while payDate.date() > aD:
                        qty += 1                    # step 2: how many times should the fee be included?
                        if feesOccurrance == rentPeriodAbbr:
                            break # these fees only get charged once per payment
                        aD = getDateXPeriodsLater(aD, feesOccurrance, qtyFeeOccr)
            if qty != 0:
                # step 3: add it
                applicableFees.append({
                    "feeName": leaseFee_i.feeName,
                    'qty': qty,
                    'feeAmount': leaseFee_i.feeAmount,
                    'periodName': feesOccurrance
                })
                x += float(leaseFee_i.feeAmount)*qty
                        
    return {'leaseID': paymentObj.leaseID,
            'payentBreakdown':applicableFees,
            'paymentAmount': x,
            'rentPeriod': rentPeriodAbbr}

def getPaymentStatus(prprty:property, sDate:datetime, eDate:datetime, uDate:datetime) -> list:
    # this returns a list of all the given property's payment periods within the given time frame
    # payment period objects include paymentID, status, and amount
    returnData = []

    basePaymentInfo = getBasePeriodPayment(prprty.getActiveLeaseID(uDate))
    # 0. Get basic info for the current lease
    # 1. fills in all the payments in the date range (it may not be homogenious, so keep track and fill in with blanks as needed)
    # 2. if there are periods after the latest payment record and before the endDate, fill them with basePayment values
    # 3. if there are periods before the oldest payment record for the lease (maybe a prior lease), recurse through getPriorPeriodPayment() and append to front of list

    # Step 1
    paymentsWithinDateRange = payment.query.filter(payment.periodStartDate>=sDate, payment.periodStartDate<=eDate).join(payment.paymentsLease).filter(lease.propertyID == prprty.propertyID).order_by(payment.paymentID.asc()).all()
    firstPayment = None
    prevPayDate = None
    leasePeriod = basePaymentInfo['rentPeriod']
    prevLeaseID = None
    print ("PaymentsWithinDateRange: ", paymentsWithinDateRange)
    missingIcon = paymentStatus.query.filter_by(statusName="missing").one().statusIcon
    lateIcon = paymentStatus.query.filter_by(statusName="late").one().statusIcon

    for paymentWithinDateRange in paymentsWithinDateRange:
        pWDR = paymentWithinDateRange
        # save the first payment for step 3
        thisPayDate = pWDR.periodStartDate
        print ("TPD: ",thisPayDate)
        if firstPayment == None:
            firstPayment = pWDR
            nextPayDate = thisPayDate
        
        # Check for missing payments
        while thisPayDate> nextPayDate:
            # apparently it's skipped one.
            if pWDR.leaseID == prevLeaseID:
                amt = 0.0
            else:
                amt = "No Lease"
            returnData.append({
                'paymentID': '',
                'periodLength': leasePeriod,
                'status': lateIcon,
                'amount': amt,
                'message': "Error: it seems a payment was skipped.\nPlease contact support."
            })
            nextPayDate = getDateXPeriodsLater(nextPayDate, leasePeriod, 1)
            print("NPD: ",nextPayDate)

        # check if the current lease changed
        if pWDR.leaseID != prevLeaseID:
            # There's a new lease
            leasePeriod = getBasePeriodPayment(pWDR.leaseID)
            baseAmount = leasePeriod['paymentAmount']
            print ("LeasePeriodInfo: ",leasePeriod)
            leasePeriod = leasePeriod['rentPeriod']
            prevLeaseID = pWDR.leaseID
            print (baseAmount)

        #recording the payment information (Starts at the oldest and ends with the newest) 
        amount = float(pWDR.amountReceived)
        if pWDR.paymentStatus == 1:
            #if the payment is 'upcoming' calculate it based on current date
            amount = calculatePayment(pWDR, uDate)
            print("CalculatedPayment", amount)
            amount = amount['paymentAmount']
            print ("NewCalculatedAmount: ", amount)
            print ("Old Amount: ", baseAmount)
            # amount = baseAmount
        comment = str(pWDR.statusOfPayment.statusName).capitalize()+" payment of ${0:,.2f}".format(float(amount))
        if pWDR.dateReceived:
            comment += " on {}".format(pWDR.dateReceived.strftime("%b %-d, %Y"))
        comment += "\n\n Click to Edit"
        returnData.append({
            'paymentID': pWDR.paymentID,
            'periodLength': leasePeriod,
            'status': pWDR.statusOfPayment.statusIcon,
            'amount': float(amount),
            'message': comment
        })
        nextPayDate = getDateXPeriodsLater(thisPayDate, leasePeriod, 1)
        print("NPD: ",nextPayDate)
    
    if firstPayment == None:
        # This means there aren't any pWDR: (essentially no leases/payments during that period)
        # assume month period and keep make them up until it gets up to assumed date range amount needed
        while timedelta(days = len(returnData)*30.75) < (eDate-sDate):
            returnData = [{
                'paymentID': '',
                'periodLength': 'mo',
                'status': missingIcon,
                'amount': 'No Lease',
                'message': "No lease payment found; unit assumed empty"
            }] + returnData
    else:
        # Step 2
        # let's go forward until we hit the endDate
        # leasePeriod should be defined currently as the lastPayment's lease Period
        while nextPayDate <= eDate.date():
            returnData.append({
                'paymentID': '',
                'periodLength': leasePeriod,
                'status': '',
                'amount': baseAmount,
                'message': "Estimated payment of ${0:,.2f}".format(float(baseAmount)) + ' due on %s'%(nextPayDate.strftime("%Y-%m-%d"))
            })
            nextPayDate = getDateXPeriodsLater(nextPayDate, leasePeriod, 1)

        
        # Step 3
        # let's go back until we hit the startDate
        # FUTURE: technically should redefine leasePeriod as firstPayment's lease Period
        prevPayDate = getDateOnePeriodEarlier(firstPayment.periodStartDate, leasePeriod)
        while prevPayDate >= sDate.date():
            returnData = [{
                'paymentID': '',
                'periodLength': leasePeriod,
                'status': missingIcon,
                'amount': 'No Lease',
                'message': "No lease payment found; unit assumed empty"
            }] + returnData
            prevPayDate = getDateOnePeriodEarlier(prevPayDate, leasePeriod)


    return returnData

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
        phoneNumber = filterPhoneNumber(jsonData['phoneNumber']), 
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
        phoneNumber = filterPhoneNumber(jsonData['companyPhone']),
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

def getAdminRentRollData(company, session, reqArgs, startDate, endDate, userDate):
    returnData = []
    if "propertyID" in reqArgs:
        properties = property.query.filter_by(propertyID = reqArgs["propertyID"],companyID = company.companyID).all()
    else:
        properties = property.query.filter_by(companyID = company.companyID).all()

    for prprty in properties:
        hasActiveLease = prprty.getActiveLease(userDate)
        if hasActiveLease:
            lease_i = hasActiveLease
            LPList = []
            for LPi in lease_i.leasePeople:
                if LPi.role == 'tenant':
                    LPList.append(LPi.leasePerson.firstName + " " + LPi.leasePerson.lastName)
            tenants = ", ".join(LPList)
        else: 
            tenants = "-- EMPTY --"

        
        propertyData = {
            'propertyID':       prprty.propertyID,
            'nickname':         prprty.nickname,
            'address':          prprty.fullAddress.getHouseNStreet(),
            'tenants':          tenants,
            'paymentStatuses':  getPaymentStatus(prprty, sDate = startDate, eDate = endDate, uDate = userDate),
        }


        returnData.append(propertyData)

    return returnData    
    leases = lease.query.filter(lease.terminationDate == None)
    leaseReturnList = []
    for lease_i in leases:
        fees = []
        monthlyRent = 'n/a'
        leaseFees = leaseFee.query.filter_by(leaseID = lease_i.leaseID)
        for leaseFee_i in leaseFees:
            if leaseFee_i.feeName == 'Rent':
                monthlyRent = leaseFee_i.feeAmount
            else:
                fees.append("%s: %.2f/%s"%(leaseFee_i.feeName,leaseFee_i.feeAmount,leaseFee_i.leaseFeeOccurrence.occurrencePeriod.abbreviation))
        
        leasePeriodAbbr = lease_i.periodOfLease.abbreviation
        if lease_i.moveInDate:
            if leasePeriodAbbr == 'wk':
                tD = lease_i.moveInDate + timedelta(weeks = 1)
                tD = tD.strftime("%Y-%m-%d")
            elif leasePeriodAbbr == 'mo':
                month = int(lease_i.moveInDate.strftime('%m'))+1
                year = int(lease_i.moveInDate.strftime("%Y"))
                if month >12:
                    month -= 12
                    year += 1
                tD = str(year)+"-"+str(month)+lease_i.moveInDate.strftime("-%d")
            elif leasePeriodAbbr == 'day':
                tD = (lease_i.moveInDate + timedelta(days = 1)).strftime("%Y-%m-%d")
            elif leasePeriodAbbr == 'yr':
                tD = str(int(lease_i.moveInDate.strftime("%Y"))+1)+lease_i.moveInDate.strftime("-%m-%d")
            else:
                tD = "n/a"
        else:
            tD = "n/a"
        
        LPList = []
        for LPi in lease_i.leasePeople:
            if LPi.role == 'tenant':
                LPList.append(LPi.leasePerson.firstName + " " + LPi.leasePerson.lastName)
        LnP = ", ".join(LPList)

        leasData = {
            'leaseID': lease_i.leaseID,
            'nickname': lease_i.leasedProperty.nickname,
            'address': lease_i.leasedProperty.fullAddress.getHouseNStreet(),
            'tenants': LnP,
            'monthlyRent': monthlyRent,
            'monthlyFees': "<br/>".join(fees),
            'leasePeriod': "1 "+ str(lease_i.periodOfLease.abbreviation),
            'moveInDate': lease_i.moveInDate.strftime("%Y-%m-%d"),
            'endDate': tD
        }
        leaseReturnList.append(leasData)


def createPayment(jsonData):
    
    # 1. update the payment with final details
    # 2. if the payment status is 'complete', then write the paymentItems
    # 3. if #2, then create the next payment

    createdDBItems = []

    requiredAttrs = ['leaseID', 'people', 'leaseStatus', 
                     'availableDate', 'leasePeriod', 'leaseSuccessionPeriod',
                     'fees']

    for attribute in requiredAttrs:
        if attribute not in jsonData:
            print (jsonData)
            return False, "Failed to create payment: Missing %s in jsonData"%attribute
    # if 'moveInDate' in jsonData:
    #     mID = datetime.strptime(jsonData['moveInDate'],'%Y-%m-%d')
    #     newtime = jsonData['moveInDate'][:-2]+"01"
    #     #FUTURE: Setup this to find the actual first period start date
    #     psd = datetime.strptime(newtime, "%Y-%m-%d")
    # else:
    #     mID = None
    #     psd = None

    # if 'terminationDate' not in jsonData:
    #     tD = None
    # else:
    #     tD = datetime.strptime(jsonData['terminationDate'],'%Y-%m-%d')

    #     __newPament = payment(
    #     leaseID = int(__newLease.leaseID), 
    #     periodNo = 0, 
    #     periodStartDate = psd, 
    #     dueDate = mID,
    #     paymentStatus = 1,
    #     paymentMethod = None,
    #     amountReceived = 0.0,
    #     createUser = int(jsonData['createUser']),
    #     createDate = datetime.utcnow()
    # )

    # db.session.add(__newPament)
    # db.session.commit()


def createLease(jsonData):

    # 1. make lease
    # 2. make Lease-People connection
    # 3. make leaseFees
    createdDBItems = []

    requiredAttrs = ['propertyID', 'people', 'leaseStatus', 
                     'availableDate', 'leasePeriod', 'leaseSuccessionPeriod',
                     'fees']

    for attribute in requiredAttrs:
        if attribute not in jsonData:
            print (jsonData)
            return False, "Failed to create Tenant Account: Missing %s in jsonData"%attribute
    if 'moveInDate' in jsonData:
        mID = datetime.strptime(jsonData['moveInDate'],'%Y-%m-%d')
        newtime = jsonData['moveInDate'][:-2]+"01"
        #FUTURE: Setup this to find the actual first period start date
        psd = datetime.strptime(newtime, "%Y-%m-%d")
    else:
        mID = None
        psd = None

    if 'terminationDate' not in jsonData:
        tD = None
    else:
        tD = datetime.strptime(jsonData['terminationDate'],'%Y-%m-%d')

    __newLease = lease(
        propertyID = int(jsonData['propertyID']), 
        leaseStatus = jsonData['leaseStatus'], 
        availableDate = datetime.strptime(jsonData['availableDate'],'%Y-%m-%d'), 
        moveInDate = mID,
        terminationDate = tD,
        lastPaidPeriodStartingDate = None,
        lastPeriodRemainingBalance = 0.0,
        leasePeriod=int(jsonData['leasePeriod']),
        leaseSuccessionPeriod=int(jsonData['leaseSuccessionPeriod']),
        securityDeposit = '',#float(jsonData['securityDeposit']),
        contractDocID = None if 'contractDocID' not in jsonData else jsonData['contractDocID'],
        createUser = int(jsonData['createUser']),
        createDate = datetime.utcnow()
    )

    db.session.add(__newLease)
    db.session.commit()
    createdDBItems.append(__newLease)

    __newPament = payment(
        leaseID = int(__newLease.leaseID), 
        periodNo = 0, 
        periodStartDate = psd, 
        dueDate = mID,
        paymentStatus = 1,
        paymentMethod = None,
        amountReceived = 0.0,
        createUser = int(jsonData['createUser']),
        createDate = datetime.utcnow()
    )

    db.session.add(__newPament)
    db.session.commit()
    createdDBItems.append(__newPament)

    for person in jsonData['people']:
        peopleRequirements = ['personID', 'role']
        for attribute in peopleRequirements:
            if attribute not in person:
                print ("Error writing the leasePerson", person)
                for dbItem in createdDBItems:
                    db.session.remove(dbItem)
                db.session.commit()
                return False, "Failed to create leasePerson: missing %s"%attribute
        
        __newLeasePerson = leasePerson(
            leaseID = __newLease.leaseID,
            personID = int(person['personID']),
            role = person['role']
        )
        db.session.add(__newLeasePerson)
        createdDBItems.append(__newLeasePerson)
    db.session.commit()

    # rentOccurrence = occurrence.query.filter_by(occurrence = 1).join(occurrence.occurrencePeriod).filter(name = 'month').one()
    # jsonData['fees'].append({
    #     "feeID": 4, 
    #     "feeAmount": float(jsonData['monthlyRent']), 
    #     "occurrence": 1, 
    #     "startAfterLength": 0, 
    #     "startAfterPeriod": 3
    #     })

    for fee in jsonData['fees']:
        feeRequirements = ['feeID', 'feeAmount','occurrence','startAfterLength','startAfterPeriod']
        for attribute in feeRequirements:
            if attribute not in fee:
                print ("Error writing the leaseFee", fee)
                # Delete all the previously created DB items for this function execution
                for dbItem in createdDBItems:
                    db.session.remove(dbItem)
                db.session.commit()
                return False, "Failed to create Tenant Account: Missing %s in jsonData"%attribute
        feeName = feeType.query.filter_by(feeID = int(fee['feeID'])).one().feeName
        __newLeaseFee = leaseFee(
            leaseID = __newLease.leaseID,
            feeID = int(fee['feeID']),
            feeName = feeName,
            feeAmount = float(fee['feeAmount']),
            occurrence = int(fee['occurrence']),
            startAfterLength = int(fee['startAfterLength']),
            startAfterPeriod = int(fee['startAfterPeriod']),
            createUser = fee['createUser'],
            createDate = datetime.utcnow(),
        )

        db.session.add(__newLeaseFee)
        createdDBItems.append(__newLeaseFee)
        
        # __newPaymentItem = paymentItem(
        #     leaseID = __newLease.leaseID,
        #     feeID = int(fee['feeID']),
        #     feeName = feeName,
        #     feeAmount = float(fee['feeAmount']),
        #     occurrence = int(fee['occurrence']),
        #     startAfterLength = int(fee['startAfterLength']),
        #     startAfterPeriod = int(fee['startAfterPeriod']),
        #     createUser = fee['createUser'],
        #     createDate = datetime.utcnow(),
        # )

        # db.session.add(__newLeaseFee)
        # createdDBItems.append(__newLeaseFee)


    db.session.commit()

    return True, __newLease
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
        phoneNumber = filterPhoneNumber(jsonData['phoneNumber']), 
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

        # 'POST' request comes from the HomeEasy webserver (form post gets processed on the webserver and requests the API to save the data).
        print("Request: ", request)
        if request.remote_addr != '20.228.226.251' and request.remote_addr != '127.0.0.1' and request.remote_addr != '24.101.69.174':
            return {'status': 403, 'message': 'Forbidden: You cannot view this request'}, 403

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
                elif dataItem == 'emailAddress':
                    accountJsonData['emailAddress'] = str(requestData[dataItem]).lower()
                else:
                    accountJsonData[dataItem] = requestData[dataItem]
            
        if len(requiredItems) >=1:
            return {'status': 400, 'message': "Missing necessary information to create a new user", "missingField(s)": requiredItems}, 400
        similarUsers = userAccount.query.filter_by(emailAddress = accountJsonData['emailAddress']).all()
        if len(similarUsers)>=1:
            return {'status': 403, 'message': "This username already exists: '%s'"%str(accountJsonData['emailAddress'])}, 403
        wasCreated, result = newLandlordAccount(accountJsonData)
        if wasCreated:
            return {'status': 201, 'message':'Success: User account has been created!','userID':str(result.userID)}, 201#,'redirectURL':'./home'}
        else:
            print ( dir(result))
            return {'status': 400, 'message':'Failed to save','error':str(result),'traceback':result.args,'redirectURL':'#'}, 400

class getRentRoll(Resource):
    
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
                    if 'viewStartDate' in request.args and 'viewEndDate' in request.args:
                        try:
                            sDate = datetime.strptime(request.args['viewStartDate'], "%Y-%m-%d")
                            eDate = datetime.strptime(request.args['viewEndDate'], "%Y-%m-%d")
                            uDate = datetime(year= int(request.args['year']), month= int(request.args['month']), day=int(request.args['day']))
                            # print ("TYPE uDATE: ", type(eDate), type(uDate))
                            if (eDate-sDate)>timedelta(days=366):
                                return {'status': 401, 'message': 'Error: Date range should be less than 1 year.'}, 401
                        except:
                            return {'status': 401, 'message': 'Incorrect Date Format: viewStartDate and viewEndDate use yyyy-mm-dd format, Year, month, and day must be included as integers as well'}, 401
                    else:
                        return {'status': 401, 'message': 'Missing Input: You must specify the viewStartDate and viewEndDate'}, 401
                    cRPs = sessn.sessionUser.companyRolePerson
                    if len(cRPs) >0:
                        returnData = {'status': 200, 'data': []}
                        for cRP in cRPs:
                            cmpny = cRP.associatedCompany
                            print ("company(s): ", cmpny)
                            returnData['data'].append({
                                'companyID':cmpny.companyID,
                                'companyName':cmpny.companyName,
                                'rentRoll': getAdminRentRollData(company = cmpny, session = sessn, reqArgs = request.args, startDate = sDate, endDate = eDate, userDate = uDate)
                            })
                        
                        return returnData, returnData['status']
                    else:
                        sessionOrComment = "Error with your account"
                elif accntType == 'tenant':
                    # FUTURE: Tenant user get /rent function goes here
                    data = {
                        'status': 200,
                        'name': "Hello",
                        'id': "World"
                    }
                    return data, data['status']
                else:
                    sessionOrComment = "Insufficient Authority to view this data"
            return {'status': 401, 'message': 'Unauthorized: %s'%(sessionOrComment)}, 401
        else:
            return {'status': 401, 'message': 'Unauthorized: You must be logged in to view this request'}, 401

    # def post(self):
    #     if 'sessionID' in request.cookies:
    #         isValid, sessionInfo = isSessionValid(request.cookies['sessionID'])
            
    #         if isValid:
    #             #Now check if the person is authorized
    #             print(sessionInfo.sessionUser)
    #             rows=[]
    #             appPaymentStatuses = paymentStatus.query.filter_by().all()
    #             for status in appPaymentStatuses:
    #                 rows.append({
    #                     'statusID':    status.statusID,
    #                     'statusName':  status.statusName,
    #                     'isCompleted': status.isCompleted!=b''#, 'big')
    #                 })
    #             return {'response': 200, 'data': rows}, 200
    #         return {'status': 401, 'message': 'Unauthorized: %s'%(sessionInfo)}, 401
    #     else:
    #         return {'message': 'Unauthorized: You must be logged in to view this request'}, 401

class userPayment(Resource):
    
    def get(self):
        
        if 'sessionID' in request.args:
            if 'paymentID' in request.args:
                ipAddress = request.remote_addr
                # print (ipAddress)
                # ipAddress = request.headers['ipAddress']
                isValid, sessionOrComment = isSessionValid(request.args['sessionID'], ipAddress=ipAddress)
                if isValid:
                    sessn = sessionOrComment
                    accntType = sessn.sessionUser.accountAuthority.typeName
                    
                    if accntType in ['landlord'] or 'admin' in accntType.lower():
                        cmpnys = []
                        cRPs = sessn.sessionUser.companyRolePerson
                        if len(cRPs) >0:
                            for cRP in cRPs:
                                cmpnys.append(cRP.associatedCompany.companyID)
                            print ("company(s): ", cmpnys)


                            pamnts = db.session.query(payment).filter(payment.paymentID == str(request.args['paymentID'])).all()
                            if pamnts:
                                for pamnt in pamnts:
                                    if pamnt.paymentsLease.leasedProperty.companyID in cmpnys:
                                        responseObj = {'status': 200, 'data': {}}
                                        LPList = []
                                        for LPi in pamnt.paymentsLease.leasePeople:
                                            if LPi.role == 'tenant':
                                                LPList.append(LPi.leasePerson.firstName + " " + LPi.leasePerson.lastName)
                                        tenants = ", ".join(LPList)
                                        
                                        fees = []
                                        processedBy = []
                                        processedDate = []
                                        paymentDate = ''
                                        if pamnt.statusOfPayment.isCompleted != b'':
                                            for paymentItem in pamnt.paymentItems:
                                                fees.append({
                                                    'paymentItemID': paymentItem.paymentItemID,
                                                    'dueDate': paymentItem.dueDate.strftime("%Y-%m-%d"),
                                                    'itemName': paymentItem.itemName,
                                                    'leaseFeeID': paymentItem.leaseFeeID,
                                                    'qty': paymentItem.qty,
                                                    'amountPaid': paymentItem.amountPaid
                                                })
                                                if paymentItem.paymentItemCreator.accountPerson.lastName not in processedBy:
                                                    processedBy.append(paymentItem.paymentItemCreator.accountPerson.lastName)
                                                if paymentItem.createDate.strftime("%Y-%m-%d") not in processedDate:
                                                    processedDate.append(paymentItem.createDate.strftime("%Y-%m-%d"))
                                                paymentDate = pamnt.dateReceived.strftime("%Y-%m-%d")
                                        else:
                                            # the payment isn't completed so return the fees ordered by the fee order
                                            leaseFees4Lease = db.session.query(leaseFee).filter_by(leaseID = pamnt.paymentsLease.leaseID).join(leaseFee.leaseFeeType).order_by(feeType.displayOrder).all()
                                            for leaseFeeItem in leaseFees4Lease:
                                                fees.append({
                                                    'paymentItemID': '',
                                                    'dueDate': pamnt.dueDate.strftime("%Y-%m-%d"),
                                                    'itemName': leaseFeeItem.feeName,
                                                    'leaseFeeID': leaseFeeItem.leaseFeeID,
                                                    'qty': "",
                                                    'amountPaid': ''
                                                })
                                        processedBy = ", ".join(processedBy)
                                        processedDate = ", ".join(processedDate)
                                        

                                        data = {
                                            'paymentID': pamnt.paymentID,
                                            'tenant': tenants,
                                            'address': pamnt.paymentsLease.leasedProperty.fullAddress.getHouseNStreet(),
                                            'paymentStatus': pamnt.paymentStatus,
                                            'paymentMethod': pamnt.paymentMethod,
                                            'paymentDate': paymentDate,
                                            'fees': fees,
                                            'processedBy': processedBy,
                                            'processedDate': processedDate
                                        }
                                        
                                        responseObj['data'] = data

                                        return responseObj, responseObj['status']
                                    else:
                                        sessionOrComment = "No Payment with the paymentID = %s for your company"%(pamnt.paymentID)
                            else:
                                sessionOrComment = "No Payment with that paymentID"
                        else:
                            sessionOrComment = "No Payment with that paymentID for your company"
                    elif accntType == 'tenant':
                        # FUTURE: Tenant user get /payment-history function goes here
                        data = {
                            'status': 200,
                            'name': "Hello",
                            'id': "World"
                        }
                        return data, data['status']
                else:
                    sessionOrComment = "Insufficient Authority to view this data"
                return {'status': 401, 'message': 'Unauthorized: %s'%(sessionOrComment)}, 401
            else:
                return {'status': 401, 'message': 'Missing Input: You must specify the paymentID'}, 401

        else:
            return {'status': 401, 'message': 'Unauthorized: You must be logged in to view this request'}, 401


class paymentOptions(Resource):

    def get(self):
        # 'GET' request comes directly from the webpage on a client's browser. - No Authentication required here
        returnData = {'status': 200, 
                      'paymentStatus': [], #[{'statusID': int, 'statusName': str}], 
                      'paymentMethods': [], #[{'methodID': int, 'methodName': str}], 
                    }
        
        payStatuses = paymentStatus.query.filter().all()
        payStatusList = []
        for payStatus in payStatuses:
            returnData['paymentStatus'].append({
                'statusID': payStatus.statusID,
                'statusName': payStatus.statusName
            })

        paymentMethods = paymentMethod.query.filter().all()
        paymentMethodList = []
        for paymentMethod_i in paymentMethods:
            returnData['paymentMethods'].append({
                'methodID': paymentMethod_i.methodID,
                'methodName': paymentMethod_i.methodName
            })

        return returnData, returnData['status']
        

class adminLeases(Resource):

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
                        cmpny = cRP[0].associatedCompany
                        print ("company(s): ", cmpny)

                        leases = lease.query.filter(lease.terminationDate == None).join(lease.leasedProperty).filter(property.companyID == cmpny.companyID).all()
                        leaseReturnList = []
                        for lease_i in leases:
                            fees = []
                            monthlyRent = 'n/a'
                            leaseFees = leaseFee.query.filter_by(leaseID = lease_i.leaseID)
                            for leaseFee_i in leaseFees:
                                if leaseFee_i.feeName == 'Rent':
                                    monthlyRent = leaseFee_i.feeAmount
                                else:
                                    fees.append("%s: %.2f/%s"%(leaseFee_i.feeName,leaseFee_i.feeAmount,leaseFee_i.leaseFeeOccurrence.occurrencePeriod.abbreviation))
                            
                            LPList = []
                            for LPi in lease_i.leasePeople:
                                if LPi.role == 'tenant':
                                    LPList.append(LPi.leasePerson.firstName + " " + LPi.leasePerson.lastName)
                            LnP = ", ".join(LPList)

                            leasData = {
                                'leaseID': lease_i.leaseID,
                                'nickname': lease_i.leasedProperty.nickname,
                                'address': lease_i.leasedProperty.fullAddress.getHouseNStreet(),
                                'tenants': LnP,
                                'monthlyRent': monthlyRent,
                                'monthlyFees': "<br/>".join(fees),
                                'leasePeriod': "1 "+ str(lease_i.periodOfLease.abbreviation),
                                'moveInDate': lease_i.moveInDate.strftime("%Y-%m-%d"),
                                'endDate': getDateXPeriodsLater(lease_i.moveInDate, lease_i.periodOfLease.abbreviation, 1).strftime("%Y-%m-%d")
                            }
                            leaseReturnList.append(leasData)

                        returnData = {'status': 200, 'leases': leaseReturnList}

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

        leaseJsonData = {}
        requiredItems = ['sessionID', 'ipAddress', 'propertyID', 'people', 'leaseStatus', 
                         'availableDate', 'moveInDate', 'leasePeriod', 'leaseSuccessionPeriod',
                         'fees']
        feeRequirements = ['feeID', 'feeAmount','occurrence','startAfterLength','startAfterPeriod']
        peopleRequirements = ['personID', 'role']

        requestData = request.get_json()
        for dataItem in requestData:
            if dataItem in requiredItems:
                requiredItems.remove(dataItem)
                if dataItem == 'people':
                    # FUTURE: Add some code to check that the personID is not already on a lease
                    for person in requestData[dataItem]:
                        for personComp in person:
                            if personComp in peopleRequirements:
                                peopleRequirements.remove(personComp)
                        if len(peopleRequirements)>=1:
                            return {'status': 400, 'message': "Missing Tenant detail(s)", "problemObject": person, "missingField(s)": peopleRequirements}, 400
                    leaseJsonData['people'] = requestData[dataItem]
                if dataItem == 'fees':
                    for fee_i in requestData[dataItem]:
                        for feeComp in fee_i:
                            if feeComp in feeRequirements:
                                feeRequirements.remove(feeComp)
                        if len(feeRequirements)>=1:
                            return {'status': 400, 'message': "Missing fee detail(s)", "problemObject": fee_i, "missingField(s)": feeRequirements}, 400
                    leaseJsonData['fees'] = requestData[dataItem]
                elif dataItem in ['sessionID', 'ipAddress']:
                    pass
                else:
                    leaseJsonData[dataItem] = requestData[dataItem]
            
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
                
                leaseJsonData['companyID'] = sessn.sessionUser.companyRolePerson[0].associatedCompany.companyID
                for fee in leaseJsonData['fees']:
                    fee['createUser'] = sessn.userID
                leaseJsonData['createUser']=sessn.userID

                wasCreated, reslt = createLease(leaseJsonData)
                if wasCreated:
                    return {'status': 201, 'message':'Success: Lease has been created!','leaseID':str(reslt.leaseID)}, 201#,'redirectURL':'./home'}
                else:
                    print ( dir(reslt))
                    return {'status': 500, 'message':'Failed to create new lease','error':str(reslt),'redirectURL':'#'}, 500
            else:
                return {'status': 403, 'message': 'Forbidden: Insufficient authority to add a property'}, 403
        return {'status': 401, 'message': 'Unauthorized: %s'%(sessionOrComment)}, 401


class leaseOptions(Resource):
    def get(self):
        # 'GET' request comes directly from the webpage on a client's browser for creating leases.
        if 'sessionID' in request.args:
            ipAddress = request.remote_addr
            isValid, sessionOrComment = isSessionValid(request.args['sessionID'], ipAddress=ipAddress)
            if isValid:
                sessn = sessionOrComment
                accntType = sessn.sessionUser.accountAuthority.typeName

                # print(sessn.sessionUser.accountAuthority.typeName)
                if accntType in ['landlord'] or 'admin' in accntType.lower():
                    #Now check if the person is authorized
                    cRP = sessn.sessionUser.companyRolePerson
                    if len(cRP) >0:
                        returnData = {'status': 200, 
                                      'people': [], #[{'personID': int, 'name': str, 'emailAddress': str}], 
                                      'properties': [], #[{'propertyID': int, 'nickname': str, 'address': str}], 
                                      'feeTypes':[], #[{'feeID': int, 'name': str = 'Pet Fee', 'description': str, 'defaultPrice': int, 'defaultOccurrence': int = occurrenceID}], 
                                      'occurrences':[],#[{'occurrenceID': int, 'name': str = '/day'}], 
                                      'periods':[]#[{'periodID': int, 'name': str = 'day'}], 
                                      }
                        people = [] # {"personID":"", "name":""}
                        cmpny = cRP[0].associatedCompany
                        print ("company(s): ", cmpny)

                        # Find a list of landlord users for the company who can make people
                        companyUsers = companyRole.query.filter_by(companyID = cmpny.companyID).all()
                        for companyUser in companyUsers:
                            # get a list of the people created by the company's landlord users
                            peopleCreatedByUserWOLease = personDetail.query.filter_by(setPersonID = companyUser.userID).join(personDetail.associatedDetail).filter_by(propertyName='creator').filter(~ exists().where(leasePerson.personID==personDetail.personID)).all()
                            for personCreatedByUser in peopleCreatedByUserWOLease:
                                # print ("personCreatedByUser: ", personCreatedByUser)
                                people.append(personCreatedByUser.associatedPerson)
                        print ("PeopleList: ", people)
                        # Now get a list the people details
                        for person_i in people:
                            # Now build return data
                            addedDetails = {}
                            # print("RElated Person: ", person_i)
                            # print("RElated PersonDetails: ", person_i.relatedPersonDetails)
                            for additionalDetail in person_i.relatedPersonDetails:
                                if additionalDetail.associatedDetail.propertyName != 'creator':
                                    addedDetails[additionalDetail.associatedDetail.propertyName] = additionalDetail.propertyValue
                            data = {
                                'personID':     person_i.personID,
                                'name':    person_i.firstName + " " + addedDetails['middleName'][0] + ". " + person_i.lastName,
                                'emailAddress': person_i.personsAccount[0].emailAddress,
                            }
                            returnData['people'].append(data)
                        # Get the list of properties without active leases
                        unrentedProperties = property.query.filter_by(companyID = cmpny.companyID).join(property.propertyLeases, isouter=True).filter(lease.availableDate == None,lease.terminationDate == None).all()
                        for unrentedProperty in unrentedProperties:
                            data = {
                                'propertyID': unrentedProperty.propertyID,
                                'nickname': unrentedProperty.nickname,
                                'address': unrentedProperty.fullAddress.getHouseNStreet()
                            }
                            returnData['properties'].append(data)
                        appFeeTypes = feeType.query.filter_by().order_by(feeType.displayOrder.asc()).all()
                        for appFeeType in appFeeTypes:
                            data = {
                                'feeID': appFeeType.feeID, 
                                'name': appFeeType.feeName,
                                'description': appFeeType.description,
                                'defaultPrice': str(appFeeType.defaultPrice),
                                'defaultOccurrenceID': appFeeType.defaultOccurrence
                                }
                            returnData['feeTypes'].append(data)
                        appOccurrences = occurrence.query.filter_by().all()
                        for appOccurrence in appOccurrences:
                            if appOccurrence.occurrence == 1:
                                occurrName = """/{}""".format(appOccurrence.occurrencePeriod.abbreviation)
                            else:
                                occurrName = """{}/{}""".format(appOccurrence.occurrence,appOccurrence.occurrencePeriod.abbreviation)

                            data = {
                                'occurrenceID': appOccurrence.occurrenceID, 
                                'name': occurrName,
                                }
                            returnData['occurrences'].append(data) 
                        appPeriods = period.query.filter_by().all()
                        for appPeriod in appPeriods:
                            data = {
                                'periodID': appPeriod.periodID, 
                                'name': appPeriod.name,
                                'isLeasePeriod': appPeriod.isLeasePeriod!=b''
                                }
                            returnData['periods'].append(data) 
                        # print ("ReturnData: ",returnData)
                        return returnData, returnData['status']
                    else:
                        sessionOrComment = "Error with your account"
                else:
                    sessionOrComment = "Insufficient Authority to view this data"
            return {'status': 401, 'message': 'Unauthorized: %s'%(sessionOrComment)}, 401
        else:
            return {'status': 401, 'message': 'Unauthorized: You must be logged in to view this request'}, 401


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
                                    'name':    person_i.firstName + " " + person_i.lastName,
                                    'phoneNumber':  person_i.phoneNumber,
                                    'cellPhoneNumber':  addedDetails['cellPhoneNumber'],
                                    'emailAddress': person_i.personsAccount[0].emailAddress,
                                    'DOB': addedDetails['DOB'],
                                    'cars':  addedDetails['cars'],
                                    'comments':  addedDetails['comments']
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
api.add_resource(getRentRoll, '/rent')
api.add_resource(userPayment, '/payment')
api.add_resource(paymentOptions, '/paymentOptions')

# Leases Page
api.add_resource(adminLeases, '/admin/leases')
api.add_resource(leaseOptions, '/leaseOptions')


# People
api.add_resource(adminPeople, '/admin/people')


# Properties Page
api.add_resource(adminProperties, '/admin/properties')


if __name__ == "__main__":
    app.run(debug=True)