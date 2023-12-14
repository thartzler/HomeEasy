from flask import Flask, render_template, url_for, request, redirect, make_response
import json

from datetime import datetime, timedelta
import secrets
from userTypes import getUser, TenantUser, Property_Manager_User, AdminUser,LoggedOutUser
from DB_Object_Creator import db, Department, webSession, property

# from SessionStates import LoggedInState, LoggedOutState



app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///HHS.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)



def getCurrentUser(req: request):
    if req:
        ipAddress = req.remote_addr
        sessionID = req.cookies.get('sessionID')
        if sessionID:
            return getUser(sessionID = sessionID, ipAddress = ipAddress)
    return getUser()

# current_member = getCurrentUser(request)

# current_state = LoggedOutState()

@app.route('/')
def index():
    current_member = getCurrentUser(request)
    return render_template('index.html', headerData = current_member.headerContents)

@app.route('/login', methods = ['GET', 'POST'])
def loginPage():
    current_member = getCurrentUser(request)
    if request.method == 'POST':
        current_member = current_member.Login(request.form['username'], request.form['password'], request.remote_addr)
        #user = webSession.newSession(request.form['username'], request.form['password'])
        print (current_member)
        if type(current_member) == LoggedOutUser:#[Property_Manager_User, AdminUser]:
            # highlight the field that has the incorrect data, and refresh the page.
            return render_template('login.html', headerData = current_member.headerContents, comment = current_member.message, username = request.form['username'])
        else:
            if request.args.get('goto'):
                resp = make_response(redirect(request.args.get('goto')))
            else:
                resp = make_response(redirect('/rent'))
            
            resp.set_cookie('sessionID', current_member.userSession)
            return resp
    # print(current_member)
    else:
        if type(current_member) in [Property_Manager_User, AdminUser]:
            return redirect('/rent')
        else:
            return render_template('login.html', headerData = current_member.headerContents)

@app.route('/newUser', methods = ['GET', 'POST'])
def newUserPage():
    current_member = getCurrentUser(request)
    if request.method == 'GET':
        return current_member.getNewLandlordPage(request)
    else:
        resp = current_member.newLandlord(request)
        return resp, resp['status']

@app.route('/logout')
def logoutPage():
    
    current_member = getCurrentUser(request)
    current_member = current_member.Logout()
    resp = make_response(render_template('logout.html', headerData = current_member.headerContents))
    resp.set_cookie('sessionID','', expires = 0)
    return resp

@app.route('/rent')
def rent_roll():
    current_member = getCurrentUser(request)
    print ('currentMember: ', current_member)
    userType = type(current_member)
    print ("userType: ", userType)
    if userType == TenantUser:
        return render_template('unauthorized.html', headerData = current_member.headerContents, loggedOut = True)
    elif userType in [Property_Manager_User, AdminUser]:
        rentRollList = property.query.all()
        monthlist = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']
        rentRollList = []
        return render_template('admin/rent_roll.html', headerData = current_member.headerContents, rentRollList = rentRollList, monthlist=monthlist)
    else:
        
        return render_template('unauthorized.html', headerData = current_member.headerContents, loggedOut = True)
    
@app.route('/leases')
def leases():
    current_member = getCurrentUser(request)
    return current_member.getLeasesPage(request)

@app.route('/people', methods = ['GET', 'POST'])
def people():
    current_member = getCurrentUser(request)
    if request.method == 'GET':
        return current_member.getPeoplePage(request)
    else:
        resp = current_member.savePerson(request)
        print (resp)
        return resp, resp['status']

@app.route('/properties', methods = ['GET', 'POST'])
def properties():
    current_member = getCurrentUser(request)
    if request.method == 'GET':
        return current_member.getPropertiesPage(request)#render_template('admin/properties.html', headerData = current_member.headerContents)
    else:
        resp = current_member.saveProperty(request)
        print (resp)
        return resp, resp['status']


if __name__ == "__main__":
    app.run(debug=True)