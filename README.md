
# Healthcare Management System 🏥

This is a smart and user-friendly hospital management web application built using **Flask** and **Gemini AI**, offering features like:
- ✅ Online appointment booking (with email confirmation)
- 🧠 AI chatbot for mental well-being (MoodLift)
- 🩺 AI-based symptom checker
- 📄 Medical report analyzer using OCR + Gemini AI (Secure)
- 🚑 Ambulance location tracker with email alert
- 👩‍💼 Pharmacy
- 🏥 Virtual view(360) of hospital

---

## 🚀 Tech Stack

- **Frontend:** HTML, CSS, JavaScript
- **Backend:** Python (Flask)
- **APIs:** Gemini AI API, Google Gmail API
- **Database:** JSON (file-based)
- **Deployment:** Render

---

## ⚙️ How to Run Locally

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/Visheshyadav999/Healthcare.git
   cd Healthcare
   ```

2. **Set Up Environment Variables:**
   Create a `.env` file in the root directory and add:
   ```
   GEMINI_API_KEY=your-gemini-api-key
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Flask App:**
   ```bash
   python app.py
   ```

5. **Visit:**
   Open your browser and go to:
   ```
   http://127.0.0.1:5000
   ```
   or directly open the index file in browser

---

## 🔐 Security Notes

- **DO NOT hardcode your Gemini/Gmail API keys** in `app.py`.
- Use `.env` file and access with `os.getenv('GEMINI_API_KEY')` instead.
- Make sure to include `.env` in your `.gitignore` file.

---

## 🤝 Contributions

Feel free to fork the project and submit a pull request!

---

## 📬 Contact

Created by [Vishesh Yadav](https://github.com/Visheshyadav999)  
Feel free to reach out for collaborations or queries!

