
# 🏥 HealthCare Management System (Flask + Gemini + OCR + Email)

A modern, AI-powered healthcare platform built using **Flask**, **Gemini AI**, **OCR.Space**, and **Render**. Users can book appointments, upload medical reports for AI analysis, and request ambulance services with live tracking.

## 🔗 Live Demo  
🌐 [Visit the Live Site](https://healthcare-9k9b.onrender.com)

---


## ✨ Features

- 🔐 **Signup & Login** System (Flask Sessions)
- 🧾 **AI Medical Report Analysis** using OCR + Gemini AI
- 🤖 **AI Chatbot for Symptom Check**
- 📧 **Email Confirmations** on Appointment/Booking
- 🩺 **Doctor Appointment Booking**
- 🚑 **Ambulance Booking with Live Google Maps Location**
- 😄 **MoodLifter Chatbot** for mental well-being
-    **Pharmacy**

---

## ⚙️ Technologies Used

| Backend        | Frontend    | APIs / Tools             |
|----------------|-------------|---------------------------|
| Flask (Python) | HTML, CSS   | Gemini API (Google AI)    |
| Flask-Mail     | JavaScript  | OCR.Space API             |
| Flask-CORS     | Bootstrap   | Gmail SMTP                |

---

## 🛠️ Setup Instructions (Local)

1. **Clone this repository**
   git clone https://github.com/Visheshyadav999/HealthCare.git
   cd HealthCare
   ```

2. **Create a virtual environment**
   python -m venv venv
   source venv/bin/activate  # or venv\Scripts\activate on Windows
   ```

3. **Install dependencies**
   pip install -r requirements.txt
   ```

4. **Create `.env` file** and add:
   GEMINI_API_KEY=your_google_gemini_key
   EMAIL_APP_PASSWORD=your_gmail_app_password
   OCR_API_KEY=your_ocr_space_api_key
   ```

5. **Run the app**
   python app.py
   ```

---


## 🧠 Future Enhancements

- Admin dashboard to view appointments
- Upload and manage full patient history
- WhatsApp integration for alert messages

---

## 🙋‍♂️ Developed By

**Vishesh Yadav**  
📫 [LinkedIn](https://www.linkedin.com/in/visheshyadav999/) | [GitHub](https://github.com/Visheshyadav999)

---

## 📜 License

This project is licensed under the MIT License.
