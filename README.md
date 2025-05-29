# Webhook Receiver Backend

This repository contains a Flask backend that receives GitHub webhook events (push, pull request, merge)  
and stores them in a MongoDB database. It serves as the middle layer in a pipeline where:

**Application Flow:**  
GitHub repo (push/PR) → GitHub webhook → Flask webhook receiver → MongoDB → UI (polls MongoDB every 15 seconds)

---

## Features

- Receives GitHub webhook events:
  - Push events
  - Pull request events (opened)
  - Pull request merge events (closed & merged)
- Stores event data in MongoDB with timestamp and branch info
- Provides a REST endpoint to retrieve the latest 50 events, sorted by newest first

---

## Requirements

- Python 3.7+
- MongoDB (local or remote)
- Python packages:
  - Flask
  - Flask-PyMongo
  - Flask-CORS

---

## Setup & Run

1. Clone this repo:

```bash
git clone <your-webhook-repo-url>
cd <your-webhook-repo-directory>
