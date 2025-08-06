"""
Backend business logic tests: JWT auth flows and CRUD for profile, connections, referrals, meetings, notifications.
"""
import pytest
from app import create_app, db
from app.models import User, Profile, Connection, Referral, Meeting, Notification

import datetime

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite://"
    with app.app_context():
        db.create_all()
        # Pre-populate a user
        user = User(email="alice@test.com", password_hash="hash")
        db.session.add(user)
        db.session.commit()
        yield app.test_client()
        db.drop_all()

def get_token(client):
    rv = client.post("/auth/register", json={"email": "bob@email.com", "password": "xyztest"})
    return rv.get_json()["access_token"]

def auth_header(token):
    return {"Authorization": f"Bearer {token}"}

def test_profile_crud(client):
    token = get_token(client)
    # POST (should succeed)
    rv = client.post("/profiles/", headers=auth_header(token), json={"full_name": "Bob User"})
    assert rv.status_code == 201
    prof_id = rv.get_json()["id"]
    # Duplicate POST not allowed
    rv2 = client.post("/profiles/", headers=auth_header(token), json={"full_name": "Bob User"})
    assert rv2.status_code == 409
    # GET /profiles/me
    rv3 = client.get("/profiles/me", headers=auth_header(token))
    assert rv3.status_code == 200
    # PUT updates (change business)
    rv4 = client.put("/profiles/me", headers=auth_header(token), json={"full_name": "Bob User", "business": "TechBiz"})
    assert rv4.status_code == 200
    assert rv4.get_json()["business"] == "TechBiz"

def test_connections_flow(client):
    t1 = get_token(client)
    t2 = client.post("/auth/register", json={"email": "sally@mail.com", "password": "sallypass"}).get_json()["access_token"]
    # Initiate connection (user1->user2)
    user2 = User.query.filter_by(email="sally@mail.com").first()
    rv = client.post("/connections/", headers=auth_header(t1), json={"connection_id": user2.id})
    assert rv.status_code == 201
    conn_id = rv.get_json()["id"]
    # Accept by user2
    rv2 = client.patch(f"/connections/{conn_id}", headers=auth_header(t2), json={"status": "accepted"})
    assert rv2.status_code == 200
    assert rv2.get_json()["status"] == "accepted"

def test_referral_flow(client):
    t1 = get_token(client)
    t2 = client.post("/auth/register", json={"email": "carol@biz.com", "password": "pa33w0rd"}).get_json()["access_token"]
    user2 = User.query.filter_by(email="carol@biz.com").first()
    # Send referral
    rv = client.post("/referrals/", headers=auth_header(t1), json={"referred_id": user2.id, "details": "New lead!"})
    assert rv.status_code == 201
    ref_id = rv.get_json()["id"]
    # Update status
    rv2 = client.patch(f"/referrals/{ref_id}", headers=auth_header(t1), json={"status": "closed"})
    assert rv2.status_code == 200
    assert rv2.get_json()["status"] == "closed"

def test_meeting_flow(client):
    t1 = get_token(client)
    now = datetime.datetime.utcnow() + datetime.timedelta(days=1)
    rv = client.post("/meetings/", headers=auth_header(t1),
                     json={"title": "1:1 Sync", "scheduled_for": now.isoformat()})
    assert rv.status_code == 201
    m_id = rv.get_json()["id"]
    # View meeting detail
    rv2 = client.get(f"/meetings/{m_id}", headers=auth_header(t1))
    assert rv2.status_code == 200

def test_notifications(client):
    t1 = get_token(client)
    # Post notification
    rv = client.post("/notifications/", headers=auth_header(t1), json={"message": "You have new connection."})
    assert rv.status_code == 201
    notif_id = rv.get_json()["id"]
    # Mark as read
    rv2 = client.post(f"/notifications/{notif_id}/read", headers=auth_header(t1))
    assert rv2.status_code == 200
    assert rv2.get_json()["read"] is True
