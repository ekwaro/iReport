from flask import jsonify
incidents = [
    {
        "comment": "comments",
        "createdby": "dominic",
        "createdon": "Wed, 28 Nov 2018 04:06:50 GMT",
        "id": 1,
        "incident_type": "red-flag",
        "location": 0.11,
        "status": "draft"
    }
]


class Incident:
    def __init__(self, id, createdon, createdby, incident_type, location, status, comment):
        self.id = id
        self.createdon = createdon
        self.createdby = createdby
        self.incident_type = incident_type
        self.location = location
        self.status = status
        self.comment = comment

    @staticmethod
    def id_not_found(id):
        if id < 0 or len(incidents) < id:
            return jsonify({
                "status": 400,
                "message": "Item with the id not found"
            })


