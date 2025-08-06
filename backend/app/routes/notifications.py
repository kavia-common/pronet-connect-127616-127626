from flask.views import MethodView
from flask_smorest import Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import db, Notification
from marshmallow import Schema, fields

blp = Blueprint(
    "Notifications", "notifications", url_prefix="/notifications", description="User notifications"
)

class NotificationSchema(Schema):
    id = fields.Int(dump_only=True)
    user_id = fields.Int()
    message = fields.String()
    created_at = fields.DateTime()
    read = fields.Boolean()

class NotificationCreateSchema(Schema):
    message = fields.String(required=True)

@blp.route("/")
class NotificationList(MethodView):
    @jwt_required()
    @blp.response(200, NotificationSchema(many=True))
    def get(self):
        """List notifications for current user."""
        user_id = get_jwt_identity()
        return Notification.query.filter_by(user_id=user_id).order_by(Notification.created_at.desc()).all()

    @jwt_required()
    @blp.arguments(NotificationCreateSchema)
    @blp.response(201, NotificationSchema)
    def post(self, data):
        """Push notification to the current user (or for admin/event only)."""
        user_id = get_jwt_identity()
        notif = Notification(user_id=user_id, message=data['message'])
        db.session.add(notif)
        db.session.commit()
        return notif

@blp.route("/<int:notif_id>/read")
class NotificationRead(MethodView):
    @jwt_required()
    @blp.response(200, NotificationSchema)
    def post(self, notif_id):
        notif = Notification.query.get_or_404(notif_id)
        user_id = get_jwt_identity()
        if notif.user_id != user_id:
            blp.abort(403, message="Forbidden.")
        notif.read = True
        db.session.commit()
        return notif
