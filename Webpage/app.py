from flask import Flask, render_template, url_for, request, redirect
import json, requests
from wtforms import Form, BooleanField, StringField, PasswordField, validators

from datetime import datetime, timedelta
import secrets
from userTypes import UserMaker
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




def getCurrentMember(req: request):
    ipAddress = req.remote_addr
    reqData = req.get_json()
    if hasattr(req.headers, 'sessionID'):
        sessionID = req.headers['sessionID']
        url = 'api.hartzlerhome.solutions/getAuthority'
        payload = json.dumps({"sessionID": sessionID, "ipAddress": ipAddress})
        headers = {
        'Content-Type': 'application/json'
        }
        response = requests.request("GET",url, headers=headers, data=payload)
        return response
    return None
current_member = UserMaker().MakeUser()

# current_state = LoggedOutState()

@app.route('/')
def index():
    return render_template('index.html', headerData = current_member.headerContents)

@app.route('/solutions')
def solutions():
    dbSolutions = Department.query.filter_by(IsSolution = 1).all()
    return render_template('solutions/index.html', headerData = current_member.headerContents, solutions = dbSolutions)

@app.route('/rent_roll')
def rent_roll():
    current_member = getCurrentMember(request)
    rentRollList = property.query.all()
    monthlist = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']
    rentRollList = []
    return render_template('admin/rent/rent_roll.html', headerData = current_member.headerContents, rentRollList = rentRollList, monthlist=monthlist)

@app.route('/login', methods = ['GET', 'POST'])
def loginPage():
    if request.method == 'POST':
        global current_member
        current_member = current_member.Login(request.form['username'], request.form['password'])
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

@app.route('/logout.html')
def logoutPage():
    global current_member
    current_member = UserMaker().MakeUser()
    print (current_member.headerContents)
    return render_template('logout.html', headerData = current_member.headerContents)

@app.route('/newUser',  methods = ['GET', 'POST'])
def newUserPage():
    form = newUserForm(request.form)
    # print(request.form)
    if request.method == 'POST' and form.validate():
        print("Valid Form")
        user = webSession
        user.newSession(request.form['email'], request.form['password'])
        if type(user) is list and len(user)>1:
            return render_template('newUser.html', headerData = current_member.headerContents, comment = user[1])
        else:
            return redirect('/')
    # content[4]={'name': "Log In", 'link': "/login.html", 'pageID': "login"}
    return render_template('newUser.html', headerData = current_member.headerContents, form=form)

# @app.route('/')
# def index():
#     content = [{'name': "Home", 'link': "/", 'pageID': "index"},{'name': "Solutions",'link': "../solutions/index.html", 'pageID': "solutions"},
#             {'name': "Product Reviews", 'link': "../product_reviews/index.html", 'pageID': "reviews"}, {'name': "About Us", 'link': "../about_us/index.html", 'pageID': "about"}]
#     return render_template('index.html', headerData = current_member.headerContents)

@app.route('/api/admin/rent/roll')
def getRentRoll():
    if request.headers.get('username'):
        
        content = [{'name': "Home", 'link': "/", 'pageID': "index"},{'name': "Solutions",'link': "../solutions/index.html", 'pageID': "solutions"},
                {'name': "Product Reviews", 'link': "../product_reviews/index.html", 'pageID': "reviews"}, {'name': "About Us", 'link': "../about_us/index.html", 'pageID': "about"}]
        return render_template('index.html', headerData = current_member.headerContents)
    else:
        return render_template('404.html', headerData = current_member.headerContents, title = '404'), 404



if __name__ == "__main__":
    app.run(debug=True)