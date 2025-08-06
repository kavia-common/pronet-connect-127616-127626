"""
Backend authentication route tests using Flask and pytest.
Covers registration, login, token issuance, and error scenarios.
"""
import pytest
from app import create_app, db
from app.models import User
from werkzeug.security import check_password_hash

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite://"  # In-memory test DB
    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.drop_all()

def register(client, email="foo@bar.com", password="12345678"):
    return client.post("/auth/register", json={"email": email, "password": password})

def login(client, email="foo@bar.com", password="12345678"):
    return client.post("/auth/login", json={"email": email, "password": password})

def test_register_and_login(client):
    rv = register(client)
    assert rv.status_code == 201
    data = rv.get_json()
    assert "access_token" in data

    rv = login(client)
    assert rv.status_code == 200
    data = rv.get_json()
    assert "access_token" in data

def test_double_registration(client):
    rv1 = register(client)
    assert rv1.status_code == 201
    rv2 = register(client)
    assert rv2.status_code == 409  # Already registered

def test_login_invalid(client):
    register(client)
    rv = login(client, password="wrongpass")
    assert rv.status_code == 401

def test_user_model_password_hash(client):
    email = "bar@baz.com"
    password = "verysecret"
    register(client, email, password)
    user = User.query.filter_by(email=email).first()
    assert user is not None
    assert check_password_hash(user.password_hash, password)
