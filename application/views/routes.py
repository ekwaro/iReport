from flask import Blueprint, request, jsonify
from flask_jwt_extended import (create_access_token)
from flask.views import MethodView
import datetime

from ..models.usermodel import users, User
import re
from werkzeug.security import generate_password_hash, check_password_hash

auth_blueprint = Blueprint('views', __name__)


class FirstPage(MethodView):
    def get(self):
        response_object = {
            "Message": "You are welcome to iReport webpage",
            "status_code": 200
        }

        return jsonify(response_object)


class RegisterUser(MethodView):
    def post(self):
        data = request.get_json()
        id = len(users) + 1
        firstname = data.get('firstname')
        lastname = data.get('lastname')
        othernames = data.get('othernames')
        email = data.get('email')
        phonenumber = data.get('phoneNumber')
        username = data.get('username')
        password = data.get('password')
        registered = datetime.datetime.utcnow()
        isAdmin = False

        User.validate_user_input(firstname, "firstname must be a word and must be filled in")
        User.validate_user_input(lastname, "lastname must be a word and must be filled in")
        User.validate_user_input(othernames, "othernames must be a word")
        User.validate_user_input(email, "email must be filled in")

        email_regex = re.compile(r'''(
        [a-zA-Z0-9._%+-]+ # username
        @         # @ sign
        [a-zA-Z0-9.-]+ # domain name
        (\.[a-zA-Z]{2,4})# dot-something

        )''', re.VERBOSE)
        valid_email = email_regex.search(email)
        if not valid_email:
            return jsonify({
                "status": 400,
                "Message": "email must be of the form (username@domain.something)"
            }), 400

        for user in users:
            if user['email'] == email:
                return jsonify({
                    "status": 200,
                    "error": "email already exists"
                })

        User.validate_user_input(phonenumber, "Enter a valid phone number")

        if len(str(phonenumber)) != 12:
            return jsonify({
                "status": 400,
                "error": "Make sure the phone number is 12 digits"
            }), 400

        phone = re.compile(r'''(

            ((\d{3}|(\d{3}))? # area code
            (\s|-|\.)? # separator
            (\d{3})# first three digit groups
            (\s|-|\.) # separator
            (\d{4})# last four digit groups
            ))''', re.VERBOSE)
        valid_phone_number = phone.search(phonenumber)
        if not valid_phone_number:
            return jsonify({
                'status': 400,
                'error': "Enter valid phone number eg(256 *** ****) or (256-***-****) or(256.***.****)"
            }), 400

        User.validate_user_input(username, "Username must be filled and must be a string")

        for user in users:
            if user['username'] == username:
                return jsonify({
                    "status": 204,
                    "error": "User name already exists"
                }), 204

        if not password or len(password) < 8:
            return jsonify({
                "status": 400,
                "error": "Password must be filled and must be atleast 8 characters"
            }), 400

        user = User(id, firstname, lastname, othernames, email, phonenumber, username, password, registered, isAdmin)
        json_data = dict(
            id=user.id,
            firstname=user.firstname,
            lastname=user.lastname,
            othernames=user.othernames,
            email=user.email,
            phonenumber=user.phonenumber,
            username=user.username,
            password=generate_password_hash(user.password, method='sha256'),
            registered=user.registered,
            isAdmin=isAdmin
        )
        users.append(json_data)

        responseObject = {
            "status": 201,
            "data": [{
                "id": id,
                "message": "registered successfully"
            }
            ],
            "user": json_data,
            "users": users
        }
        return jsonify(responseObject), 201

class LoginUser(MethodView):
    def post(self):
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        User.validate_user_login(username, "username is required")
        User.validate_user_login(password, "Password cannot be empty")

        for person in users:
            print(users)
            print(check_password_hash(person['password'], password))
            print(person['username'] == username)
            if person['username'] == username and check_password_hash(person['password'], password):
                print(users)
                access_token = create_access_token(username)
                response = {
                    "status": 200,
                    "data": [access_token]
                }
                print(users)
                return jsonify(response), 200

        return jsonify({"status": 404, "error": "Invalid username or password"}), 404



register_firstpage = FirstPage.as_view('firstpage_api')
auth_blueprint.add_url_rule('/api/v1', view_func=register_firstpage, methods=['GET'])

register_user = RegisterUser.as_view('register_api')
auth_blueprint.add_url_rule('/api/v1/register', view_func=register_user, methods=['POST'])

register_login = LoginUser.as_view('login_api')
auth_blueprint.add_url_rule('/api/v1/login', view_func=register_login, methods=['POST'])


