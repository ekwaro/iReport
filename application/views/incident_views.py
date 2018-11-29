from flask_jwt_extended import jwt_optional, jwt_required, get_jwt_identity
from flask import Blueprint, request, jsonify, make_response, abort
from flask.views import MethodView
import datetime
from ..models.incident import incidents, Incident
incident_blueprint = Blueprint('view', __name__)
statuses = ("draft", "resolved", "rejected","under investigation")
incident_types = ("red-flag", "investigation")
data = []


class Welcome(MethodView):
    def get(self):
        response_object = {
            "status": 200,
            "Message": "Welcome To The IREPORTER WELCOME PAGE"
        }
        return jsonify(response_object), 200

    @jwt_required
    def post(self):
        data = request.get_json()
        id = len(incidents) + 1
        createdOn = datetime.datetime.utcnow()
        createdBy = get_jwt_identity()
        incident_type = data.get('Incident_type')
        location = data.get('location')
        status = data.get('status')
        comment = data.get('comment')

        user = Incident(id, createdOn, createdBy, incident_type, location, status, comment)
        if user.incident_type == '' or user.incident_type is int or user.incident_type not in incident_types:
            abort(make_response(jsonify({
                "Status": 400,
                "Message": "Incident_type must be either a red flag or Intervention record "
            }), 400))

        if user.location == '' or type(user.location) is not float:
            abort(make_response(jsonify({
                "status": 400,
                "Message": "location must be filled and must be a number of the form 1.0000"
            }), 400))

        if user.status not in statuses:
            abort(make_response(jsonify({
                "status": 400,
                "Message": "status must be either (draft, resolved, rejected,under investigation)"
            }), 400))

        if type(user.comment) is int:
            abort(make_response(jsonify({
                "Message": "Comment must be a sentence",
                "status": 400
            }), 400))

        json_data = dict(
            id=user.id,
            createdOn=user.createdOn,
            createdBy=user.createdBy,
            incident_type=user.incident_type,
            location=user.location,
            status=user.status,
            comment=user.comment

        )
        incidents.append(json_data)
        return jsonify({
            "status": 201,
            "Message": "Created a red flag successfully",
            "red-flag": json_data
        }), 201

register_welcome = Welcome.as_view('welcome_api')
incident_blueprint.add_url_rule('/api/v1/welcome',
                                view_func=register_welcome,
                                methods=['GET'])

register_create_red_flag = Welcome.as_view('create_flag_api')
incident_blueprint.add_url_rule('/api/v1/redflags',
                                view_func=register_create_red_flag,
                                methods=['POST'])

