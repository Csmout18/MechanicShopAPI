from datetime import datetime, timedelta, timezone
from jose import jwt
from functools import wraps
from flask import request, jsonify


SECRET_KEY = 'a super secret, secret key'

def encode_token(customer_id): #used uniqed info to make tokens user specific
    payload = {
        'exp': datetime.now(timezone.utc) + timedelta(days=0,hours=1), #Sets the expiration time to 1 hour
        'iat' :datetime.now(timezone.utc), #'issued at'
        'sub': str(customer_id) #This needs to be a string or the token with be malformed and won't be able to be decoded
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split()[1]
            
            if not token:
                return jsonify({"message": "Token is missing!"}), 400
            
            try:
                
                data = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
                print(data)
                customer_id = data['sub']
            except jwt.ExpiredSignatureError as e:
                return jsonify({"message": "Token has expired!"}), 400
            except jwt.InvalidTokenError:
                return jsonify({"message": "Token is invalid!"}), 400
            
            return f(customer_id, *args, **kwargs)
        else:
            return jsonify({"message": "Login required for access."}), 400
        
    return decorated