# iReport
[![Build Status](https://travis-ci.org/ekwaro/iReport.svg?branch=challenge2)](https://travis-ci.org/ekwaro/iReport)[![Coverage Status](https://coveralls.io/repos/github/ekwaro/iReport/badge.svg?branch=challenge2)](https://coveralls.io/github/ekwaro/iReport?branch=challenge2)[![Maintainability](https://api.codeclimate.com/v1/badges/799e1be4bc2558b1c47e/maintainability)](https://codeclimate.com/github/ekwaro/iReport/maintainability)

iReporter enables
any/every citizen to bring any form of corruption to the notice of appropriate authorities and the
general public. Users can also report on things that needs government intervention

#### Getting Started
clone the project using the [link](https://github.com/ekwaro/iReport.git)
#### Prerequisites

 A browser with internet access
#### Installing
* clone the project on your local machine

##### Accessing the frontend of the application
The front-end of the application is hosted on gh pages and can be accessed from [here]( https://ekwaro.github.io/iReport/UI/home.html)

## Features
* Users can create an account and log in.
* Users can create a red-flag record (An incident linked to corruption).
* Users can create intervention record (a call for a government agency to intervene e.g
repair bad road sections, collapsed bridges, flooding e.t.c).
* Users can edit their red-flag or intervention records.
* Users can delete their red-flag or intervention records.
* Users can add geolocation (Lat Long Coordinates) to their red-flag or intervention
records .
* Users can change the geolocation (Lat Long Coordinates) attached to their red-flag or
intervention records .
* Admin can change the status of a record to either under investigation, rejected (in the
event of a false claim) or resolve (in the event that the claim has been investigated and resolved)

### Endpoints

HTTP method | Endpoint| Functionality
-------------|---------|-------------
GET|/api/v1| Welcomes Users to the application
POST|/api/v1/register| Used to register a user
POST|/api/v1/login| Used to log the user In to the application
POST|/api/v1/redflags| Used for creating redflag/intervention record
GET|/api/v1/redflags| Used to get all the red flag records created by the user
GET|/api/v1/redflags/id| Used to get specific redflag/ intervention record created by the user
PATCH|/api/v1/redflags/id/comments| Used to update comment on a specific red flag record
PATCH|/api/v1/redflags/id/location| Used to update location on a specific redflag record
DELETE|/api/v1/redflags/id| used to delete a specific red flag record


### Tools Used
 * [Flask](http://flask.pocoo.org/)
 * [Virtual Environment](https://virtualenv.pypa.io/en/stable/) - Used to create an isolated virtual environment
 * [PIP](https://pip.pypa.io/en/stable/) - A python package installer
 
 ### Deployment
 
 The API is hosted on [Heroku](https://gob.herokuapp.com/api/v1)
 
 ### Built with 
 * python/ Flask
 ### Authors
 Ekwaro Dominic

