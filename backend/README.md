# Drug Repurposing Platform - Python Backend

FastAPI backend with AI-powered drug repurposing analysis and Hugging Face dataset integration.

## Features

- 🤖 **AI-Powered Analysis** - Uses OpenAI GPT-4 for intelligent analysis
- 📊 **Hugging Face Integration** - Fetches real medicine data from Hugging Face datasets
- 🔄 **Intelligent Fallback** - Rule-based system when API key not available
- 🚀 **FastAPI** - Modern, fast Python web framework
- 📊 **Comprehensive Analysis** - Research papers, clinical trials, patents, market data
- 🔒 **CORS Enabled** - Ready for frontend integration

## Setup

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Configure environment (optional):**
```bash
cp .env.example .env
# Edit .env and add your OpenAI API key if you have one
```

3. **Run the server:**
```bash
python main.py
# Or with uvicorn directly:
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

## API Endpoints

### POST `/api/analyze`
Analyze drug repurposing potential with Hugging Face data.

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
  "recommendations": [...],
  "analysis_metadata": {...}
}
```

### GET `/api/medicines`
Get all medicines from Hugging Face dataset.

### GET `/api/medicines/search?drug_name=metformin`
Search for a specific medicine in the dataset.

### GET `/api/medicines/by-condition?condition=cancer`
Find medicines that could be repurposed for a condition.

### GET `/api/medicines/{drug_name}/details`
Get comprehensive details about a medicine.

### GET `/api/drugs/suggestions?query=met`
Get drug name suggestions for autocomplete.

### GET `/api/conditions/suggestions?query=can`
Get condition name suggestions for autocomplete.

### GET `/health`
Health check endpoint.

## Hugging Face Integration

The backend automatically loads medicine datasets from Hugging Face:
- **medical_medicine_dataset** - 700+ pharmaceutical drugs with descriptions, uses, and side effects
- **Built-in comprehensive database** - Additional medicines with repurposing potential

The system fetches real medicine data and uses it to enhance AI analysis.

## AI Integration

The backend uses OpenAI GPT-4 when an API key is provided, otherwise falls back to an intelligent rule-based system that provides medically accurate analysis using Hugging Face data.

## Development

```bash
# Install in development mode
pip install -r requirements.txt

# Run with auto-reload
uvicorn main:app --reload
```

## Dataset Sources

- **Hugging Face**: `darkknight25/medical_medicine_dataset` - 700+ medicines
- **Built-in Database**: Comprehensive medicine database with repurposing information
