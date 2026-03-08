# 🧠 ArogyaMitra – AI Powered Fitness Platform

ArogyaMitra is an AI-powered fitness and wellness platform that helps users improve their health through personalized workout plans, nutrition guidance, and progress tracking.

The system uses AI to generate workout routines and nutrition plans while tracking the user’s fitness progress through analytics and charts.

---

# 🚀 Features

- 🔐 User Authentication (JWT based login & registration)
- 🏋️ AI Workout Planner
- 🍎 AI Nutrition Planner
- 📊 Progress Tracking Dashboard
- 📅 Workout History
- 📈 Weekly Activity Analytics
- 🤖 AI Fitness Assistant

---

# 🛠 Tech Stack

### Frontend
- React
- TypeScript
- Tailwind CSS
- Axios
- React Query
- Framer Motion
- Recharts

### Backend
- FastAPI
- SQLAlchemy
- SQLite
- JWT Authentication

### APIs & AI
- Groq AI
- Spoonacular API

---

# 📂 Project Structure
ArogyaMitra
│
├── backend
│ ├── config
│ ├── models
│ ├── routes
│ ├── services
│ ├── main.py
│ └── requirements.txt
│
├── frontend
│ ├── src
│ ├── public
│ ├── package.json
│ └── vite.config.ts
│
└── README.md

---

# ⚙️ Backend Setup (FastAPI)

## 1️⃣ Navigate to backend folder


cd backend


## 2️⃣ Create virtual environment


python -m venv myenv


Activate environment

### Windows

myenv\Scripts\activate


### Linux/Mac

source myenv/bin/activate


## 3️⃣ Install dependencies


pip install -r requirements.txt


## 4️⃣ Add environment variables

Create `.env` file inside backend folder


GROQ_API_KEY=your_key
SPOONACULAR_API_KEY=your_key
SECRET_KEY=your_secret


## 5️⃣ Run backend server


uvicorn main:app --reload


Backend will start at:


http://127.0.0.1:8000


Swagger API docs:


http://127.0.0.1:8000/docs


---

# 💻 Frontend Setup (React)

## 1️⃣ Navigate to frontend folder


cd frontend


## 2️⃣ Install dependencies


npm install


## 3️⃣ Start development server


npm run dev


Frontend will run at:


http://localhost:5173


---

# 🔗 Connecting Frontend to Backend

Make sure API base URL in frontend is set to:


http://127.0.0.1:8000


or your deployed backend URL.

---

# 🎥 Demo Workflow

1. Register/Login
2. View Dashboard
3. Generate Workout Plan
4. Perform Exercises
5. Generate Nutrition Plan
6. Track Progress

---

# 👨‍💻 Authors

- Swaroop 
- Pranay 
- Prashik 
- Nandini  

---

# 📜 License

This project was developed for academic purposes.
