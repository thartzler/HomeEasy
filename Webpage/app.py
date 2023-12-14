from flask import Flask, render_template, url_for, request, redirect, make_response
import json
from wtforms import Form, BooleanField, StringField, PasswordField, validators

from datetime import datetime, timedelta
import secrets
from userTypes import getUser, TenantUser, Property_Manager_User, AdminUser,LoggedOutUser
from DB_Object_Creator import db, Department, webSession, property

# from SessionStates import LoggedInState, LoggedOutState


# from DB_Object_Creator import 
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

@app.route('/newUser',  methods = ['GET'])
def newUserPage():
    form = newUserForm(request.form)
    current_member = getCurrentUser(request)
    return render_template('newUser.html', headerData = current_member.headerContents, form=form)

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

@app.route('/people')
def people():
    current_member = getCurrentUser(request)
    return current_member.getPeoplePage(request)

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