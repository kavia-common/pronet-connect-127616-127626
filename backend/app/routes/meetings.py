from flask.views import MethodView
from flask_smorest import Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import db, Meeting
from marshmallow import Schema, fields

blp = Blueprint(
    "Meetings", "meetings", url_prefix="/meetings", description="Meetings management"
)

class MeetingSchema(Schema):
    id = fields.Int(dump_only=True)
    user_id = fields.Int()
    title = fields.String()
    scheduled_for = fields.DateTime()
    notes = fields.String()
    location = fields.String()
    status = fields.String()

class MeetingCreateSchema(Schema):
    title = fields.String(required=True)
    scheduled_for = fields.DateTime(required=True)
    notes = fields.String(required=False)
    location = fields.String(required=False)

@blp.route("/")
class MeetingsList(MethodView):
    @jwt_required()
    @blp.response(200, MeetingSchema(many=True))
    def get(self):
        """List meetings for current user."""
        user_id = get_jwt_identity()
        return Meeting.query.filter_by(user_id=user_id).all()

    @jwt_required()
    @blp.arguments(MeetingCreateSchema)
    @blp.response(201, MeetingSchema)
    def post(self, data):
        """Schedule a meeting."""
        user_id = get_jwt_identity()
        meeting = Meeting(user_id=user_id, **data)
        db.session.add(meeting)
        db.session.commit()
        return meeting

@blp.route("/<int:meeting_id>")
class MeetingItem(MethodView):
    @jwt_required()
    @blp.response(200, MeetingSchema)
    def get(self, meeting_id):
        m = Meeting.query.get_or_404(meeting_id)
        user_id = get_jwt_identity()
        if m.user_id != user_id:
            blp.abort(403, message="Forbidden.")
        return m

    @jwt_required()
    @blp.arguments(MeetingCreateSchema)
    @blp.response(200, MeetingSchema)
    def put(self, data, meeting_id):
        meeting = Meeting.query.get_or_404(meeting_id)
        user_id = get_jwt_identity()
        if meeting.user_id != user_id:
            blp.abort(403, message="Forbidden.")
        for k, v in data.items():
            setattr(meeting, k, v)
        db.session.commit()
        return meeting

    @jwt_required()
    def delete(self, meeting_id):
        meeting = Meeting.query.get_or_404(meeting_id)
        user_id = get_jwt_identity()
        if meeting.user_id != user_id:
            blp.abort(403, message="Forbidden.")
        db.session.delete(meeting)
        db.session.commit()
        return {"message": "Deleted"}
