from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True)

class AuctionItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    description = db.Column(db.Text)
    image = db.Column(db.String(300))
    starting_bid = db.Column(db.Float)
    min_increment = db.Column(db.Float)
    end_time = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean, default=True)

class Bid(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    auction_id = db.Column(db.Integer, db.ForeignKey('auction_item.id'))
    amount = db.Column(db.Float)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class AutoBid(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    auction_id = db.Column(db.Integer, db.ForeignKey('auction_item.id'))
    max_bid = db.Column(db.Float)
    current_bid = db.Column(db.Float, default=0.0)

class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    auction_id = db.Column(db.Integer, db.ForeignKey('auction_item.id'))
    is_paid = db.Column(db.Boolean, default=False)