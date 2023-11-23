import datetime
from DB_Object_Creator import UserSession, Users, Session
import secrets, getpass, datetime

def make_token():
    """
    Creates a cryptographically-secure, URL-safe string
    """
    return secrets.token_urlsafe(24) 


def hash(text):
    # Temporary function for hasing the password
    return text






existingSessionID = 'C1-v1PH7_aPUfq6QPDNgD9pEJeKysimf'        # the exting session id stored in the browser cookies
validUserSession = None

# userAuth = authentication()
username = input("Please enter your username (hint: 'admin'): ").lower()

session = Session()
validUser = session.query(Users).filter_by(Username = username).all()


if len(validUser) == 1:
    user = validUser[0]

    preExistingSessions = session.query(UserSession).filter_by(username = username).all()
    if len(preExistingSessions) > 0:
        validSession = None
        for PES in preExistingSessions:
            if datetime.datetime.now() - datetime.timedelta(days=1) > PES.AuthenticationDatetime or PES.SessionID != existingSessionID:
                print ("Removing old session - ", PES)
                session.delete(PES)
            elif validUserSession is not None:
                # for some reason if there is more than 1 valid session, delete the previous valid session and mark the newly found session as valid user session
                print (validUserSession)
                session.delete(validUserSession)
                validUserSession = PES
            else:
                validUserSession = PES

        session.commit()

    if user and validUserSession:
        print ("Welcome back %s %s" % (user.firstName, user.lastName))
    else:
        attemptNo = 0
        password = hash(getpass.getpass("Please enter your password (hint: 'password'): "))
        while attemptNo <= 3 and password != user.passHash:
            print ("Incorrect password, try again...")
            password = hash(getpass.getpass("Please enter your password (hint: 'password'): "))
            attemptNo +=1


        if password == user.passHash:
            print ("Welcome %s %s" % (user.firstName, user.lastName))
            savedLoginSession = UserSession(SessionID = str(make_token()), username = str(user.Username), AuthenticationDatetime = datetime.datetime.now())
            # print (savedLoginSession)
            session.add(savedLoginSession)
            session.commit()
        else:
            print("Password entered incorrectly too many times; Please start over.")
            exit()
else:
    print ('The username entered is invalid; Please create an account to begin.')
    exit()
input ("Press any key to exit the program...")