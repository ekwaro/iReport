users = [{
    "firstname":"di",
    "lastname":"dom",
    "othernames":"p",
    "email":"ddd",
    "phoneNumber":"234frrgyy",
    "username":"dominic",
    "password":"12345678"

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




