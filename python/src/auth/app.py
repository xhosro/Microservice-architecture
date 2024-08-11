import jwt
import datetime
import os
from flask import Flask, request, jsonify
from flask_mysqldb import MySQL

# Initialize Flask application
server = Flask(__name__)
mysql = MySQL(server)

# Configuration settings for MySQL database
server.config['MYSQL_HOST'] = os.environ.get('MYSQL_HOST')
server.config['MYSQL_USER'] = os.environ.get('MYSQL_USER')
server.config['MYSQL_PASSWORD'] = os.environ.get('MYSQL_PASSWORD')
server.config['MYSQL_DB'] = os.environ.get('MYSQL_DB')
server.config['MYSQL_PORT'] = int(os.environ.get('MYSQL_PORT', 3306))  # Ensure port is an integer

@server.route('/login', methods=['POST'])
def login():
    # Extract basic authentication credentials from the request
    auth = request.authorization
    if not auth:
        return jsonify({'error': 'Missing credentials'}), 401
    
    # Query the database for user information based on the provided username
    cur = mysql.connection.cursor()
    res = cur.execute(
        "SELECT email, password FROM user WHERE email=%s", (auth.username,)
    )
    
    if res > 0:
        user_row = cur.fetchone()
        email = user_row[0]
        password = user_row[1]
        
        # Validate the provided credentials
        if auth.username != email or auth.password != password:
            return jsonify({'error': 'Invalid credentials'}), 401
        else:
            # Generate a JWT token upon successful authentication
            token = createJWT(auth.username, os.environ.get("JWT_SECRET"), True)
            return jsonify({'token': token}), 200
    else:
        # Return an error if the user is not found
        return jsonify({'error': 'Invalid credentials'}), 401
    
@server.route("/validate", methods=["POST"]) 
def validate():
    # Extract JWT token from the Authorization header
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        return jsonify({'error': 'Missing credentials'}), 401
    
    # Extract the token part from "Bearer <token>" format
    parts = auth_header.split()
    if len(parts) != 2 or parts[0] != "Bearer":
        return jsonify({'error': 'Invalid authorization header format'}), 400
    
    encoded_jwt = parts[1]

    try:
        # Decode and validate the JWT token
        decoded = jwt.decode(
            encoded_jwt, os.environ.get("JWT_SECRET"), algorithms=["HS256"]
        )
    except jwt.ExpiredSignatureError:
        return jsonify({'error': 'Token expired'}), 403
    except jwt.InvalidTokenError:
        return jsonify({'error': 'Invalid token'}), 403

    # Return the decoded JWT payload
    return jsonify(decoded), 200
    
def createJWT(username, secret, authz):
    # Create a JWT token with specified claims
    return jwt.encode(
        {
            'username': username,
            'exp': datetime.datetime.now(tz=datetime.timezone.utc)
            + datetime.timedelta(days=1),  # Token expiration time
            'iat': datetime.datetime.utcnow(),  # Token issued at time
            'admin': authz,  # Custom claim to indicate authorization level
        },
        secret,
        algorithm='HS256'
        # For production, consider using a more secure method like RSA or ECC
    )
    
if __name__ == '__main__':
    # Run the Flask application
    server.run(host="0.0.0.0", port=5000)

