from flask import Flask, jsonify, request
import jwt
import datetime
from jwt_decorator import role_required, token_required

SECRET_KEY = "supersecretkey"
user = {
    'username':'rd003',
    'password':'123',
    'role':'admin'
}

app = Flask(__name__)

@app.route("/api/login",methods=['post'])
def login():
    data = request.get_json()

    if not data or 'username' not in data or 'password' not in data:
        return jsonify({'error':'validation error'}),400
    
    username = user['username']
    password = user['password']
    role = user['role']

    if data['username']==username and data['password']==password:
        token = jwt.encode({
            'username':username,
            'role':role,
            'exp':datetime.datetime.utcnow()+datetime.timedelta(minutes=1)
        },SECRET_KEY,algorithm="HS256")
        return jsonify({'token':token})
    
    return ({'error':'invalid credentials'}),401

@app.route("/api/greet",methods=['get'])
@token_required
def greeting():
    return jsonify({"message": f"Hello, {request.user}! You accessed protected data."})

@app.route("/api/admin")
@token_required
@role_required("admin")
def admin_area():
    return jsonify({
        "message": f"Welcome to admin area, {request.user['username']}!"
    })

@app.route('/api/all',methods=['get'])
def all():
    return jsonify({'message':'all'})

app.run(debug=True)