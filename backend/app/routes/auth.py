from flask.views import MethodView
from flask_smorest import Blueprint
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from app.models import db, User
from marshmallow import Schema, fields, validate

blp = Blueprint(
    "Auth", "auth", url_prefix="/auth", description="Authentication endpoints"
)

class RegisterSchema(Schema):
    email = fields.Email(required=True, description="User email")
    password = fields.String(required=True, load_only=True, validate=validate.Length(min=6))

class LoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True, load_only=True)

class TokenSchema(Schema):
    access_token = fields.String(description="JWT token")

def get_user_by_email(email):
    return User.query.filter_by(email=email).first()

@blp.route("/register")
class Register(MethodView):
    """Register a new user."""
    @blp.arguments(RegisterSchema)
    @blp.response(201, TokenSchema)
    def post(self, reg_data):
        if get_user_by_email(reg_data["email"]):
            blp.abort(409, message="Email already registered.")
        user = User(
            email=reg_data["email"],
            password_hash=generate_password_hash(reg_data["password"])
        )
        db.session.add(user)
        db.session.commit()
        access_token = create_access_token(identity=user.id)
        return {"access_token": access_token}

@blp.route("/login")
class Login(MethodView):
    """User login."""
    @blp.arguments(LoginSchema)
    @blp.response(200, TokenSchema)
    def post(self, login_data):
        user = get_user_by_email(login_data["email"])
        if not user or not check_password_hash(user.password_hash, login_data["password"]):
            blp.abort(401, message="Invalid email or password.")
        access_token = create_access_token(identity=user.id)
        return {"access_token": access_token}
