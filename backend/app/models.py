import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

db = SQLAlchemy()

# PUBLIC_INTERFACE
class User(db.Model):
    """User model - authentication and base info."""
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    profile = relationship("Profile", uselist=False, back_populates="user")
    connections_from = relationship("Connection", foreign_keys='Connection.user_id', back_populates="requester")
    connections_to = relationship("Connection", foreign_keys='Connection.connection_id', back_populates="recipient")
    referrals_given = relationship("Referral", foreign_keys='Referral.referrer_id', back_populates="referrer")
    referrals_received = relationship("Referral", foreign_keys='Referral.referred_id', back_populates="referred")
    meetings = relationship("Meeting", back_populates="user")
    notifications = relationship("Notification", back_populates="user")

# PUBLIC_INTERFACE
class Profile(db.Model):
    """Profile model - extended user information."""
    __tablename__ = "profiles"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, unique=True)
    full_name = db.Column(db.String(80))
    business = db.Column(db.String(120))
    title = db.Column(db.String(80))
    phone = db.Column(db.String(40))
    bio = db.Column(db.Text)
    location = db.Column(db.String(120))
    linkedin = db.Column(db.String(240))
    user = relationship("User", back_populates="profile")

# PUBLIC_INTERFACE
class Connection(db.Model):
    """Connection model - member connections."""
    __tablename__ = "connections"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey("users.id"), nullable=False)
    connection_id = db.Column(db.Integer, ForeignKey("users.id"), nullable=False)
    status = db.Column(db.String(30), default="pending")  # pending, accepted, rejected
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    requester = relationship("User", foreign_keys=[user_id], back_populates="connections_from")
    recipient = relationship("User", foreign_keys=[connection_id], back_populates="connections_to")

# PUBLIC_INTERFACE
class Referral(db.Model):
    """Referral model - business referrals."""
    __tablename__ = "referrals"
    id = db.Column(db.Integer, primary_key=True)
    referrer_id = db.Column(db.Integer, ForeignKey("users.id"), nullable=False)
    referred_id = db.Column(db.Integer, ForeignKey("users.id"), nullable=False)
    details = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(30), default="open")  # open, closed, lost
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    referrer = relationship("User", foreign_keys=[referrer_id], back_populates="referrals_given")
    referred = relationship("User", foreign_keys=[referred_id], back_populates="referrals_received")

# PUBLIC_INTERFACE
class Meeting(db.Model):
    """Meeting model - meeting records between members."""
    __tablename__ = "meetings"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey("users.id"), nullable=False)
    title = db.Column(db.String(120), nullable=False)
    scheduled_for = db.Column(db.DateTime, nullable=False)
    notes = db.Column(db.Text, nullable=True)
    location = db.Column(db.String(120))
    status = db.Column(db.String(30), default="scheduled")  # scheduled, completed, canceled
    user = relationship("User", back_populates="meetings")

# PUBLIC_INTERFACE
class Notification(db.Model):
    """Notification model - notifications sent to users."""
    __tablename__ = "notifications"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey("users.id"), nullable=False)
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    read = db.Column(db.Boolean, default=False)
    user = relationship("User", back_populates="notifications")
