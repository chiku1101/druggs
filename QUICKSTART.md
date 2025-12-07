# Quick Start Guide

Get your Drug Repurposing Platform up and running in minutes!

## 🚀 Quick Start (Both Servers)

### Option 1: Manual Start

**Terminal 1 - Backend:**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

**Terminal 2 - Frontend:**
```bash
npm install
npm run dev
```

### Option 2: Using Startup Scripts

**Backend (Mac/Linux):**
```bash
cd backend
./start.sh
```

**Backend (Windows):**
```bash
cd backend
start.bat
```

**Frontend (Any OS):**
```bash
npm install
npm run dev
```

## 📍 Access Points

- **Frontend:** http://localhost:5173
- **Backend API:** http://localhost:8000
- **API Docs:** http://localhost:8000/docs (Swagger UI)

## 🔑 Optional: Add OpenAI API Key

For enhanced AI analysis:

1. Get API key from https://platform.openai.com/api-keys
2. Create `backend/.env`:
```env
OPENAI_API_KEY=sk-your-key-here
```

Without the key, the system uses an intelligent fallback that still works great!

## ✅ Test It

1. Open http://localhost:5173
2. Try searching: **Metformin** for **Cancer**
3. See the AI-powered analysis!

## 🐛 Troubleshooting

**Backend won't start:**
- Make sure Python 3.8+ is installed
- Check if port 8000 is available
- Verify all dependencies are installed

**Frontend can't connect:**
- Make sure backend is running on port 8000
- Check browser console for CORS errors
- Verify API URL in App.jsx

**No AI analysis:**
- Check if OpenAI API key is set (optional)
- System will use intelligent fallback automatically

