import os
import base64
import json
import requests
from flask import Flask, render_template, request, flash, redirect, url_for, jsonify, session
from email.mime.text import MIMEText
from werkzeug.utils import secure_filename
from flask_cors import CORS
import google.generativeai as genai
import smtplib

# --- Configuration ---
app = Flask(__name__, template_folder='templates')
CORS(app)
app.secret_key = 'your_secret_key'
app.config['UPLOAD_FOLDER'] = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# Gemini setup
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

# Allowed file check
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# SMTP Email sender (Gmail App Password)
def send_email(sender_email, app_password, to_email, subject, body):
    try:
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = sender_email
        msg['To'] = to_email

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender_email, app_password)
            server.send_message(msg)
        return "Email sent successfully"
    except Exception as e:
        return f"Error: {e}"

# OCR.Space API text extraction
def extract_text_with_ocr_space(image_path, api_key):
    with open(image_path, 'rb') as f:
        response = requests.post(
            'https://api.ocr.space/parse/image',
            files={'filename': f},
            data={
                'apikey': api_key,
                'language': 'eng'
            },
        )
    result = response.json()
    return result['ParsedResults'][0]['ParsedText'] if result['IsErroredOnProcessing'] == False else "OCR Failed"

# User Auth System
def load_users():
    if os.path.exists('users.json'):
        with open('users.json', 'r') as f:
            return json.load(f)
    return {}

def save_users(users):
    with open('users.json', 'w') as f:
        json.dump(users, f)

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

            # Use OCR.Space API instead of Tesseract
            OCR_API_KEY = os.getenv("OCR_SPACE_API_KEY")
            text = extract_text_with_ocr_space(path, OCR_API_KEY)

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

@app.route('/emer')
def emer():
    return render_template('emer.html')

@app.route('/doclist')
def doclist():
    return render_template('doclist.html')

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
        sender_email = 'devilofmyownworld90@gmail.com'
        app_password = os.getenv("EMAIL_APP_PASSWORD")
        email_status = send_email(sender_email, app_password, email, subject, body)
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
        sender_email = 'devilofmyownworld90@gmail.com'
        app_password = os.getenv("EMAIL_APP_PASSWORD")
        email_status = send_email(sender_email, app_password, email, subject, body)
        if "Error" in email_status:
            flash(f'Error sending email: {email_status}', 'error')
            return redirect(url_for('ambu_track'))
        flash('Ambulance booked! Live location sent to your email.', 'success')
    except Exception as e:
        flash(f'Error: {str(e)}', 'error')
    return redirect(url_for('ambu_track'))

@app.route("/chat")
def chat_bot():
    return render_template("chatbot.html")

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

# REMOVE app.run() - Gunicorn will handle this in production
os.makedirs('uploads', exist_ok=True)  # Ensure upload folder exists

