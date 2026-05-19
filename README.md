# MediBot - Rule-Based Medical Assistant Chatbot
### CodSoft AI Internship | Task 1

## 📌 About
MediBot is a rule-based chatbot built with Python (Flask) that provides first-aid guidance for:
- 🧴 Skincare (acne, dry skin, oily skin, sunburn, rashes, dark spots, eczema)
- 🩹 Wounds & Injuries (cuts, deep wounds, burns, bruises, infections, sprains)
- 🌡️ General Symptoms (fever, cold, cough, headache, nausea, dizziness, eye issues)

## 🛠️ Tech Stack
- **Backend:** Python, Flask
- **Frontend:** HTML, CSS, JavaScript
- **Logic:** Regex-based pattern matching (rule-based NLP)

## 🚀 How to Run

### 1. Install dependencies
```bash
pip install flask
```

### 2. Run the app
```bash
python app.py
```

### 3. Open in browser
```
http://127.0.0.1:5000
```

## 📁 Project Structure
```
medbot/
├── app.py               # Flask backend + rule engine
├── requirements.txt     # Dependencies
├── README.md
└── templates/
    └── index.html       # Frontend UI
```

## ⚠️ Disclaimer
MediBot provides general first-aid guidance only. It is NOT a substitute for professional medical advice. Always consult a qualified doctor for serious conditions.
