from datetime import datetime



def get_utc_timestamp():
    return datetime.utcnow().isoformat() + "Z"

def build_event(action, request_id, author, to_branch, from_branch=None):
    return {
        "request_id": request_id,
        "author": author,
        "action": action.upper(),  # Ensure it's PUSH, PULL_REQUEST, or MERGE
        "from_branch": from_branch,
        "to_branch": to_branch,
        "timestamp": get_utc_timestamp()
    }
