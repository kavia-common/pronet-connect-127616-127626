from flask.views import MethodView
from flask_smorest import Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import db, Connection
from marshmallow import Schema, fields

blp = Blueprint(
    "Connections", "connections", url_prefix="/connections", description="Member connections"
)

class ConnectionSchema(Schema):
    id = fields.Int(dump_only=True)
    user_id = fields.Int()
    connection_id = fields.Int()
    status = fields.Str()
    created_at = fields.DateTime()

class ConnectionRequestSchema(Schema):
    connection_id = fields.Int(required=True)

@blp.route("/")
class ConnectionList(MethodView):
    @jwt_required()
    @blp.response(200, ConnectionSchema(many=True))
    def get(self):
        """List all connections for current user."""
        user_id = get_jwt_identity()
        conns = Connection.query.filter(
            (Connection.user_id==user_id) | (Connection.connection_id==user_id)
        ).all()
        return conns

    @jwt_required()
    @blp.arguments(ConnectionRequestSchema)
    @blp.response(201, ConnectionSchema)
    def post(self, data):
        """Request connection to another member."""
        user_id = get_jwt_identity()
        other_id = data["connection_id"]
        if Connection.query.filter_by(user_id=user_id, connection_id=other_id).first():
            blp.abort(409, message="Already requested or connected.")
        conn = Connection(user_id=user_id, connection_id=other_id, status="pending")
        db.session.add(conn)
        db.session.commit()
        return conn

@blp.route("/<int:conn_id>")
class ConnectionItem(MethodView):
    @jwt_required()
    @blp.response(200, ConnectionSchema)
    def get(self, conn_id):
        conn = Connection.query.get_or_404(conn_id)
        return conn

    @jwt_required()
    @blp.arguments({"status": fields.String()}, location="json")
    @blp.response(200, ConnectionSchema)
    def patch(self, update, conn_id):
        """Accept or reject a connection request."""
        conn = Connection.query.get_or_404(conn_id)
        user_id = get_jwt_identity()
        # Only recipient can accept/reject
        if conn.connection_id != user_id:
            blp.abort(403, message="Not allowed.")
        if update.get("status") not in ("accepted", "rejected"):
            blp.abort(400, message="Invalid status value.")
        conn.status = update["status"]
        db.session.commit()
        return conn
