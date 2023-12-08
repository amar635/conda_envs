
from flask_smorest import Blueprint, abort
from flask.views import MethodView
from flask_jwt_extended import jwt_required

from cdmsapp.schemas import PlainParticipantSchema
from cdmsapp.models import ParticipantModel


blp = Blueprint("Participants", "participants", description="Operations on participants")

@blp.route("/register/participant")
class InsertParticipant(MethodView):
    @blp.arguments(PlainParticipantSchema)
    def post(self, participant_data):
        if ParticipantModel.find_by_mobilenumber(mobile=participant_data['mobilenumber']):
            abort(400, "Mobile Number already exists")
        
        participant = ParticipantModel(
            fullname = participant_data['fullname'],
            designation = participant_data['designation'],
            email = participant_data['email'],
            mobilenumber = participant_data['mobilenumber'],
            state = participant_data['state'],
            district = participant_data['district'],
            block = participant_data['block'],
            grampanchayat = participant_data['grampanchayat']
        )

        participant.save_to_db()

        return {"message":"Participant registered successfully"}, 201 

@blp.route('/modify/participant')
def UpdateParticipant(MethodView):
    @blp.arguments(PlainParticipantSchema)
    def post(self, participant_data):
        if not ParticipantModel.find_by_mobilenumber(mobile=participant_data['mobilenumber']).first():
            participant = ParticipantModel(
                fullname = participant_data['fullname'],
                designation = participant_data['designation'],
                email = participant_data['email'],
                mobilenumber = participant_data['mobilenumber'],
                state = participant_data['state'],
                district = participant_data['district'],
                block = participant_data['block'],
                grampanchayat = participant_data['grampanchayat']
            )
            # participant.update_to_db()
        else:
            abort(400, "Participant does not exists")

@blp.route("/participant/<int:participant_id>", methods=["GET"])
class User(MethodView):
    """
    This resource can be useful when testing our Flask app.
    We may not want to expose it to public users, but for the
    sake of demonstration in this course, it can be useful
    when we are manipulating data regarding the users.
    """

    @blp.response(200, PlainParticipantSchema)
    @jwt_required(refresh=True)
    def get(self, participant_id):
        participant = ParticipantModel.find_by_id(participant_id)
        if not participant:
            abort(404, message="Participant not found.")
        return participant

    def delete(self, user_id):
        participant = ParticipantModel.find_by_id(user_id)
        if not participant:
            abort(404, message="Participant not found.")
        participant.delete_from_db()
        return {"message": "Participant deleted."}, 200     


# @blp.route('/delete/participant')

# @blp.route('/get/all/paticipants')

# @blp.route('get/participant')

