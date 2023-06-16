from flask import Flask, jsonify, request
import tensorflow as tf
import numpy as np
import cv2
from tensorflow.keras.preprocessing.image import img_to_array
import bcrypt
import jwt
import mysql.connector
from functools import wraps

app = Flask(__name__)

db = mysql.connector.connect(
    host='34.101.63.220',
    user='nisa',
    password='123',
    database='framewiz'
)

model = tf.keras.models.load_model('model2')

face_shape_categories = ['oval', 'round', 'heart', 'square', 'oblong']

@app.before_request
def allow_unauthenticated():
    return

@app.route('/predict', methods=['POST'])
def predict():
    image = request.files['image']
    image = cv2.imdecode(np.fromstring(image.read(), np.uint8), cv2.IMREAD_GRAYSCALE)
    
    image = cv2.resize(image, (250, 190))
    image = image.astype("float") / 255.0
    image = img_to_array(image)
    image = np.expand_dims(image, axis=0)

    predictions = model.predict(image)
    predicted_class_index = np.argmax(predictions)
    predicted_class = face_shape_categories[predicted_class_index]

    response = {'predicted_class': predicted_class}
    return jsonify(response)

@app.route('/register', methods=['POST'])
def register():
    email = request.form.get('email')
    password = request.form.get('password')
    nama = request.form.get('nama')

    if not email or not password or not nama:
        return jsonify({'message': 'Email, password, and nama are required'}), 400

    cursor = db.cursor()
    cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
    results = cursor.fetchall()

    if len(results) > 0:
        return jsonify({'message': 'User already exists'}), 409

    salt = bcrypt.gensalt(10)
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)

    cursor.execute("INSERT INTO users (email, password, nama) VALUES (%s, %s, %s)", (email, hashed_password, nama))
    db.commit()

    return jsonify({'message': 'User registered successfully'}), 201

@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')

    if not email or not password:
        return jsonify({'message': 'Email and password are required'}), 400

    cursor = db.cursor()
    cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
    results = cursor.fetchall()

    if len(results) == 0:
        return jsonify({'message': 'Invalid credentials'}), 401

    user = results[0]

    if not bcrypt.checkpw(password.encode('utf-8'), user[2].encode('utf-8')):
        return jsonify({'message': 'Invalid credentials'}), 401

    payload = {'user_id': user[0], 'email': user[1]}
    secret_key = 'IniAdalahKunciRahasia123!@#'
    token = jwt.encode(payload, secret_key, algorithm='HS256')

    return jsonify({'message': 'Login successful', 'token': token}), 200

def verify_token(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')

        if not token:
            return jsonify({'error': 'Token is missing'}), 401

        try:
            decoded = jwt.decode(token, 'IniAdalahKunciRahasia123!@#', algorithms=['HS256'])
            kwargs['user_id'] = decoded['user_id']
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Invalid token'}), 401

        return f(*args, **kwargs)

    return decorated

if __name__ == '__main__':
    app.run(debug=True)
