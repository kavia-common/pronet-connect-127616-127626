from flask.views import MethodView
from flask_smorest import Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import db, Profile
from marshmallow import Schema, fields

blp = Blueprint(
    "Profiles", "profiles", url_prefix="/profiles", description="Profile management"
)

class ProfileSchema(Schema):
    id = fields.Int(dump_only=True)
    user_id = fields.Int(dump_only=True)
    full_name = fields.String()
    business = fields.String()
    title = fields.String()
    phone = fields.String()
    bio = fields.String()
    location = fields.String()
    linkedin = fields.String()

class ProfileCreateSchema(Schema):
    full_name = fields.String()
    business = fields.String()
    title = fields.String()
    phone = fields.String()
    bio = fields.String()
    location = fields.String()
    linkedin = fields.String()

@blp.route("/")
class ProfileList(MethodView):
    @jwt_required()
    @blp.response(200, ProfileSchema(many=True))
    def get(self):
        """Get all profiles."""
        return Profile.query.all()

    @jwt_required()
    @blp.arguments(ProfileCreateSchema)
    @blp.response(201, ProfileSchema)
    def post(self, profile_data):
        """Create profile for current user (if not exists)."""
        user_id = get_jwt_identity()
        if Profile.query.filter_by(user_id=user_id).first():
            blp.abort(409, message="Profile already exists.")
        profile = Profile(user_id=user_id, **profile_data)
        db.session.add(profile)
        db.session.commit()
        return profile

@blp.route("/me")
class MyProfile(MethodView):
    @jwt_required()
    @blp.response(200, ProfileSchema)
    def get(self):
        user_id = get_jwt_identity()
        profile = Profile.query.filter_by(user_id=user_id).first()
        if not profile:
            blp.abort(404, message="Profile not found.")
        return profile

    @jwt_required()
    @blp.arguments(ProfileCreateSchema)
    @blp.response(200, ProfileSchema)
    def put(self, profile_data):
        user_id = get_jwt_identity()
        profile = Profile.query.filter_by(user_id=user_id).first()
        if not profile:
            blp.abort(404, message="Profile not found.")
        for k, v in profile_data.items():
            setattr(profile, k, v)
        db.session.commit()
        return profile
