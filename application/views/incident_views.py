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
            "message": "Welcome To The IREPORTER WELCOME PAGE"
        }
        return jsonify(response_object), 200

    @jwt_required
    def post(self):
        data = request.get_json()
        id = len(incidents) + 1
        createdon = datetime.datetime.utcnow()
        createdby = get_jwt_identity()
        incident_type = data.get('incident_type')
        location = data.get('location')
        status = data.get('status')
        comment = data.get('comment')

        user = Incident(id, createdon, createdby, incident_type, location, status, comment)
        if user.incident_type == '' or user.incident_type is int or user.incident_type not in incident_types:
            abort(make_response(jsonify({
                "status": 400,
                "message": "Incident_type must be either a red flag or Intervention record "
            }), 400))

        if user.location == '' or type(user.location) is not float:
            abort(make_response(jsonify({
                "status": 400,
                "message": "location must be filled and must be a number of the form 1.0000"
            }), 400))

        if user.status not in statuses:
            abort(make_response(jsonify({
                "status": 400,
                "message": "status must be either (draft, resolved, rejected,under investigation)"
            }), 400))

        if type(user.comment) is int:
            abort(make_response(jsonify({
                "message": "Comment must be a sentence",
                "status": 400
            }), 400))

        json_data = dict(
            id=user.id,
            createdon=user.createdon,
            createdby=user.createdby,
            incident_type=user.incident_type,
            location=user.location,
            status=user.status,
            comment=user.comment

        )
        incidents.append(json_data)
        return jsonify({
            "status": 201,
            "message": "Created a red flag successfully",
            "red-flag": json_data
        }), 201

    @jwt_required
    def get(self):
        if len(incidents) <= 0:
            return jsonify({
                "Status": 404,
                "error": "No records created yet, Please create one"
            }), 404
        else:
            return jsonify({
                "status": 200,
                "Data": incidents
            }), 200


class GetSpecificRedflag(MethodView):
    @jwt_required
    def get(self, id):
        Incident.id_not_found(id)
        
        for redflag in incidents:
            if redflag['id'] == id:
                data.append(redflag)

        if len(data) > 0:
            return jsonify({
                "status": 200,
                "data": data
            }), 200

        else:
            return jsonify({
                "status": 404,
                "error": "Item with the Id not found"
            }), 404


class UpdateLocation(MethodView):
    @jwt_required
    def patch(self, redflag_id):
        update = []
        item = request.get_json()
        location = item.get('location')
        if location == '' or type(location) is not float:
            response_object = {
                "status": 404,
                "error": "Location should be a decimal number and must be filled"
            }
            return jsonify(response_object), 404
        for redflag in incidents:
            if redflag['id'] == redflag_id:
                redflag['location'] = location
                update.append(redflag['id'])

        if len(update) > 0:
            return jsonify({
                "status": 200,
                "data": update,
                "message": "Updated red-flag record’s location"
            }), 200

        else:
            return jsonify({
                "status": 204,
                "error": "Content not found"
            })


class UpdateComment(MethodView):
    @jwt_required
    def patch(self, redflag_id):
        Incident.id_not_found(redflag_id)
        update = []
        item = request.get_json()
        comment = item.get('comment')
        if comment == '' or type(comment) is int:
            response_object = {
                "status": 404,
                "error": "comment should be words and must be filled"
            }
            return jsonify(response_object), 404
        for redflag in incidents:
            if redflag['id'] == redflag_id:
                redflag['comment'] = comment
                update.append(redflag_id)

        if len(update) > 0:
            return jsonify({
                "status": 200,
                "data": update,
                "message": "Updated red-flag record’s comment"
            }), 200
        else:
            return jsonify(
                {
                    "status": 204,
                    "Message": "Content not found"
                }
            ), 204


class DeleteRedflag(MethodView):
    @jwt_required
    def delete(self, redflag_id):
        Incident.id_not_found(redflag_id)
        delete_redflag = []
        for redflag in incidents:
            if redflag['id'] == redflag_id:
                incidents.remove(redflag)
                delete_redflag.append(redflag_id)

        if len(delete_redflag) > 0:
            response_object = {
                "status": 200,
                "id": delete_redflag
            }
            return jsonify(response_object), 200
        else:
            return jsonify({
                "status": 404,
                "error": "Content not found"
            }), 404


register_welcome = Welcome.as_view('welcome_api')
incident_blueprint.add_url_rule('/api/v1/welcome',
                                view_func=register_welcome,
                                methods=['GET'])

register_create_red_flag = Welcome.as_view('create_flag_api')
incident_blueprint.add_url_rule('/api/v1/redflags',
                                view_func=register_create_red_flag,
                                methods=['POST'])

register_get_all_redflags = Welcome.as_view('get_all_redflags_api')
incident_blueprint.add_url_rule('/api/v1/redflags',
                                view_func=register_get_all_redflags,
                                methods=['GET'])

register_get_a_single_redflag = GetSpecificRedflag.as_view('get_single_red_flag')
incident_blueprint.add_url_rule('/api/v1/redflags/<int:id>',
                                view_func=register_get_a_single_redflag,
                                methods=['GET'])

register_update_location = UpdateLocation.as_view('update_location_api')
incident_blueprint.add_url_rule('/api/v1/<int:redflag_id>/locations',
                                view_func=register_update_location,
                                methods=['PATCH']
                                )

register_update_comment = UpdateComment.as_view('update_comment_api')
incident_blueprint.add_url_rule('/api/v1/redflags/<int:redflag_id>/comments',
                                view_func=register_update_comment,
                                methods=['PATCH'])

register_delete_red_flag = DeleteRedflag.as_view('delete_redflag_api')
incident_blueprint.add_url_rule('/api/v1/redflags/<int:redflag_id>',
                                view_func=register_delete_red_flag,
                                methods=['DELETE'])

