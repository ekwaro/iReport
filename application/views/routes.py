from flask import Blueprint, jsonify, request, make_response, abort
from flask_jwt_extended import (create_access_token)
from flask.views import MethodView
import datetime
from ..models.usermodel import users, User
import re

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

        if firstname == '' or type(firstname) is int:
            abort(make_response(jsonify({"status": 400,
                                         "error": "firstname must be a word and must be filled in"
                                         }), 400))

        if lastname == '' or type(lastname) is int:
            abort(make_response(jsonify({"status": 400,
                                         "error": "lastname must be a word and must be filled in"
                                         }), 400))

        if type(othernames) is int:
            abort(make_response(jsonify({"status": 400,
                                         "error": "othernames must be a word"
                                         }), 400))

        if email == '' or type(email) is int:
            abort(make_response(jsonify({"status": 400,
                                         "error": "email must be filled in"
                                         }), 400))

        email_regex = re.compile(r'''(
        [a-zA-Z0-9._%+-]+ # username
        @         # @ sign
        [a-zA-Z0-9.-]+ # domain name
        (\.[a-zA-Z]{2,4})# dot-something

        )''', re.VERBOSE)
        valid_email = email_regex.search(email)
        if not valid_email:
            abort(make_response(jsonify({
                "status": 400,
                "Message": "email must be of the form (username@domain.something)"
            })))

        for user in users:
            if user['email'] == email:
                abort(make_response(jsonify({
                    "status": 200,
                    "error": "email already exists"
                })))

        if phonenumber == '' or type(phonenumber) is int:
            abort(make_response(jsonify({
                "status": 400,
                "error": "Enter a valid phone number"
            }), 400))

        if len(str(phonenumber)) != 12:
            abort(make_response(jsonify({
                "status": 400,
                "error": "Make sure the phone number is 12 digits"
            }), 400))

        phone = re.compile(r'''(

            ((\d{3}|(\d{3}))? # area code
            (\s|-|\.)? # separator
            (\d{3})# first three digit groups
            (\s|-|\.) # separator
            (\d{4})# last four digit groups
            ))''', re.VERBOSE)
        valid_phone_number = phone.search(phonenumber)
        if not valid_phone_number:
            abort(make_response(jsonify({
                'status': 400,
                'error': "Enter valid phone number eg(256 *** ****) or (256-***-****) or(256.***.****)"
            }), 400))

        if username == '' or type(username) is int:
            abort(make_response(jsonify({
                "status": 400,
                "error": "Username must be filled and must be a string"
            }), 400))

        for user in users:
            if user['username'] == username:
                abort(make_response(jsonify({
                    "status": 204,
                    "error": "User name already exists"
                }), 204))

        if not password or len(password) < 8:
            abort(make_response(jsonify({
                "status": 400,
                "error": "Password must be filled and must be atleast 8 characters"
            }), 400))

        user = User(id, firstname, lastname, othernames, email, phonenumber, username, password, registered, isAdmin)
        json_data = dict(
            id=user.id,
            firstname=user.firstname,
            lastname=user.lastname,
            othernames=user.othernames,
            email=user.email,
            phonenumber=user.phonenumber,
            username=user.username,
            password=user.password,
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
        if not username:
            response_object = {
                "status": 400,
                "error": "username is required"
            }
            abort(make_response(jsonify(response_object), 400))
        if not password:
            response_object = {
                "status": 400,
                "error": "Password cannot be empty"
            }
            abort(make_response(jsonify(response_object), 400))

        for person in users:
            if person['username'] == username or person['password'] == password:
                access_token = create_access_token(username)
                response = {
                    "status": 200,
                    "data": [access_token]
                }
                return jsonify(response), 200

            else:
                abort(make_response(jsonify({"status": 404, "error": "Invalid username or password"}), 404))


register_firstpage = FirstPage.as_view('firstpage_api')
auth_blueprint.add_url_rule('/api/v1', view_func=register_firstpage, methods=['GET'])

register_user = RegisterUser.as_view('register_api')
auth_blueprint.add_url_rule('/api/v1/register', view_func=register_user, methods=['POST'])

register_login = LoginUser.as_view('login_api')
auth_blueprint.add_url_rule('/api/v1/login', view_func=register_login, methods=['POST'])
