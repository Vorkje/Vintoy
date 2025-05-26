from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import login_required, current_user
from .models import db, Bid, User, Auction
from datetime import datetime, timedelta

main = Blueprint('main', __name__)

def anonymize_name(name):
    # Example: "John Doe" -> "Jd"
    parts = name.split()
    if len(parts) >= 2:
        return parts[0][0] + parts[1][0]
    return name[:2]

@main.route('/')
def index():
    auction = Auction.query.first()
    if not auction:
        return "No auction available."

    bids = Bid.query.filter_by(auction_id=auction.id).order_by(Bid.time.desc()).all()

    # Prepare bids with anonymized user names and count bids per user
    user_bid_count = {}
    anon_bids = []
    for bid in bids:
        anon_name = anonymize_name(bid.user.name)
        user_bid_count[anon_name] = user_bid_count.get(anon_name, 0) + 1
        anon_bids.append({
            "name": anon_name,
            "amount": bid.amount,
            "time": bid.time
        })

    return render_template('index.html', auction=auction, bids=anon_bids, user_bid_count=user_bid_count)

@main.route('/bid', methods=['POST'])
@login_required
def place_bid():
    auction = Auction.query.first()
    if not auction or not auction.active:
        flash("No active auction.")
        return redirect(url_for('main.index'))

    # Anti-snipe: if last bid was less than 5 minutes ago, extend auction end time
    last_bid = Bid.query.filter_by(auction_id=auction.id).order_by(Bid.time.desc()).first()
    now = datetime.utcnow()

    min_increment = auction.min_increment
    current_bid = auction.current_bid or auction.starting_bid

    # Get user max auto-bid from form (optional)
    try:
        max_auto_bid = float(request.form.get('max_auto_bid', 0))
    except:
        max_auto_bid = 0

    new_bid_amount = float(request.form.get('bid_amount', 0))

    if new_bid_amount < current_bid + min_increment:
        flash(f"Bid must be at least {min_increment} higher than current bid.")
        return redirect(url_for('main.index'))

    # Create new bid by user
    new_bid = Bid(user_id=current_user.id, auction_id=auction.id, amount=new_bid_amount, time=now)
    db.session.add(new_bid)

    # Auto-bid logic: check other users’ max auto-bids and outbid if needed
    all_auto_bids = {}  # {user_id: max_auto_bid}
    for bid in Bid.query.filter_by(auction_id=auction.id).all():
        # You would store max_auto_bid per user in DB ideally; here simplified
        pass  # implement storage in DB for production

    # Anti-snipe: extend auction if bid placed in last 5 minutes
    if last_bid and (auction.end_time - now) < timedelta(minutes=5):
        auction.end_time = now + timedelta(minutes=5)
        flash("Auction time extended due to last minute bid!")

    # Update current bid in auction
    auction.current_bid = new_bid_amount
    auction.current_winner_id = current_user.id

    db.session.commit()

    flash("Bid placed successfully!")
    return redirect(url_for('main.index'))

# Admin routes and other logic would go here...
