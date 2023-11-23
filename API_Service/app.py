from flask import Flask, jsonify, render_template, url_for, request, redirect
from flask_restful import Api, Resource
import json
# from wtforms import Form, BooleanField, StringField, PasswordField, validators

# from datetime import datetime, timedelta
# import secrets
# from userTypes import UserMaker
# from DB_Object_Creator import db, Department, webSession, property

# from SessionStates import LoggedInState, LoggedOutState


# from DB_Object_Creator import 
# class newUserForm(Form):
#     firstName= StringField('First Name*', [validators.DataRequired(), validators.Regexp('[A-Za-z]+')])
#     lastName= StringField('Last Name*', [validators.DataRequired(), validators.Regexp('[A-Za-z]+')])
#     companyName= StringField('Company Name*', [validators.DataRequired(), validators.Regexp('[A-Za-z]+')])
#     email= StringField('Email Address*', [validators.DataRequired()])
#     address= StringField('Address*', [validators.DataRequired()])
#     city= StringField('City*', [validators.DataRequired()])
#     state= StringField('State*', [validators.DataRequired(), validators.Regexp('[A-Z]{2}')])
#     zipCode= StringField('Zip Code*', [validators.DataRequired(), validators.Regexp('[0-9]+')])
#     phone= StringField('Phone Number*', [validators.DataRequired()])
#     password= PasswordField('Password*', [
#             validators.DataRequired(),\
#             validators.EqualTo('password_confirm', message='Passwords must match!')\
#         ])
#     password_confirm= PasswordField('Verify Password*', [validators.DataRequired()])



app = Flask(__name__)

api = Api(app)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///HHS.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# db.init_app(app)





# current_member = UserMaker().MakeUser()

# current_state = LoggedOutState()

# @app.route('/', methods = ['GET'])
class rentRoll(Resource):

    def get(self):
        data = {
            'name': "Hello",
            'id': "World"
        }
        return (data)
    # return render_template('index.html', headerData = current_member.headerContents)

api.add_resource(rentRoll, '/rent')


if __name__ == "__main__":
    app.run(debug=True)