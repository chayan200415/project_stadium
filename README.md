# StadiumGPT - Smart Stadiums & Tournament Operations

StadiumGPT is a Generative AI-enabled solution designed to enhance stadium operations and improve the FIFA World Cup 2026 experience for fans, organizers, volunteers, and venue staff.

## 🌟 Project Overview
Unlike a standard chatbot, StadiumGPT acts as an intelligent AI assistant that understands live stadium situations and provides context-aware, actionable recommendations. The solution features an interactive dashboard for crowd intelligence, operations (incidents), transport, and sustainability.

## 🏗 Architecture
- **Frontend**: React 18 (Vite), TypeScript, Tailwind CSS, shadcn/ui, Recharts, Framer Motion
- **Backend**: FastAPI (Python), SQLite (SQLAlchemy ORM)
- **Generative AI**: Google Gemini API (via `google-generativeai`)

## ✨ Features
1. **AI Fan Assistant**: Contextual chatbot for routing, queues, and general stadium questions.
2. **AI Crowd Intelligence**: Real-time simulated occupancy dashboard with AI congestion alerts.
3. **AI Incident Assistant**: Incident reporting tool that instantly generates AI emergency response plans.
4. **Transportation Hub**: Simulates metro, bus, and parking availability.
5. **Sustainability Dashboard**: Tracks power, water, waste, and food surplus with AI optimization insights.
6. **AI Match Day Summary**: Automatically generates a high-level stadium operations summary.

## 🛠 Tech Stack
- **Frontend**: React, React Router, TailwindCSS, Lucide React, Recharts, Framer Motion
- **Backend**: FastAPI, Uvicorn, SQLAlchemy, Pydantic, python-dotenv
- **Testing**: Pytest

## 🚀 Installation & Running

### Prerequisites
- Node.js (v18+)
- Python (3.10+)
- Google Gemini API Key

### 1. Clone & Environment Setup
Create a `.env` file in the root directory (copy from `.env.example`):
```env
GEMINI_API_KEY=your_api_key_here
DATABASE_URL=sqlite:///./stadium.db
```

### 2. Backend Setup
```bash
python -m venv venv
# Activate venv (Windows: venv\Scripts\activate, Mac/Linux: source venv/bin/activate)
pip install -r requirements.txt
uvicorn backend.main:app --reload
```
*Backend runs on http://localhost:8000*

### 3. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```
*Frontend runs on http://localhost:5173*

## 📂 Folder Structure
```
project_stadium/
├── backend/
│   ├── routes/          # API endpoint routers (chat, crowd, incident, etc.)
│   ├── services/        # AI service and prompt templates
│   ├── database.py      # SQLAlchemy setup
│   ├── main.py          # FastAPI entry point
│   ├── models.py        # Database models
│   └── schemas.py       # Pydantic validation schemas
├── frontend/
│   ├── src/
│   │   ├── components/  # Reusable UI components (shadcn/ui, Layout, Sidebar)
│   │   ├── lib/         # Utility functions
│   │   ├── pages/       # Dashboard, Chat, Navigation, Operations views
│   │   ├── App.tsx      # Main React Router setup
│   │   └── main.tsx     # React entry point
│   ├── tailwind.config.js
│   └── vite.config.ts
├── tests/               # Pytest tests
├── .env.example
├── requirements.txt
└── README.md
```

## 📸 Screenshots
*(Placeholder for UI screenshots)*
- Dashboard Overview
- AI Chat Interface
- Operations Center

## 🔮 Future Improvements
- **Voice Support**: Integrate Web Speech API for voice input/output.
- **Real-Time Data**: Replace mocked sensor data with WebSockets/Kafka streams.
- **Multilingual UI**: Extend translation beyond chat to the entire UI.
- **PWA & Docker**: Add Progressive Web App support and Dockerize for easier deployment.

## 📝 Assumptions
- For this MVP, data (crowd, sustainability, transport) is mocked/simulated in the backend routers.
- SQLite is used for simplicity, but can be easily swapped to PostgreSQL via SQLAlchemy.
