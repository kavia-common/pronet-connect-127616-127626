from flask.views import MethodView
from flask_smorest import Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import db, Referral
from marshmallow import Schema, fields

blp = Blueprint(
    "Referrals", "referrals", url_prefix="/referrals", description="Business referrals"
)

class ReferralSchema(Schema):
    id = fields.Int(dump_only=True)
    referrer_id = fields.Int()
    referred_id = fields.Int()
    details = fields.String()
    status = fields.String()
    created_at = fields.DateTime()

class ReferralCreateSchema(Schema):
    referred_id = fields.Int(required=True)
    details = fields.String(required=True)

@blp.route("/")
class ReferralList(MethodView):
    @jwt_required()
    @blp.response(200, ReferralSchema(many=True))
    def get(self):
        user_id = get_jwt_identity()
        # Both referrals you gave and received
        return Referral.query.filter(
            (Referral.referrer_id == user_id) | (Referral.referred_id == user_id)
        ).all()

    @jwt_required()
    @blp.arguments(ReferralCreateSchema)
    @blp.response(201, ReferralSchema)
    def post(self, data):
        user_id = get_jwt_identity()
        new_ref = Referral(
            referrer_id=user_id,
            referred_id=data["referred_id"],
            details=data["details"]
        )
        db.session.add(new_ref)
        db.session.commit()
        return new_ref

@blp.route("/<int:ref_id>")
class ReferralItem(MethodView):
    @jwt_required()
    @blp.response(200, ReferralSchema)
    def get(self, ref_id):
        return Referral.query.get_or_404(ref_id)

    @jwt_required()
    @blp.arguments({"status": fields.String()}, location="json")
    @blp.response(200, ReferralSchema)
    def patch(self, update, ref_id):
        """Mark referral as closed, lost, etc."""
        ref = Referral.query.get_or_404(ref_id)
        if update.get("status") and update["status"] in ("open", "closed", "lost"):
            ref.status = update["status"]
            db.session.commit()
        else:
            blp.abort(400, message="Invalid status value.")
        return ref
