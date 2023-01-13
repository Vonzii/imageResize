
import base64
import json
import os
from google.auth import jwt
import google.oauth2.id_token
import pyrebase
from flask import Flask, request, jsonify
from flask_cors import CORS
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
CORS(app)


@app.route("/", methods=["POST"])
def index():
    auth_header = request.headers.get("Authorization")
    if auth_header:
        auth_type, creds = auth_header.split(" ", 1)
        if auth_type.lower() == "bearer":
            try:
                claims = google.oauth2.id_token.verify_firebase_token(
                    creds, firebase_request_adapter)
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

    json = request.get_json()
    if not json:
        msg = "no json received"
        print(f"error: {msg}")
        return f"Bad Request: {msg}", 400
    return image.resize_images(json, creds, claims)


if __name__ == "__main__":
    PORT = int(os.getenv("PORT")) if os.getenv("PORT") else 8080

    app.run(host="127.0.0.1", port=PORT, debug=True)
