"""
FastAPI Backend for Drug Repurposing Platform
AI-Powered Analysis Service
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import os
from dotenv import load_dotenv
from services.ai_analyzer import AIDrugRepurposingAnalyzer
from services.huggingface_service import HuggingFaceMedicineService


load_dotenv()

app = FastAPI(
    title="Drug Repurposing AI Platform",
    description="AI-powered drug repurposing analysis API",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize AI Analyzer and Hugging Face Service
ai_analyzer = AIDrugRepurposingAnalyzer()
hf_service = HuggingFaceMedicineService()

# Request/Response Models
class RepurposingRequest(BaseModel):
    drug_name: str
    target_condition: str

class ResearchPaper(BaseModel):
    title: str
    authors: str
    journal: str
    year: int
    relevance: int
    summary: str

class ClinicalTrial(BaseModel):
    id: str
    title: str
    status: str
    phase: str
    participants: int
    completion_date: str

class Patent(BaseModel):
    number: str
    title: str
    status: str
    filing_date: str
    assignee: str

class MarketFeasibility(BaseModel):
    market_size: str
    growth_rate: str
    competition: str
    regulatory_path: str
    timeline: str

class RepurposingResponse(BaseModel):
    drug_name: str
    target_condition: str
    research_papers: List[ResearchPaper]
    clinical_trials: List[ClinicalTrial]
    patents: List[Patent]
    market_feasibility: MarketFeasibility
    repurposeability_score: int
    recommendations: List[str]
    analysis_metadata: Optional[dict] = None

@app.get("/")
async def root():
    return {
        "message": "Drug Repurposing AI Platform API",
        "version": "1.0.0",
        "status": "operational"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "ai_service": "operational"}

@app.post("/api/analyze", response_model=RepurposingResponse)
async def analyze_repurposing(request: RepurposingRequest):
    """
    Analyze drug repurposing potential using AI
    """
    try:
        # Validate input
        if not request.drug_name or not request.target_condition:
            raise HTTPException(
                status_code=400,
                detail="Both drug_name and target_condition are required"
            )

        # Perform AI-powered analysis
        analysis_result = await ai_analyzer.analyze(
            drug_name=request.drug_name,
            target_condition=request.target_condition
        )

        return RepurposingResponse(**analysis_result)

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Analysis failed: {str(e)}"
        )

@app.get("/api/drugs/suggestions")
async def get_drug_suggestions(query: str = ""):
    """
    Get drug name suggestions (for autocomplete)
    """
    suggestions = ai_analyzer.get_drug_suggestions(query)
    return {"suggestions": suggestions}

@app.get("/api/conditions/suggestions")
async def get_condition_suggestions(query: str = ""):
    """
    Get condition name suggestions (for autocomplete)
    """
    suggestions = ai_analyzer.get_condition_suggestions(query)
    return {"suggestions": suggestions}

@app.get("/api/medicines")
async def get_all_medicines():
    """
    Get all medicines from Hugging Face dataset
    """
    medicines = await hf_service.get_all_medicines()
    return {"medicines": medicines, "count": len(medicines)}

@app.get("/api/medicines/search")
async def search_medicine(drug_name: str):
    """
    Search for a specific medicine in Hugging Face dataset
    """
    medicine = await hf_service.search_medicine(drug_name)
    if medicine:
        return {"medicine": medicine, "found": True}
    return {"medicine": None, "found": False}

@app.get("/api/medicines/by-condition")
async def get_medicines_by_condition(condition: str):
    """
    Find medicines that could be repurposed for a condition
    """
    medicines = await hf_service.search_medicines_by_condition(condition)
    return {"medicines": medicines, "count": len(medicines)}

@app.get("/api/medicines/{drug_name}/details")
async def get_medicine_details(drug_name: str):
    """
    Get comprehensive details about a medicine
    """
    details = await hf_service.get_medicine_details(drug_name)
    if details:
        return {"details": details, "found": True}
    return {"details": None, "found": False}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

