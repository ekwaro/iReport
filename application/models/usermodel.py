from werkzeug.security import generate_password_hash
from flask import abort, make_response, jsonify
users = [{
    "firstname":"di",
    "lastname":"dom",
    "othernames":"p",
    "email":"ddd",
    "phoneNumber":"234frrgyy",
    "username":"dominic",
    "password": generate_password_hash('123456789', method='sha256')

}]


class User:
    def __init__(self, id, firstname, lastname, othernames, email, phoneNumber, username, password, registered, isAdmin):
        self.id = id
        self.firstname = firstname
        self.lastname = lastname
        self.othernames = othernames
        self.email = email
        self.phonenumber = phoneNumber
        self.username = username
        self.password = password
        self.registered = registered
        self.isAdmin = isAdmin
    @staticmethod
    def validate_user_input(user_input, return_value):
        if user_input == '' or type(user_input) is int:
            abort(make_response(jsonify({
                "status": 400,
                "error": return_value
            }), 400))

    @staticmethod
    def validate_user_login(user_data, return_message):
        if user_data == '':
            abort(make_response(jsonify({
                "status": 400,
                "error": return_message
            }), 400))





