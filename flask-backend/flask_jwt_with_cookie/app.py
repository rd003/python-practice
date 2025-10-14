from flask import Flask, jsonify, request
import jwt
from flask_jwt_extended import (
    JWTManager, create_access_token, create_refresh_token,
    jwt_required, get_jwt_identity,get_jwt, set_access_cookies, unset_jwt_cookies
)
from dotenv import load_dotenv
import os
from datetime import datetime,timedelta,timezone

SECRET_KEY = os.getenv("JWT_SECRET_KEY")
user = {
    'username':'rd003',
    'password':'123',
    'role':'admin'
}

load_dotenv()

def create_tokens(username,additional_claims):
    access_token = create_access_token(identity=username,additional_claims=additional_claims)
    refresh_token = create_refresh_token(identity=username,additional_claims=additional_claims)
    return access_token, refresh_token

app = Flask(__name__)

# --- Configuration ---
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
app.config["JWT_TOKEN_LOCATION"] = ["headers","cookies"] # token location both headers and cookies
app.config["JWT_COOKIE_SECURE"] = os.getenv("JWT_COOKIE_SECURE", "False").lower() in ("true", "1", "yes")
app.config["JWT_COOKIE_SAMESITE"] = os.getenv("JWT_COOKIE_SAMESITE", "Lax")
app.config["JWT_COOKIE_CSRF_PROTECT"] = True
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=int(os.getenv("JWT_ACCESS_TOKEN_EXPIRES", "2")))
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(hours=int(os.getenv("JWT_REFRESH_TOKEN_EXPIRES", "1")))

jwt = JWTManager(app)


# Using an `after_request` callback, we refresh any token that is within 30
# minutes of expiring. Change the timedeltas to match the needs of your application.
@app.after_request
def refresh_expiring_jwts(response):
    try:
        exp_timestamp = get_jwt()["exp"]
        now = datetime.now(timezone.utc)
        target_timestamp = datetime.timestamp(now + timedelta(minutes=30))
        if target_timestamp > exp_timestamp:
            access_token = create_access_token(identity=get_jwt_identity())
            set_access_cookies(response, access_token)
        return response
    except (RuntimeError, KeyError):
        # Case where there is not a valid JWT. Just return the original response
        return response

@app.route("/api/login", methods=['POST'])
def login():
    try:
        data = request.get_json()
        if not data or 'username' not in data or 'password' not in data:
            return jsonify({'error':'validation error'}), 400
        
        username = user['username']
        password = user['password']
        role = user['role']
        
        if data['username'] != username or data['password'] != password:
            return jsonify({'error':'invalid credentials'}), 401
        
        additional_claims = {"role": role}
        access_token, refresh_token = create_tokens(username,additional_claims)
        
        response = jsonify({
            "message": "Login successful",
            "access_token": access_token,
            "refresh_token": refresh_token
        })
        set_access_cookies(response, access_token)
        return response
    except Exception as e:
        print(f"Login error: {str(e)}")  # Debug print
        return jsonify({'error': str(e)}), 500


# We are using the `refresh=True` options in jwt_required to only allow
# refresh tokens to access this route.
@app.route("/api/refresh",methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    try:
        identity = get_jwt_identity()
        access_token = create_access_token(identity=identity)
        return jsonify(access_token=access_token)
    except Exception as ex:
        print(f"====> refresh error: {str(ex)}")
        return jsonify({'error':str(ex)})

@app.route("/api/greet",methods=['get'])
@jwt_required()
def greeting():
    current_user = get_jwt_identity()
    return jsonify({"message": f"Hello, {current_user}! You accessed protected data."})

@app.route("/api/admin")
@jwt_required()
def admin():
    user = get_jwt()
    if user.get("role") != "admin":
        return jsonify({"error": "Admin access required"}), 403
    return jsonify({"message": f"Welcome to admin area, {user['sub']}!"})

@app.route("/api/logout", methods=["POST"])
def logout():
    """Clears cookies for browser clients; mobile apps can simply drop tokens."""
    response = jsonify({"message": "Logout successful"})
    unset_jwt_cookies(response)
    return response

@app.route('/api/all',methods=['get'])
def all():
    return jsonify({'message':'all'})

# ====== ERROR HANDLERS ======
@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    token_type = jwt_payload["type"]
    return jsonify({"error": f"{token_type.capitalize()} token has expired"}), 401

@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({"error": "Invalid token"}), 401

@jwt.unauthorized_loader
def missing_token_callback(error):
    return jsonify({"error": "Missing access token"}), 401    

if __name__ == "__main__":
    app.run(debug=True)