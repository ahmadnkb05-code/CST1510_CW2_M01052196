# CST1510 Coursework 2 – Multi-Domain Intelligence Platform (Cyber + IT)

This project is built for **Tier 2**, combining two real-world areas: **Cybersecurity** and **IT Support**.  
It’s designed to show how data from different domains can be connected, managed, and visualized through one unified dashboard.

The goal was to make something practical — not just code that runs, but a tool that looks and feels like a small working system.

---

## 1. Overview

Most organizations track two things constantly:
- **Cyber incidents** (like data breaches or malware detections)
- **IT support tickets** (things like system errors or user issues)

This app brings those together in one place.  
You can log in, view incidents and tickets, make edits, and explore patterns with simple, clear graphs.

---

## 2. Features at a Glance

✅ Secure login using password hashing (bcrypt)  
✅ Manage and visualize both Cyber and IT data  
✅ Create, view, update, and delete records (CRUD)  
✅ Real-time interactive charts using Plotly  
✅ Optional OpenAI-powered insights  
✅ Clean and minimal interface powered by Streamlit  

---

## 3. Tech Stack

| Component | Tool | Why It’s Used |
|------------|------|---------------|
| Frontend | **Streamlit** | Fast, no-fuss dashboard creation |
| Database | **SQLite** | Simple and perfect for local data |
| Security | **bcrypt** | Encrypts user passwords securely |
| Data Handling | **Pandas** | Easy manipulation and filtering |
| Charts | **Plotly** | Clear visuals with interactivity |
| AI (optional) | **OpenAI API** | Adds smart suggestions and insights |
| Config | **dotenv** | Keeps API keys out of code |

---

## 4. Folder Guide (How Everything’s Organized)
```
CST1510_CW2_Project/
│
├── app.py # Main Streamlit app
├── auth.py # User registration & login
├── db_manager.py # Handles database setup and connection
├── models.py # Defines CRUD operations
├── migrate_users_to_db.py # Moves registered users into database
├── load_sample_data.py # Inserts demo Cyber & IT data
├── ai_helper.py # Optional AI insights (OpenAI)
├── utils.py # Helper functions
│
├── .env.example # Template for API key
├── requirements.txt # Libraries list
├── README.md # Project documentation
│
└── pages/
├── Login.py
├── Cyber_Dashboard.py
└── IT_Dashboard.py
```

---

## 5. How to Run (start to finish)

1. **Install requirements**
   ```bash
   pip install -r requirements.txt
   python auth.py
