from flask import Flask, request, jsonify, Response, session, make_response, redirect
from flask_session import Session
from flask_cors import CORS
import redis
import bcrypt
import mysql.connector
import os
from dotenv import load_dotenv
import openai
from werkzeug.utils import secure_filename
import docx

app = Flask(__name__)
CORS(app, supports_credentials=True, origins=["http://bachattv.com"])

app.config['SECRET_KEY'] = '31423142314231423142'
app.config['SESSION_TYPE'] = 'redis'
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_USE_SIGNER'] = True
app.config['SESSION_KEY_PREFIX'] = 'session:'
app.config['SESSION_REDIS'] = redis.StrictRedis(host='172.234.123.78', port=6379, db=0)
app.config['SESSION_COOKIE_NAME'] = 'your_cookie_name'
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'None'

Session(app)

dotenv_path = 'doc_2024-04-30_19-13-36.env'
load_dotenv(dotenv_path)

api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = api_key

db = mysql.connector.connect(
    host="172.234.123.78",
    user="root",
    password="3142758609",
    database="bachat_users",
    port=3306
)

@app.after_request
def after_request(response):
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization'
    response.headers['Access-Control-Allow-Methods'] = 'GET,PUT,POST,DELETE,OPTIONS'
    response.headers['Access-Control-Allow-Origin'] = 'http://bachattv.com'
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    return response

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'doc', 'docx'}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def read_docx(file_path):
    doc = docx.Document(file_path)
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)
    return '\n'.join(full_text)

# ChatBot
@app.route('/api/send-message', methods=['POST'])
def api_handle_user_message():
    data = request.json
    message = data.get('message')
    if message:
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": message}]
            )
            responses = response.choices[0].message['content'].strip()
            return jsonify({"response": responses}), 200
        except Exception as e:
            app.logger.error(f"Error processing the message: {e}")
            return jsonify({"error": "Failed to process your message"}), 500
    else:
        return jsonify({"error": "No message provided"}), 400

@app.route('/api/upload-document', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        if os.path.getsize(file_path) > MAX_CONTENT_LENGTH:
            os.remove(file_path)
            return jsonify({"error": "File too large"}), 413

        try:
            cursor = db.cursor()
            with open(file_path, 'rb') as f:
                file_data = f.read()
            cursor.execute("INSERT INTO documents (user_id, file_data, file_name) VALUES (%s, %s, %s)", 
                           (session.get('user_id'), file_data, filename))
            db.commit()
            cursor.close()

            try:
                if filename.endswith('.docx'):
                    file_text = read_docx(file_path)
                else:
                    file_text = file_data.decode('utf-8')

                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "system", "content": "Analyze the following document:"}, {"role": "user", "content": file_text}]
                )
                analysis = response.choices[0].message['content'].strip()
            except (UnicodeDecodeError, docx.opc.exceptions.PackageNotFoundError):
                analysis = "The file could not be decoded as text."

            os.remove(file_path)  # Удаляем файл после обработки

            return jsonify({ "analysis": analysis}), 201
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    else:
        return jsonify({"error": "File type is not allowed"}), 400

# Flask
@app.route('/')
def index():
    return "Welcome to the Flask API!", 200

def hash_password(password):
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt)

def verify_password(password, hashed):
    if isinstance(hashed, str):
        hashed = hashed.encode('utf-8')
    return bcrypt.checkpw(password.encode('utf-8'), hashed)

# Registration and Login
@app.route('/login', methods=['POST'])
def login():
    user = request.json
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT id, password_hash FROM users WHERE email = %s", (user['email'],))
    result = cursor.fetchone()
    cursor.close()

    if result:
        if bcrypt.checkpw(user['password'].encode('utf-8'), result['password_hash'].encode('utf-8')):
            session['user_id'] = result['id']
            app.logger.info(f"User {result['id']} logged in successfully. Session: {session['user_id']}")
            response = make_response(jsonify({"message": "Logged in successfully"}))
            response.set_cookie(
                app.config['SESSION_COOKIE_NAME'],
                session.sid,
                httponly=True,
                secure=app.config['SESSION_COOKIE_SECURE'],
                samesite='None'
            )
            return response, 200
        else:
            app.logger.warning(f"Invalid credentials for email: {user['email']}")
            return jsonify({"error": "Invalid credentials"}), 401
    else:
        app.logger.warning(f"User not found for email: {user['email']}")
        return jsonify({"error": "User not found"}), 404

@app.route('/logout', methods=['POST'])
def logout():
    user_id = session.get('user_id')
    if user_id:
        try:
            cursor = db.cursor()
            cursor.execute("DELETE FROM documents WHERE user_id = %s", (user_id,))
            db.commit()
            cursor.close()
        except mysql.connector.Error as error:
            app.logger.error(f"Error deleting user's documents: {error}")
        session.pop('user_id', None)
    return jsonify({"message": "Logged out successfully"}), 200

@app.route('/user-info', methods=['GET'])
def user_info():
    app.logger.info(f"Session data: {session.items()}")
    if 'user_id' not in session:
        app.logger.info("User not authenticated")
        return jsonify({"error": "User not authenticated"}), 401
    user_id = session['user_id']
    app.logger.info(f"Authenticated user: {user_id}")
    return jsonify({"user_id": user_id, "info": "Some user info"})

@app.route('/users', methods=['POST'])
def add_user():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    try:
        cursor = db.cursor()
        password_hash = hash_password(data['password'])
        cursor.execute(
            "INSERT INTO users (firstName, lastName, email, password_hash) VALUES (%s, %s, %s, %s)",
            (data.get('firstName'), data.get('lastName'), data.get('email'), password_hash)
        )
        db.commit()
        cursor.close()
        return redirect('/')
    except mysql.connector.Error as error:
        app.logger.error(f"Error when trying to register user: {error}")
        return jsonify({"error": "Registration failed"}), 500


# Document 
@app.route('/documents', methods=['GET'])
def get_documents():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"error": "User not authenticated"}), 401
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT id, file_name, created_at FROM documents WHERE user_id = %s", (user_id,))
    documents = cursor.fetchall()
    cursor.close()
    return jsonify(documents)

@app.route('/download/<int:document_id>', methods=['GET'])
def download_file(document_id):
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"error": "User not authenticated"}), 401

    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT file_data, file_name, user_id FROM documents WHERE id = %s", (document_id,))
    doc = cursor.fetchone()
    cursor.close()

    if doc and doc['user_id'] == user_id:
        file_data = doc['file_data']
        file_name = doc['file_name']
        return Response(file_data, mimetype="application/octet-stream", headers={
            "Content-Disposition": f"attachment;filename={file_name}"
        })
    else:
        return jsonify({"error": "Document not found or access denied"}), 404

@app.route('/documents/<int:document_id>', methods=['DELETE'])
def delete_document(document_id):
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"error": "User not authenticated"}), 401

    cursor = db.cursor()
    cursor.execute("DELETE FROM documents WHERE id = %s AND user_id = %s", (document_id, user_id))
    db.commit()
    cursor.close()

    if cursor.rowcount == 0:
        return jsonify({"error": "Document not found or access denied"}), 404

    return jsonify({"message": "Document deleted successfully"}), 200

# Sales - Statistic
@app.route('/sales', methods=['POST'])
def add_sale():
    if 'user_id' not in session:
        return jsonify({"error": "User not authenticated"}), 401
    data = request.get_json()
    if not data or 'amount' not in data or 'date' not in data:
        return jsonify({"error": "Invalid data"}), 400

    try:
        cursor = db.cursor()
        cursor.execute("INSERT INTO sales (user_id, amount, date) VALUES (%s, %s, %s)",
                       (session['user_id'], data['amount'], data['date']))
        db.commit()
        sale_id = cursor.lastrowid
        cursor.close()
        return jsonify({"id": sale_id, "amount": data['amount'], "date": data['date']}), 201
    except mysql.connector.Error as error:
        return jsonify({"error": str(error)}), 500

@app.route('/sales', methods=['GET'])
def get_sales():
    if 'user_id' not in session:
        return jsonify({"error": "User not authenticated"}), 401

    start_date = request.args.get('startDate')
    end_date = request.args.get('endDate')

    query = "SELECT id, amount, date FROM sales WHERE user_id = %s"
    params = [session['user_id']]

    if start_date and end_date:
        query += " AND date BETWEEN %s AND %s"
        params.extend([start_date, end_date])

    cursor = db.cursor(dictionary=True)
    cursor.execute(query, params)
    sales = cursor.fetchall()
    cursor.close()
    return jsonify(sales), 200

@app.route('/sales/<int:sale_id>', methods=['DELETE'])
def delete_sale(sale_id):
    if 'user_id' not in session:
        return jsonify({"error": "User not authenticated"}), 401
    cursor = db.cursor()
    cursor.execute("DELETE FROM sales WHERE id = %s AND user_id = %s", (sale_id, session['user_id']))
    db.commit()
    cursor.close()

    if cursor.rowcount == 0:
        return jsonify({"error": "Sale not found or access denied"}), 404

    return jsonify({"message": "Sale deleted successfully"}), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
