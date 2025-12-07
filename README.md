# Drug Repurposing Platform

A full-stack AI-powered platform for drug repurposing analysis, transforming months of manual research into minutes of intelligent analysis.

## 🚀 Features

- **AI-Powered Analysis** - Uses OpenAI GPT-4 for intelligent drug repurposing analysis
- **Hugging Face Integration** - Fetches real medicine datasets from Hugging Face (700+ medicines)
- **Python Backend** - FastAPI backend with comprehensive analysis engine
- **React Frontend** - Modern, responsive UI built with React + Vite
- **Medically Accurate** - Evidence-based analysis with real research data
- **Comprehensive Reports** - Research papers, clinical trials, patents, and market feasibility
- **Real Medicine Database** - Access to comprehensive medicine information from Hugging Face datasets

## 📁 Project Structure

```
druggs/
├── backend/                 # Python FastAPI backend
│   ├── main.py              # FastAPI application
│   ├── services/            # AI analysis services
│   │   └── ai_analyzer.py   # AI-powered analyzer
│   ├── requirements.txt     # Python dependencies
│   └── README.md            # Backend documentation
├── src/                     # React frontend
│   ├── components/          # React components
│   ├── App.jsx              # Main application
│   └── main.jsx             # Entry point
└── package.json             # Frontend dependencies
```

## 🛠️ Setup Instructions

### Backend Setup

1. **Navigate to backend directory:**
```bash
cd backend
```

2. **Create virtual environment (recommended):**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Configure environment (optional):**
```bash
cp .env.example .env
# Edit .env and add your OpenAI API key if you have one
```

5. **Run the backend server:**
```bash
python main.py
# Or: uvicorn main:app --reload
```

Backend will run on `http://localhost:8000`

### Frontend Setup

1. **Install dependencies:**
```bash
npm install
```

2. **Start development server:**
```bash
npm run dev
```

Frontend will run on `http://localhost:5173`

## 🔧 Configuration

### OpenAI API (Optional but Recommended)

For enhanced AI-powered analysis, add your OpenAI API key:

1. Get API key from [OpenAI Platform](https://platform.openai.com/api-keys)
2. Create `backend/.env` file:
```env
OPENAI_API_KEY=your_api_key_here
```

Without an API key, the system uses an intelligent fallback that still provides medically accurate analysis.

## 📡 API Endpoints

### POST `/api/analyze`
Analyze drug repurposing potential.

**Request:**
```json
{
  "drug_name": "Metformin",
  "target_condition": "Cancer"
}
```

**Response:**
```json
{
  "drug_name": "Metformin",
  "target_condition": "Cancer",
  "research_papers": [...],
  "clinical_trials": [...],
  "patents": [...],
  "market_feasibility": {...},
  "repurposeability_score": 89,
  "recommendations": [...]
}
```

### GET `/api/drugs/suggestions?query=met`
Get drug name suggestions.

### GET `/api/conditions/suggestions?query=can`
Get condition name suggestions.

## 🧪 Example Searches

- **Metformin** for **Cancer** - Well-documented repurposing case
- **Metformin** for **PCOS** - FDA-approved off-label use
- **Aspirin** for **Cardiovascular Disease** - Established prevention
- **Sildenafil** for **Pulmonary Hypertension** - FDA-approved as Revatio
- **Zinc** for **Diarrhea** - WHO-recommended adjunct to ORS

## 🏗️ Technology Stack

### Backend
- **FastAPI** - Modern Python web framework
- **OpenAI GPT-4** - AI-powered analysis
- **Hugging Face Datasets** - Real medicine data (700+ medicines)
- **Transformers** - AI model integration
- **Pydantic** - Data validation
- **Uvicorn** - ASGI server

### Frontend
- **React 18** - UI library
- **Vite** - Build tool
- **Tailwind CSS** - Styling
- **Lucide React** - Icons

## 📝 Development

### Backend Development
```bash
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Development
```bash
npm run dev
```

### Build for Production

**Frontend:**
```bash
npm run build
```

**Backend:**
The FastAPI app is ready for production deployment with uvicorn or gunicorn.

## 🔒 Security Notes

- API keys should never be committed to version control
- Use environment variables for sensitive configuration
- CORS is configured for development; adjust for production

## 📄 License

MIT
