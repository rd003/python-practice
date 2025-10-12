from functools import wraps

from flask import jsonify, request
import jwt

SECRET_KEY = "supersecretkey"

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization")

        if not auth_header:
            return jsonify({"error": "Missing Authorization header"}), 401

        try:
            token = auth_header.split(" ")[1]
            decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            request.user = decoded  # save the entire decoded payload
        except IndexError:
            return jsonify({"error": "Token format must be: Bearer <token>"}), 401
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token has expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token"}), 401

        return f(*args, **kwargs)
    return decorated

def role_required(required_role):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            user_role = request.user.get("role")
            if user_role != required_role:
                return jsonify({
                    "error": f"Access denied. {required_role} role required."
                }), 403
            return f(*args, **kwargs)
        return wrapper
    return decorator