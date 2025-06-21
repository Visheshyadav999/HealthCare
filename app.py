import os
import base64
import json
from flask import Flask, render_template, request, flash, redirect, url_for, jsonify, session
from email.mime.text import MIMEText
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
import google.generativeai as genai
from werkzeug.utils import secure_filename
from PIL import Image
import pytesseract
from flask_cors import CORS
from dotenv import load_dotenv
load_dotenv()


# --- Configuration ---
app = Flask(__name__, template_folder='public/templates')
CORS(app)
app.secret_key = 'your_secret_key'
app.config['UPLOAD_FOLDER'] = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# Allowed file check
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Gmail API Setup
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

def authenticate_gmail():
    creds = None
    token_file = 'token.json'
    if os.path.exists(token_file):
        creds = Credentials.from_authorized_user_file(token_file, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open(token_file, 'w') as token:
            token.write(creds.to_json())
    return build('gmail', 'v1', credentials=creds)

def send_email(service, sender, to, subject, body):
    message = MIMEText(body)
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
    message_body = {'raw': raw_message}
    try:
        sent_message = service.users().messages().send(userId="me", body=message_body).execute()
        print(f"Message sent: {sent_message['id']}")
    except Exception as e:
        print(f"An error occurred: {e}")
        return f"Error: {str(e)}"

# Gemini setup
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

# User Auth System
def load_users():
    if os.path.exists('users.json'):
        with open('users.json', 'r') as f:
            return json.load(f)
    return {}

def save_users(users):
    with open('users.json', 'w') as f:
        json.dump(users, f)

# --- Routes ---
@app.route('/')
def home():
    return render_template("home.html")

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        users = load_users()
        if email in users:
            flash('Email already exists')
        else:
            users[email] = {'password': password}
            save_users(users)
            flash('Signup successful, please login')
            return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        users = load_users()
        if email in users and users[email]['password'] == password:
            session['user'] = email
            return redirect(url_for('upload'))
        else:
            flash('Invalid credentials')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    flash('Logged out successfully')
    return redirect(url_for('login'))

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if 'user' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(path)
            text = pytesseract.image_to_string(Image.open(path))
            prompt = f"""
            Analyze the following medical report and provide:
            - A summary in simple language
            - Pros (good signs in the report)
            - Cons (issues found in the report)

            Report:
            {text}
            """
            response = model.generate_content(prompt)
            return render_template('result.html', result=response.text)
        else:
            flash('Only image files allowed (jpg, jpeg, png)')
    return render_template('upload.html')

@app.route('/appointment_form')
def appointment_form():
    return render_template('appointment_form.html')

@app.route('/book_appointment', methods=['POST'])
def book_appointment():
    name = request.form.get('name')
    email = request.form.get('email')
    doctor = request.form.get('doctor')
    date = request.form.get('date')
    time = request.form.get('time')
    if not name or not email or not doctor or not date or not time:
        flash('All fields are required!', 'error')
        return redirect(url_for('appointment_form'))
    try:
        subject = 'Appointment Confirmation'
        body = f"""
        Hello {name},

        Your appointment with {doctor} has been scheduled for:
        Date: {date}
        Time: {time}

        Thank you for booking with us!

        Best Regards,
        Your Healthcare Provider
        """
        service = authenticate_gmail()
        sender_email = 'your_email@gmail.com'
        email_status = send_email(service, sender_email, email, subject, body)
        if "Error" in email_status:
            flash(f'Error sending email: {email_status}', 'error')
            return redirect(url_for('appointment_form'))
        flash('Appointment booked successfully! A confirmation email has been sent.', 'success')
    except Exception as e:
        flash(f'Error: {str(e)}', 'error')
    return redirect(url_for('appointment_form'))

@app.route('/ambu_track')
def ambu_track():
    return render_template('ambu_track.html')

@app.route('/book_ambulance', methods=['POST'])
def book_ambulance():
    name = request.form.get('name')
    email = request.form.get('email')
    if not name or not email:
        flash('All fields are required!', 'error')
        return redirect(url_for('ambu_track'))
    try:
        subject = '🚑 Ambulance on the way!'
        body = f"""
        Hello {name},

        Track the ambulance here:
        https://maps.app.goo.gl/NezjqRXwvxFX6H4K9

        Best Regards,
        Your Healthcare Provider
        """
        service = authenticate_gmail()
        sender_email = 'your_email@gmail.com'
        email_status = send_email(service, sender_email, email, subject, body)
        if "Error" in email_status:
            flash(f'Error sending email: {email_status}', 'error')
            return redirect(url_for('ambu_track'))
        flash('Ambulance booked! Live location sent to your email.', 'success')
    except Exception as e:
        flash(f'Error: {str(e)}', 'error')
    return redirect(url_for('ambu_track'))

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message", "")
    if not user_input:
        return jsonify({"error": "No input provided."}), 400
    try:
        system_prompt = "You are a symptoms checker chatbot. Users will describe their health problems. If the user asks for a solution, provide a basic solution with no side effects.\n\n"
        full_prompt = system_prompt + user_input
        response = model.generate_content(full_prompt)
        return jsonify({"response": response.text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/moodlift")
def mood_page():
    return render_template("moodlift.html")

@app.route("/mood_chat", methods=["POST"])
def mood_chat():
    user_input = request.json.get("message", "")
    if not user_input:
        return jsonify({"response": "Please say something!"}), 400
    try:
        prompt = f"""
        You're a supportive and cheerful AI friend. Your job is to lift the mood of a user who might be sad, stressed, or anxious.
        Always reply in short, casual, fun messages like a friend would in WhatsApp. Be positive and funny when possible.

        User: {user_input}
        AI:
        """
        response = model.generate_content(prompt)
        return jsonify({"response": response.text.strip()})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    os.makedirs('uploads', exist_ok=True)
    app.run(debug=True)