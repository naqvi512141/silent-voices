# Silent Voices
## AI-Powered ASL to Text Translation System

A web application that translates American Sign Language gestures 
from uploaded videos into English text using computer vision and machine learning.

## Team Members
- Irtaza Naqvi (23l-0608)
- Faizan Ashfaq (23L-3091)
- Muhammad Fakhir (22L6827)



## Tech Stack
- **Backend:** Python 3.11, FastAPI, SQLAlchemy, PostgreSQL
- **Frontend:** React 18, Axios, React Router
- **Authentication:** JWT (JSON Web Tokens) + bcrypt
- **ML Pipeline (Sprint 2+):** MediaPipe, Scikit-learn, OpenCV

## How to Run

### Prerequisites
- Python 3.11+, Node.js 18+, PostgreSQL 15+

### Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env       # Edit .env with your database credentials
uvicorn app.main:app --reload
```

### Frontend Setup
```bash
cd frontend
npm install
npm start
```

### API Documentation
Visit http://localhost:8000/docs after starting the backend.