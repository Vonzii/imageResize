
import base64
import json
import os
from google.auth import jwt
import google.oauth2.id_token
import pyrebase
from flask import Flask, request, jsonify
from google.auth.transport import requests

firebase_request_adapter = requests.Request()

import image

"""config = {
  "apiKey": "AIzaSyCgXzxKEx9aX8X3W5RcW12ogBtOp2mn_Fg",
  "authDomain": "carbide-ego-367216.firebaseapp.com",
"databaseURL": "https://databaseName.firebaseio.com",
  "projectId": "carbide-ego-367216",
  "storageBucket": "carbide-ego-367216.appspot.com",
  "messagingSenderId": "521778265240",
  "appId": "1:521778265240:web:a2995a7d779269ea8fa4ed",
  "measurementId": "G-NE4CH1FRYV"
}"""

config= {
  "apiKey": "AIzaSyC2zPWX_-MEBd9qCAOQ4V7qjMWV2-fyMMw",
  "authDomain": "minireddit-c45c6.firebaseapp.com",
  "projectId": "minireddit-c45c6",
  "storageBucket": "minireddit-c45c6.appspot.com",
  "messagingSenderId": "911213281913",
  "appId": "1:911213281913:web:1ec0ceecbaf8f27dac4aa8"
};

app = Flask(__name__)


@app.route("/", methods=["POST"])
def index():
    print("Get connection\n")
    auth_header = request.headers.get("Authorization")
    if auth_header:
        auth_type, creds = auth_header.split(" ", 1)
        if auth_type.lower() == "bearer":
            try:
                claims = google.oauth2.id_token.verify_firebase_token(
                    creds, firebase_request_adapter)
                print(f"{claims}")
            except ValueError as exc:
                msg = "error Authorization"
                print(f"error: {msg}, {exc}")
                return f"Bad Request: {msg}, {exc}", 400
        else:
            msg = "error Authorization"
            print(f"error: {msg}")
            return f"Bad Request: {msg}", 400
    else:
        msg = "error no Authorization found in header"
        print(f"error: {msg}")
        return f"Bad Request: {msg}", 400       

    envelope = request.get_json()
    print(f"Find Json\n")
    if not envelope:
        msg = "no Pub/Sub message received"
        print(f"error: {msg}")
        return f"Bad Request: {msg}", 400

    print(f"Find Pub/Sub message\n")
    if not isinstance(envelope, dict) or "message" not in envelope:
        msg = "invalid Pub/Sub message format"
        print(f"error: {msg}")
        return f"Bad Request: {msg}", 400

    pubsub_message = envelope["message"]
    print(f"try to decode\n")
    if isinstance(pubsub_message, dict) and "data" in pubsub_message:
        try:
            print(f"Decode base64\n")
            data = json.loads(base64.b64decode(pubsub_message["data"]).decode())

        except Exception as e:
            msg = (
                "Invalid Pub/Sub message: "
                "data property is not valid base64 encoded JSON"
            )
            print(f"error: {e}")
            return f"Bad Request: {msg}", 400

        # Validate the message is a Cloud Storage event.
        if not data["name"] or not data["bucket"]:
            msg = (
                "Invalid Cloud Storage notification: "
                "expected name and bucket properties"
            )
            print(f"error: {msg}")
            return f"Bad Request: {msg}", 400

        try:
            image.resize_images(data, creds, claims)
            return ("", 204)

        except Exception as e:
            print(f"error: {e}")
            return ("", 500)

    return ("", 500)

@app.route("/gettoken", methods=["POST"])
def gettoken():
        
    firebase = pyrebase.initialize_app(config)

    auth = firebase.auth()
    user = auth.sign_in_with_email_and_password("azrael1206@googlemail.com",'1qay2wsx!QAY"WSX')
    if user:
        print(user)
        return jsonify(user)
    else:
        return ("Error authentication", 500)

@app.route("/gettoken2", methods=["POST"])
def gettoken2():
        
    firebase = pyrebase.initialize_app(config)

    auth = firebase.auth()
    user = auth.sign_in_with_email_and_password("test2@test.com",'12345678')
    if user:
        print(user)
        return jsonify(user)
    else:
        return ("Error authentication", 500)

if __name__ == "__main__":
    PORT = int(os.getenv("PORT")) if os.getenv("PORT") else 8080

    app.run(host="127.0.0.1", port=PORT, debug=True)
