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
from services.medical_supplies_service import MedicalSuppliesService
from services.medicine_dataset_service import MedicineDatasetService
from services.database_service import MongoDBService


load_dotenv()

app = FastAPI(
    title="Drug Repurposing AI Platform",
    description="AI-powered drug repurposing analysis API",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173", 
        "http://localhost:5174",  # Added for Vite alternate port
        "http://localhost:3000", 
        "http://127.0.0.1:5173",
        "http://127.0.0.1:5174"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize AI Analyzer, Hugging Face Service, Medical Supplies Service, and CSV Dataset Service
ai_analyzer = AIDrugRepurposingAnalyzer()
hf_service = HuggingFaceMedicineService()
supplies_service = MedicalSuppliesService()
medicine_dataset = MedicineDatasetService()

# Request/Response Models
class RepurposingRequest(BaseModel):
    drug_name: Optional[str] = None
    target_condition: Optional[str] = None
    analyze_ingredients: bool = False  # Case 4: Ingredient analysis mode

# Case-specific request models
class Case1Request(BaseModel):
    """Case 1: Have drug, find diseases"""
    drug_name: str

class Case2Request(BaseModel):
    """Case 2: Have disease, find drugs"""
    target_condition: str

class Case3Request(BaseModel):
    """Case 3: Have both drug and disease"""
    drug_name: str
    target_condition: str

class Case4Request(BaseModel):
    """Case 4: Ingredient analysis"""
    drug_name: str

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

@app.post("/api/analyze")
async def analyze_repurposing(request: RepurposingRequest):
    """
    Analyze drug repurposing potential using AI
    
    Cases supported:
    - Case 1: drug_name only → Find diseases for this drug
    - Case 2: target_condition only → Find drugs for this disease
    - Case 3: Both drug_name and target_condition → Full analysis
    - Case 4: drug_name + analyze_ingredients=True → Ingredient analysis
    """
    try:
        # Validate - at least one field required
        if not request.drug_name and not request.target_condition:
            raise HTTPException(
                status_code=400,
                detail="Either drug_name or target_condition is required"
            )

        # Perform AI-powered analysis based on case
        analysis_result = await ai_analyzer.analyze(
            drug_name=request.drug_name or "",
            target_condition=request.target_condition or "",
            analyze_ingredients=request.analyze_ingredients
        )
        
        # For Cases 1, 2, 4 - return flexible response
        case_type = analysis_result.get("case_type", "")
        if case_type in ["CASE_1_DRUG_ONLY", "CASE_2_DISEASE_ONLY", "CASE_4_INGREDIENT_ANALYSIS"]:
            return analysis_result
        
        # For Case 3 - ensure all required fields for RepurposingResponse
        if not analysis_result.get("research_papers"):
            analysis_result["research_papers"] = []
        if not analysis_result.get("clinical_trials"):
            analysis_result["clinical_trials"] = []
        if not analysis_result.get("patents"):
            analysis_result["patents"] = []
        if not analysis_result.get("recommendations"):
            analysis_result["recommendations"] = ["Analysis completed"]
        if not analysis_result.get("market_feasibility"):
            analysis_result["market_feasibility"] = {
                "market_size": "To be determined",
                "growth_rate": "Market analysis required",
                "competition": "Assessment needed",
                "regulatory_path": "FDA IND required",
                "timeline": "36-48 months"
            }

        return analysis_result

    except Exception as e:
        import traceback
        print(f"❌ ERROR in analyze_repurposing: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(
            status_code=500,
            detail=f"Analysis failed: {str(e)}"
        )

# ==================== CASE-SPECIFIC ENDPOINTS ====================

@app.post("/api/analyze/case1")
async def case1_find_diseases(request: Case1Request):
    """
    Case 1: Have drug, find potential diseases it could treat
    
    Request body:
    {
        "drug_name": "string"
    }
    """
    result = await ai_analyzer.analyze(
        drug_name=request.drug_name, 
        target_condition="", 
        analyze_ingredients=False
    )
    return result

@app.post("/api/analyze/case2")
async def case2_find_drugs(request: Case2Request):
    """
    Case 2: Have disease, find best drug candidates
    
    Request body:
    {
        "target_condition": "string"
    }
    """
    result = await ai_analyzer.analyze(
        drug_name="", 
        target_condition=request.target_condition, 
        analyze_ingredients=False
    )
    return result

@app.post("/api/analyze/case3")
async def case3_full_analysis(request: Case3Request):
    """
    Case 3: Have both drug and disease, full repurposing analysis
    
    Request body:
    {
        "drug_name": "string",
        "target_condition": "string"
    }
    """
    result = await ai_analyzer.analyze(
        drug_name=request.drug_name, 
        target_condition=request.target_condition, 
        analyze_ingredients=False
    )
    return result

@app.post("/api/analyze/case4")
async def case4_ingredient_analysis(request: Case4Request):
    """
    Case 4: Analyze drug ingredients for effectiveness in other areas
    
    Request body:
    {
        "drug_name": "string"
    }
    """
    result = await ai_analyzer.analyze(
        drug_name=request.drug_name, 
        target_condition="", 
        analyze_ingredients=True
    )
    return result

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

@app.get("/api/supplies")
async def get_all_supplies():
    """
    Get all medical supplies in the database
    """
    supplies = supplies_service.get_all_supplies()
    return {"supplies": supplies, "count": len(supplies)}

@app.get("/api/supplies/search")
async def search_supplies(query: str):
    """
    Search for medical supplies by name, category, or description
    """
    results = supplies_service.search_supply(query)
    return {"supplies": results, "count": len(results)}

@app.get("/api/supplies/for-condition")
async def get_supplies_for_condition(condition: str):
    """
    Get medical supplies needed for a specific condition
    """
    supplies = supplies_service.get_supplies_for_condition(condition)
    cost_info = supplies_service.calculate_supply_cost(supplies)
    return {
        "condition": condition,
        "supplies": supplies,
        "count": len(supplies),
        "cost_analysis": cost_info
    }

@app.get("/api/supplies/for-drug-class")
async def get_supplies_for_drug_class(drug_class: str):
    """
    Get medical supplies needed for a specific drug class
    """
    supplies = supplies_service.get_supplies_for_drug_class(drug_class)
    cost_info = supplies_service.calculate_supply_cost(supplies)
    return {
        "drug_class": drug_class,
        "supplies": supplies,
        "count": len(supplies),
        "cost_analysis": cost_info
    }

@app.get("/api/dataset/search")
async def search_dataset(drug_name: str = None, indication: str = None):
    """
    Search the medicine_dataset.csv file
    """
    if drug_name:
        results = await medicine_dataset.search_drug(drug_name)
        return {"query": drug_name, "type": "drug", "results": results, "count": len(results)}
    elif indication:
        results = await medicine_dataset.search_by_indication(indication)
        return {"query": indication, "type": "indication", "results": results, "count": len(results)}
    else:
        return {"error": "Please provide either drug_name or indication parameter"}

@app.get("/api/dataset/drug/{drug_name}")
async def get_drug_from_dataset(drug_name: str):
    """
    Get comprehensive drug details from CSV dataset
    """
    drug_data = await medicine_dataset.get_drug_details(drug_name)
    if drug_data:
        return {"drug": drug_data, "found": True}
    return {"drug": None, "found": False}

@app.get("/api/dataset/repurposing")
async def check_repurposing_opportunity(drug_name: str, target_condition: str):
    """
    Check repurposing opportunities using CSV data
    """
    opportunity = await medicine_dataset.find_repurposing_opportunities(drug_name, target_condition)
    return {
        "drug_name": drug_name,
        "target_condition": target_condition,
        "opportunity": opportunity
    }

@app.get("/api/dataset/statistics")
async def get_dataset_statistics():
    """
    Get statistics about the CSV dataset
    """
    stats = await medicine_dataset.get_statistics()
    return {"statistics": stats}

# ==================== MONGODB ENDPOINTS ====================

# Initialize MongoDB service
mongodb_service = MongoDBService()

@app.on_event("startup")
async def startup_event():
    """Initialize MongoDB connection on startup"""
    csv_path = os.path.join(os.path.dirname(__file__), "services", "medicine_dataset.csv")
    if mongodb_service.connect_sync():
        mongodb_service.load_csv_to_mongodb(csv_path)
        await mongodb_service.connect_async()
        print("  ✅ MongoDB ready!")
    else:
        print("  ⚠️ MongoDB not available - using CSV fallback")

@app.get("/api/db/search")
async def db_search_drug(query: str, limit: int = 10):
    """
    Search drugs in MongoDB
    """
    if not mongodb_service.is_connected:
        raise HTTPException(status_code=503, detail="MongoDB not connected")
    
    results = await mongodb_service.search_drug(query, limit)
    return {"query": query, "results": results, "count": len(results)}

@app.get("/api/db/drug/{drug_name}")
async def db_get_drug(drug_name: str):
    """
    Get drug details from MongoDB
    """
    if not mongodb_service.is_connected:
        raise HTTPException(status_code=503, detail="MongoDB not connected")
    
    details = await mongodb_service.get_drug_details(drug_name)
    if not details:
        raise HTTPException(status_code=404, detail=f"Drug {drug_name} not found")
    return details

@app.get("/api/db/indication/{indication}")
async def db_search_by_indication(indication: str, limit: int = 20):
    """
    Find drugs by indication in MongoDB
    """
    if not mongodb_service.is_connected:
        raise HTTPException(status_code=503, detail="MongoDB not connected")
    
    results = await mongodb_service.search_by_indication(indication, limit)
    return {"indication": indication, "results": results, "count": len(results)}

@app.get("/api/db/category/{category}")
async def db_search_by_category(category: str, limit: int = 20):
    """
    Find drugs by category in MongoDB
    """
    if not mongodb_service.is_connected:
        raise HTTPException(status_code=503, detail="MongoDB not connected")
    
    results = await mongodb_service.search_by_category(category, limit)
    return {"category": category, "results": results, "count": len(results)}

@app.get("/api/db/repurposing")
async def db_check_repurposing(drug_name: str, target_condition: str):
    """
    Check repurposing opportunity in MongoDB
    """
    if not mongodb_service.is_connected:
        raise HTTPException(status_code=503, detail="MongoDB not connected")
    
    result = await mongodb_service.find_repurposing_opportunities(drug_name, target_condition)
    return result

@app.get("/api/db/statistics")
async def db_get_statistics():
    """
    Get MongoDB statistics
    """
    if not mongodb_service.is_connected:
        raise HTTPException(status_code=503, detail="MongoDB not connected")
    
    stats = await mongodb_service.get_statistics()
    return stats

@app.get("/api/db/status")
async def db_status():
    """
    Check MongoDB connection status
    """
    return {
        "connected": mongodb_service.is_connected,
        "database": mongodb_service.database_name,
        "collection": mongodb_service.collection_name
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

