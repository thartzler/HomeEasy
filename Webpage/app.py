from flask import Flask, render_template, url_for, request, redirect
import json
from wtforms import Form, BooleanField, StringField, PasswordField, validators

from datetime import datetime, timedelta
import secrets
from userTypes import getUser, TenantUser, Property_Manager_User, AdminUser
from DB_Object_Creator import db, Department, webSession, property

# from SessionStates import LoggedInState, LoggedOutState


# from DB_Object_Creator import 
class newUserForm(Form):
    firstName= StringField('First Name*', [validators.DataRequired(), validators.Regexp('[A-Za-z]+')])
    lastName= StringField('Last Name*', [validators.DataRequired(), validators.Regexp('[A-Za-z]+')])
    companyName= StringField('Company Name*', [validators.DataRequired(), validators.Regexp('[A-Za-z]+')])
    emailAddress= StringField('Email Address*', [validators.DataRequired()])
    houseNumber= StringField('House No.*', [validators.DataRequired()])
    streetName= StringField('Street*', [validators.DataRequired()])
    apptNo= StringField('Appt No.')
    city= StringField('City*', [validators.DataRequired()])
    state= StringField('State*', [validators.DataRequired(), validators.Regexp('[A-Z]{2}')])
    zipCode= StringField('Zip Code*', [validators.DataRequired(), validators.Regexp('[0-9]+')])
    companyPhone= StringField('Company Phone*', [validators.DataRequired()])
    phoneNumber= StringField('Personal Phone Number*', [validators.DataRequired()])
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

@app.route('/solutions')
def solutions():
    current_member = getCurrentUser(request)
    dbSolutions = Department.query.filter_by(IsSolution = 1).all()
    return render_template('solutions/index.html', headerData = current_member.headerContents, solutions = dbSolutions)

@app.route('/rent')
def rent_roll():
    current_member = getCurrentUser(request)
    userType = type(current_member)
    if userType == TenantUser:
        return render_template('unauthorized.html', headerData = current_member.headerContents, loggedIn = True)
    elif userType in [Property_Manager_User, AdminUser]:
        rentRollList = property.query.all()
        monthlist = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']
        rentRollList = []
        return render_template('admin/rent/rent_roll.html', headerData = current_member.headerContents, rentRollList = rentRollList, monthlist=monthlist)
    else:
        
        return render_template('unauthorized.html', headerData = current_member.headerContents, loggedIn = True)
    


@app.route('/login', methods = ['GET'])
def loginPage():
    current_member = getCurrentUser(request)
    if request.method == 'POST':
        current_member.Login(request.form['username'], request.form['password'])
        #user = webSession.newSession(request.form['username'], request.form['password'])
        print (current_member)
        if hasattr(current_member, 'createAnAccount'):
            return render_template('login.html', headerData = current_member.headerContents, comment = current_member.message)
        else:
            print (current_member)
            if request.args.get('goto'):
                return redirect(request.args.get('goto'))
            else:
                return redirect('/')
    # print(current_member)
    return render_template('login.html', headerData = current_member.headerContents)

@app.route('/logout')
def logoutPage():
    current_member = getCurrentUser(request)
    return render_template('logout.html', headerData = current_member.headerContents)

@app.route('/newUser',  methods = ['GET'])
def newUserPage():
    form = newUserForm(request.form)
    current_member = getCurrentUser(request)
    return render_template('newUser.html', headerData = current_member.headerContents, form=form)

# @app.route('/')
# def index():
#     content = [{'name': "Home", 'link': "/", 'pageID': "index"},{'name': "Solutions",'link': "../solutions/index.html", 'pageID': "solutions"},
#             {'name': "Product Reviews", 'link': "../product_reviews/index.html", 'pageID': "reviews"}, {'name': "About Us", 'link': "../about_us/index.html", 'pageID': "about"}]
#     return render_template('index.html', headerData = current_member.headerContents)


if __name__ == "__main__":
    app.run(debug=True)