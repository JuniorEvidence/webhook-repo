from flask import Blueprint, request, jsonify
from . import mongo
from datetime import datetime
from .utils import build_event
from dateutil import parser

webhook_bp = Blueprint("webhook", __name__)

def get_utc_timestamp():
    return datetime.utcnow().isoformat() + "Z"

@webhook_bp.route("/webhook", methods=["POST"])
def webhook():
    event_type = request.headers.get("X-GitHub-Event")
    data = request.json
    print("\n📦 Received Webhook Event:")
    print(data)
    timestamp = get_utc_timestamp()
    event = None

    if event_type == "push":
        author = data.get("pusher", {}).get("name")
        to_branch = data.get("ref", "").split("/")[-1]
        request_id = data.get("after")  # Commit hash

        event = event = build_event("PUSH", request_id, author, to_branch)

    elif event_type == "pull_request":
        action = data.get("action")
        pr = data.get("pull_request", {})
        author = pr.get("user", {}).get("login")
        from_branch = pr.get("head", {}).get("ref")
        to_branch = pr.get("base", {}).get("ref")
        request_id = str(pr.get("id"))

        if action == "opened":
            event = {
                "request_id": request_id,
                "author": author,
                "action": "PULL_REQUEST",
                "from_branch": from_branch,
                "to_branch": to_branch,
                "timestamp": timestamp
            }
        elif action == "closed" and pr.get("merged"):
            event = {
                "request_id": request_id,
                "author": author,
                "action": "MERGE",
                "from_branch": from_branch,
                "to_branch": to_branch,
                "timestamp": timestamp
            }

    if event:
        mongo.db.events.insert_one(event)
        return jsonify({"status": "stored", "event": event}), 200

    return jsonify({"status": "received"}), 200

@webhook_bp.route("/events", methods=["GET"])
def get_events():
    events = list(mongo.db.events.find({}, {"_id": 0}).sort("_id", -1))
    formatted = []

    for event in events:
        try:
            dt = parser.isoparse(event["timestamp"])
            readable_ts = dt.strftime("%d %b %Y - %I:%M %p UTC")
        except Exception:
            readable_ts = event["timestamp"]

        if event["action"] == "PUSH":
            message = f'{event["author"]} pushed to {event["to_branch"]} on {readable_ts}'
        elif event["action"] == "PULL_REQUEST":
            message = f'{event["author"]} submitted a pull request from {event["from_branch"]} to {event["to_branch"]} on {readable_ts}'
        elif event["action"] == "MERGE":
            message = f'{event["author"]} merged branch {event["from_branch"]} to {event["to_branch"]} on {readable_ts}'
        else:
            message = "Unknown event"

        formatted.append({
    "message": message,
    "action": event["action"]
})

    return jsonify(formatted)
