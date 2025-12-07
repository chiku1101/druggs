"""
Multi-Agent Orchestrator for Drug Repurposing Analysis
Coordinates specialized agents running in parallel

CASE TYPES:
- Case 1 (DRUG_ONLY): Have drug/molecule but no target disease → Find potential diseases
- Case 2 (DISEASE_ONLY): Know disease but no drug → Find best drug candidates  
- Case 3 (DRUG_AND_DISEASE): Have both drug and disease → Full repurposing analysis
- Case 4 (INGREDIENT_ANALYSIS): Analyze drug ingredients for other uses
"""

import asyncio
from typing import Dict, List, Optional, Any
from enum import Enum
import json


class CaseType(Enum):
    """
    Case detection types based on user input
    """
    DRUG_ONLY = 1            # Case 1: Have drug, find diseases
    DISEASE_ONLY = 2         # Case 2: Have disease, find drugs
    DRUG_AND_DISEASE = 3     # Case 3: Have both, full analysis
    INGREDIENT_ANALYSIS = 4  # Case 4: Analyze drug ingredients


class MultiAgentOrchestrator:
    """
    Orchestrates multiple specialized agents running in parallel
    Based on the architecture diagram
    """
    
    def __init__(self, agents_pool: Dict[str, Any]):
        self.agents_pool = agents_pool
        self.case_type = None
        self.agent_results = {}
        print("✅ Multi-Agent Orchestrator initialized")
    
    def detect_case(self, drug_name: Optional[str], target_condition: Optional[str], 
                     analyze_ingredients: bool = False) -> CaseType:
        """
        Case Detection Logic:
        - Case 1: Drug only → Find potential diseases
        - Case 2: Disease only → Find best drug candidates
        - Case 3: Both drug and disease → Full repurposing analysis
        - Case 4: Ingredient analysis mode → Analyze drug components
        """
        if analyze_ingredients and drug_name:
            return CaseType.INGREDIENT_ANALYSIS
        elif drug_name and target_condition:
            return CaseType.DRUG_AND_DISEASE
        elif drug_name and not target_condition:
            return CaseType.DRUG_ONLY
        elif not drug_name and target_condition:
            return CaseType.DISEASE_ONLY
        else:
            # Default to drug analysis if nothing provided
            return CaseType.DRUG_ONLY
    
    async def orchestrate(self, drug_name: Optional[str], target_condition: Optional[str],
                         analyze_ingredients: bool = False) -> Dict:
        """
        Main orchestration method - runs agents based on case type
        
        Cases:
        - Case 1 (DRUG_ONLY): Find diseases for a drug
        - Case 2 (DISEASE_ONLY): Find drugs for a disease
        - Case 3 (DRUG_AND_DISEASE): Full repurposing analysis
        - Case 4 (INGREDIENT_ANALYSIS): Analyze drug ingredients
        """
        # Step 1: Case Detection
        self.case_type = self.detect_case(drug_name, target_condition, analyze_ingredients)
        print(f"🔍 Case Type Detected: {self.case_type.name}")
        
        # Step 2: Execute appropriate flow based on case
        print("🤖 Launching Multi-Agent System...")
        
        if self.case_type == CaseType.DRUG_ONLY:
            # Case 1: Have drug, find diseases
            return await self._execute_case1_drug_only(drug_name)
        elif self.case_type == CaseType.DISEASE_ONLY:
            # Case 2: Have disease, find drugs
            return await self._execute_case2_disease_only(target_condition)
        elif self.case_type == CaseType.DRUG_AND_DISEASE:
            # Case 3: Have both, full analysis
            return await self._execute_case3_full_analysis(drug_name, target_condition)
        elif self.case_type == CaseType.INGREDIENT_ANALYSIS:
            # Case 4: Analyze ingredients
            return await self._execute_case4_ingredient_analysis(drug_name)
        else:
            return await self._execute_case3_full_analysis(drug_name, target_condition)
    
    # ==================== CASE 1: DRUG ONLY ====================
    async def _execute_case1_drug_only(self, drug_name: str) -> Dict:
        """
        Case 1: Have drug/molecule but no target disease
        → Find potential diseases this drug could treat
        """
        print(f"  📊 Case 1: Finding potential diseases for {drug_name}")
        
        # Get drug details from MongoDB
        research_agent = self.agents_pool.get("research_agent")
        db = research_agent.db if research_agent else None
        
        drug_data = {}
        potential_diseases = []
        
        if db:
            # Get drug info from database
            drug_data = await db.get_drug_details(drug_name)
            
            if drug_data:
                # Current indication is already known
                current_indications = drug_data.get("indications", [])
                category = drug_data.get("category", "")
                
                # Find other drugs in same category to suggest diseases
                similar_drugs = await db.search_by_category(category, limit=20)
                
                # Collect all indications from similar drugs
                all_indications = set()
                for drug in similar_drugs:
                    indication = drug.get("Indication", "")
                    if indication:
                        all_indications.add(indication)
                
                # Remove current indications to find NEW potential uses
                for ind in current_indications:
                    all_indications.discard(ind)
                
                potential_diseases = [
                    {
                        "disease": ind,
                        "confidence": 75,
                        "rationale": f"Other {category} drugs are used for this condition"
                    }
                    for ind in list(all_indications)[:10]
                ]
        
        return {
            "case_type": "CASE_1_DRUG_ONLY",
            "drug_name": drug_name,
            "drug_data": drug_data,
            "current_indications": drug_data.get("indications", []) if drug_data else [],
            "potential_new_diseases": potential_diseases,
            "repurposeability_score": 70 if potential_diseases else 40,
            "verdict": "EXPLORE" if potential_diseases else "LIMITED DATA",
            "recommendations": [
                f"🔬 {drug_name} is a {drug_data.get('category', 'Unknown')} drug",
                f"📋 Current uses: {', '.join(drug_data.get('indications', ['Unknown']))}",
                f"💡 Found {len(potential_diseases)} potential new disease targets",
                "🧪 Further research recommended for each potential target"
            ] if drug_data else [f"⚠️ {drug_name} not found in database"],
            "analysis_metadata": {
                "case_type": "DRUG_ONLY",
                "data_source": "MongoDB Atlas"
            }
        }
    
    # ==================== CASE 2: DISEASE ONLY ====================
    async def _execute_case2_disease_only(self, disease: str) -> Dict:
        """
        Case 2: Know disease but no drug
        → Find best drug candidates for this disease
        """
        print(f"  📊 Case 2: Finding drug candidates for {disease}")
        
        research_agent = self.agents_pool.get("research_agent")
        db = research_agent.db if research_agent else None
        
        drug_candidates = []
        
        if db:
            # Search for drugs that treat this disease
            drugs = await db.search_by_indication(disease, limit=20)
            
            for drug in drugs:
                drug_candidates.append({
                    "drug_name": drug.get("Name", "Unknown"),
                    "category": drug.get("Category", "Unknown"),
                    "dosage_form": drug.get("Dosage Form", "Unknown"),
                    "strength": drug.get("Strength", "Unknown"),
                    "manufacturer": drug.get("Manufacturer", "Unknown"),
                    "classification": drug.get("Classification", "Unknown"),
                    "confidence": 90,
                    "source": "MongoDB Atlas"
                })
        
        # Rank candidates
        ranked_candidates = sorted(drug_candidates, key=lambda x: x["confidence"], reverse=True)
        
        return {
            "case_type": "CASE_2_DISEASE_ONLY",
            "target_condition": disease,
            "drug_candidates": ranked_candidates[:10],
            "total_candidates_found": len(drug_candidates),
            "repurposeability_score": 85 if drug_candidates else 30,
            "verdict": "MULTIPLE OPTIONS" if len(drug_candidates) > 5 else "LIMITED OPTIONS" if drug_candidates else "NO MATCHES",
            "recommendations": [
                f"🏥 Disease: {disease}",
                f"💊 Found {len(drug_candidates)} drug candidates",
                f"✅ Top candidate: {ranked_candidates[0]['drug_name']}" if ranked_candidates else "❌ No candidates found",
                "📋 Review each candidate for safety and efficacy"
            ],
            "analysis_metadata": {
                "case_type": "DISEASE_ONLY",
                "data_source": "MongoDB Atlas",
                "search_method": "indication_match"
            }
        }
    
    # ==================== CASE 3: FULL ANALYSIS ====================
    async def _execute_case3_full_analysis(self, drug_name: str, target_condition: str) -> Dict:
        """
        Case 3: Have both drug and disease
        → Full repurposing analysis with all agents
        """
        print(f"  📊 Case 3: Full analysis for {drug_name} → {target_condition}")
        return await self._execute_multi_agent_flow(drug_name, target_condition)
    
    # ==================== CASE 4: INGREDIENT ANALYSIS ====================
    async def _execute_case4_ingredient_analysis(self, drug_name: str) -> Dict:
        """
        Case 4: Analyze drug ingredients for effectiveness in other areas
        → Break down drug into components and find alternative uses
        """
        print(f"  📊 Case 4: Analyzing ingredients of {drug_name}")
        
        research_agent = self.agents_pool.get("research_agent")
        db = research_agent.db if research_agent else None
        
        drug_data = {}
        ingredient_analysis = []
        alternative_uses = []
        
        if db:
            drug_data = await db.get_drug_details(drug_name)
            
            if drug_data:
                category = drug_data.get("category", "")
                current_indication = drug_data.get("indications", ["Unknown"])[0] if drug_data.get("indications") else "Unknown"
                
                # Analyze based on drug category (ingredient class)
                ingredient_analysis = [
                    {
                        "ingredient_class": category,
                        "mechanism": self._get_mechanism_for_category(category),
                        "properties": self._get_properties_for_category(category)
                    }
                ]
                
                # Find all other uses for this drug category
                similar_drugs = await db.search_by_category(category, limit=50)
                
                indication_counts = {}
                for drug in similar_drugs:
                    ind = drug.get("Indication", "")
                    if ind and ind != current_indication:
                        indication_counts[ind] = indication_counts.get(ind, 0) + 1
                
                # Sort by frequency
                sorted_indications = sorted(indication_counts.items(), key=lambda x: x[1], reverse=True)
                
                alternative_uses = [
                    {
                        "indication": ind,
                        "evidence_count": count,
                        "confidence": min(95, 50 + count * 5),
                        "rationale": f"{count} other {category} drugs treat this condition"
                    }
                    for ind, count in sorted_indications[:10]
                ]
        
        return {
            "case_type": "CASE_4_INGREDIENT_ANALYSIS",
            "drug_name": drug_name,
            "drug_data": drug_data,
            "ingredient_analysis": ingredient_analysis,
            "current_indication": drug_data.get("indications", ["Unknown"])[0] if drug_data and drug_data.get("indications") else "Unknown",
            "alternative_uses": alternative_uses,
            "repurposeability_score": 80 if alternative_uses else 50,
            "verdict": "HIGH REPURPOSING POTENTIAL" if len(alternative_uses) > 5 else "MODERATE POTENTIAL" if alternative_uses else "LIMITED DATA",
            "recommendations": [
                f"🧬 Drug: {drug_name}",
                f"📦 Category: {drug_data.get('category', 'Unknown')}" if drug_data else "",
                f"💊 Current use: {drug_data.get('indications', ['Unknown'])[0] if drug_data and drug_data.get('indications') else 'Unknown'}",
                f"🔬 Found {len(alternative_uses)} potential alternative uses",
                f"✅ Best alternative: {alternative_uses[0]['indication']} ({alternative_uses[0]['confidence']}% confidence)" if alternative_uses else "❌ No alternatives found"
            ],
            "analysis_metadata": {
                "case_type": "INGREDIENT_ANALYSIS",
                "data_source": "MongoDB Atlas",
                "analysis_method": "category_based_repurposing"
            }
        }
    
    def _get_mechanism_for_category(self, category: str) -> str:
        """Get mechanism of action for drug category"""
        mechanisms = {
            "Antibiotic": "Inhibits bacterial cell wall synthesis or protein synthesis",
            "Antiviral": "Blocks viral replication or entry into cells",
            "Antifungal": "Disrupts fungal cell membrane integrity",
            "Antidiabetic": "Regulates glucose metabolism and insulin sensitivity",
            "Analgesic": "Blocks pain signal transmission",
            "Anti-inflammatory": "Reduces inflammatory mediators",
            "Antihypertensive": "Reduces blood pressure through various pathways",
            "Antihistamine": "Blocks histamine receptors"
        }
        return mechanisms.get(category, f"Mechanism specific to {category} class")
    
    def _get_properties_for_category(self, category: str) -> List[str]:
        """Get properties for drug category"""
        properties = {
            "Antibiotic": ["Bactericidal", "Bacteriostatic", "Broad/Narrow spectrum"],
            "Antiviral": ["Viral inhibition", "Immune modulation"],
            "Antifungal": ["Fungicidal", "Fungistatic"],
            "Antidiabetic": ["Glucose regulation", "Insulin sensitivity"],
            "Analgesic": ["Pain relief", "Anti-pyretic"],
            "Anti-inflammatory": ["COX inhibition", "Cytokine modulation"],
            "Antihypertensive": ["Vasodilation", "Diuretic effect"],
            "Antihistamine": ["H1 blocking", "Sedative/Non-sedative"]
        }
        return properties.get(category, ["Category-specific properties"])
    
    async def _execute_multi_agent_flow(self, drug_name: str, target_condition: str) -> Dict:
        """
        Execute agents in parallel (Cases 1, 2, 3)
        """
        # Launch all agents in parallel
        agent_tasks = [
            self._run_research_agent(drug_name, target_condition),
            self._run_trials_agent(drug_name, target_condition),
            self._run_patent_agent(drug_name, target_condition),
            self._run_regulatory_agent(drug_name, target_condition),
            self._run_market_agent(drug_name, target_condition)
        ]
        
        print("  → Research Agent: Searching PubMed, PubChem...")
        print("  → Trials Agent: Querying ClinicalTrials.gov...")
        print("  → Patent Agent: Searching Google Patents...")
        print("  → Regulatory Agent: Checking FDA/EXIM...")
        print("  → Market Agent: Analyzing pricing & trends...")
        
        # Execute all agents in parallel
        results = await asyncio.gather(*agent_tasks, return_exceptions=True)
        
        # Store normalized results
        self.agent_results = {
            "research": results[0] if not isinstance(results[0], Exception) else {},
            "trials": results[1] if not isinstance(results[1], Exception) else {},
            "patents": results[2] if not isinstance(results[2], Exception) else {},
            "regulatory": results[3] if not isinstance(results[3], Exception) else {},
            "market": results[4] if not isinstance(results[4], Exception) else {}
        }
        
        print("✅ All agents completed")
        
        # Step 3: Normalize to JSON Pool
        normalized_data = self._normalize_agent_outputs()
        
        # Step 4: Scoring Engine
        score = self._calculate_weighted_score(normalized_data)
        
        # Step 5: Decision & Recommendation
        decision = self._make_decision(score, normalized_data)
        
        # Step 6: Generate final report structure
        return self._generate_report_structure(drug_name, target_condition, normalized_data, score, decision)
    
    async def _run_research_agent(self, drug_name: str, target_condition: str) -> Dict:
        """
        Research Agent: Searches PubMed, PubChem, scientific literature
        """
        agent = self.agents_pool.get("research_agent")
        if agent:
            return await agent.execute(drug_name, target_condition)
        return {"status": "completed", "papers": []}
    
    async def _run_trials_agent(self, drug_name: str, target_condition: str) -> Dict:
        """
        Trials Agent: Queries ClinicalTrials.gov
        """
        agent = self.agents_pool.get("trials_agent")
        if agent:
            return await agent.execute(drug_name, target_condition)
        return {"status": "completed", "trials": []}
    
    async def _run_patent_agent(self, drug_name: str, target_condition: str) -> Dict:
        """
        Patent Agent: Searches Google Patents
        """
        agent = self.agents_pool.get("patent_agent")
        if agent:
            return await agent.execute(drug_name, target_condition)
        return {"status": "completed", "patents": []}
    
    async def _run_regulatory_agent(self, drug_name: str, target_condition: str) -> Dict:
        """
        Regulatory Agent: Checks FDA status, EXIM data, regulatory flags
        """
        agent = self.agents_pool.get("regulatory_agent")
        if agent:
            return await agent.execute(drug_name, target_condition)
        return {"status": "completed", "regulatory": {}}
    
    async def _run_market_agent(self, drug_name: str, target_condition: str) -> Dict:
        """
        Market Agent: Analyzes pricing, market trends, feasibility
        """
        agent = self.agents_pool.get("market_agent")
        if agent:
            return await agent.execute(drug_name, target_condition)
        return {"status": "completed", "market": {}}
    
    async def _execute_trend_analytics(self) -> Dict:
        """
        Trend Intelligence (Case 4): No input, analyze market trends
        """
        print("📊 Executing Trend Analytics (Case 4)...")
        
        agent = self.agents_pool.get("trend_agent")
        if agent:
            trends = await agent.execute()
            return {
                "case_type": "TREND_INTELLIGENCE",
                "trends": trends,
                "recommendations": ["Top emerging repurposing opportunities"]
            }
        
        return {"case_type": "TREND_INTELLIGENCE", "trends": []}
    
    def _normalize_agent_outputs(self) -> Dict:
        """
        Agent Output Store: Normalize all agent results to JSON pool
        """
        research_result = self.agent_results.get("research", {})
        return {
            "research_data": {
                "papers_count": len(research_result.get("papers", [])),
                "papers": research_result.get("papers", []),
                "evidence_quality": self._assess_research_quality(),
                "db_data": research_result.get("db_data"),  # Include CSV data
                "data_source": research_result.get("data_source", "Unknown")
            },
            "trials_data": {
                "trials_count": len(self.agent_results.get("trials", {}).get("trials", [])),
                "trials": self.agent_results.get("trials", {}).get("trials", []),
                "trial_phases": self._extract_trial_phases(),
                "db_evidence": self.agent_results.get("trials", {}).get("db_evidence", {}),
                "data_source": self.agent_results.get("trials", {}).get("data_source", "Unknown")
            },
            "patent_data": {
                "patents_count": len(self.agent_results.get("patents", {}).get("patents", [])),
                "patents": self.agent_results.get("patents", {}).get("patents", []),
                "ip_protection": self._assess_ip_landscape()
            },
            "regulatory_data": {
                "fda_status": self.agent_results.get("regulatory", {}).get("fda_approved", False),
                "regulatory_path": self.agent_results.get("regulatory", {}).get("pathway", "Unknown"),
                "barriers": self.agent_results.get("regulatory", {}).get("barriers", []),
                "db_classification": self.agent_results.get("regulatory", {}).get("db_classification", ""),
                "db_manufacturers": self.agent_results.get("regulatory", {}).get("db_manufacturers", []),
                "data_source": self.agent_results.get("regulatory", {}).get("data_source", "Unknown")
            },
            "market_data": {
                "market_size": self.agent_results.get("market", {}).get("market_size", "To be determined"),
                "growth_rate": self.agent_results.get("market", {}).get("growth_rate", "Market analysis required"),
                "competition": self.agent_results.get("market", {}).get("competition", "Assessment needed"),
                "regulatory_path": self.agent_results.get("market", {}).get("regulatory_path", 
                    self.agent_results.get("regulatory", {}).get("pathway", "FDA IND required")),
                "timeline": self.agent_results.get("market", {}).get("timeline", "36-48 months"),
                "pricing": self.agent_results.get("market", {}).get("pricing", {})
            }
        }
    
    def _calculate_weighted_score(self, normalized_data: Dict) -> int:
        """
        Scoring Engine: Calculate weighted score (0-100)
        Weights: science/trial/IP/regulatory/market
        """
        weights = {
            "science": 0.30,      # 30% - Scientific evidence
            "trials": 0.25,       # 25% - Clinical trial data
            "ip": 0.15,           # 15% - IP/Patent landscape
            "regulatory": 0.20,   # 20% - Regulatory feasibility
            "market": 0.10        # 10% - Market potential
        }
        
        # Science Score (0-100)
        science_score = self._score_scientific_evidence(normalized_data["research_data"])
        
        # Trials Score (0-100)
        trials_score = self._score_clinical_trials(normalized_data["trials_data"])
        
        # IP Score (0-100)
        ip_score = self._score_ip_landscape(normalized_data["patent_data"])
        
        # Regulatory Score (0-100)
        regulatory_score = self._score_regulatory(normalized_data["regulatory_data"])
        
        # Market Score (0-100)
        market_score = self._score_market(normalized_data["market_data"])
        
        # Calculate weighted total
        total_score = (
            science_score * weights["science"] +
            trials_score * weights["trials"] +
            ip_score * weights["ip"] +
            regulatory_score * weights["regulatory"] +
            market_score * weights["market"]
        )
        
        print(f"\n📊 Scoring Breakdown:")
        print(f"  Science: {science_score}/100 (weight: {weights['science']*100}%)")
        print(f"  Trials: {trials_score}/100 (weight: {weights['trials']*100}%)")
        print(f"  IP: {ip_score}/100 (weight: {weights['ip']*100}%)")
        print(f"  Regulatory: {regulatory_score}/100 (weight: {weights['regulatory']*100}%)")
        print(f"  Market: {market_score}/100 (weight: {weights['market']*100}%)")
        print(f"  ⭐ Final Score: {int(total_score)}/100")
        
        return int(total_score)
    
    def _score_scientific_evidence(self, research_data: Dict) -> int:
        """Score based on research papers and evidence quality"""
        score = 50  # Base score
        
        # Check if CSV data exists (real evidence)
        if research_data.get("db_data"):
            db_data = research_data.get("db_data", {})
            score += 25  # CSV data = real evidence
            if db_data.get("record_count", 0) > 1:
                score += 10  # Multiple records = stronger evidence
            if db_data.get("indications"):
                score += 10  # Has indications = documented use
        
        papers_count = research_data.get("papers_count", 0)
        score += min(papers_count * 5, 30)  # Up to +30 for papers
        
        if research_data.get("evidence_quality") == "high":
            score += 20
        elif research_data.get("evidence_quality") == "medium":
            score += 10
        
        return min(score, 100)
    
    def _score_clinical_trials(self, trials_data: Dict) -> int:
        """Score based on clinical trials"""
        score = 40  # Base score
        
        # Check if already approved in CSV
        db_evidence = trials_data.get("db_evidence", {})
        if db_evidence.get("already_approved"):
            score += 50  # Already approved = very high score!
            return min(score, 100)
        
        trials_count = trials_data.get("trials_count", 0)
        score += min(trials_count * 10, 30)  # Up to +30
        
        phases = trials_data.get("trial_phases", [])
        if "Phase 3" in phases:
            score += 30
        elif "Phase 2" in phases:
            score += 20
        elif "Phase 1" in phases:
            score += 10
        
        return min(score, 100)
    
    def _score_ip_landscape(self, patent_data: Dict) -> int:
        """Score based on patent landscape"""
        score = 60  # Base score
        
        patents_count = patent_data.get("patents_count", 0)
        if patents_count > 0:
            score += 20
        
        ip_protection = patent_data.get("ip_protection", "none")
        if ip_protection == "strong":
            score += 20
        elif ip_protection == "moderate":
            score += 10
        
        return min(score, 100)
    
    def _score_regulatory(self, regulatory_data: Dict) -> int:
        """Score based on regulatory status"""
        score = 40  # Base score
        
        # Check CSV classification (Prescription/OTC = approved)
        if regulatory_data.get("db_classification"):
            score += 35  # CSV shows it's classified/approved
            if "Prescription" in regulatory_data.get("db_classification", ""):
                score += 5  # Prescription = FDA approved
        
        if regulatory_data.get("fda_status"):
            score += 40
        
        pathway = regulatory_data.get("regulatory_path", "Unknown")
        if "505(b)(2)" in pathway or "Fast Track" in pathway:
            score += 20
        
        return min(score, 100)
    
    def _score_market(self, market_data: Dict) -> int:
        """Score based on market potential"""
        score = 50  # Base score
        
        market_size = market_data.get("market_size", "Unknown")
        if "B" in str(market_size):  # Billions
            score += 30
        elif "M" in str(market_size):  # Millions
            score += 20
        
        competition = market_data.get("competition", "Unknown")
        if competition == "Low":
            score += 20
        elif competition == "Moderate":
            score += 10
        
        return min(score, 100)
    
    def _make_decision(self, score: int, normalized_data: Dict) -> Dict:
        """
        Decision & Recommendation: Go/No-Go verdict
        """
        # Check if already approved in CSV (highest priority)
        db_evidence = normalized_data.get("trials_data", {}).get("db_evidence", {})
        if db_evidence.get("already_approved"):
            verdict = "STRONG GO"
            confidence = "Very High"
            recommendation = f"✅ ALREADY APPROVED: This drug is documented in the dataset for this condition. Strong evidence for repurposing with existing approval status."
            score = max(score, 90)  # Boost score to 90+ if already approved
        elif score >= 80:
            verdict = "STRONG GO"
            confidence = "High"
            recommendation = "Highly recommended for repurposing. Strong evidence across all dimensions."
        elif score >= 65:
            verdict = "GO"
            confidence = "Moderate-High"
            recommendation = "Recommended for repurposing with further validation."
        elif score >= 50:
            verdict = "CONDITIONAL GO"
            confidence = "Moderate"
            recommendation = "Proceed with caution. Additional research recommended."
        else:
            verdict = "NO-GO"
            confidence = "Low"
            recommendation = "Not recommended. Insufficient evidence for repurposing."
        
        return {
            "verdict": verdict,
            "confidence": confidence,
            "recommendation": recommendation,
            "score": score
        }
    
    def _generate_report_structure(self, drug_name: str, target_condition: str, 
                                   normalized_data: Dict, score: int, decision: Dict) -> Dict:
        """
        Generate final report structure for PDF Report Generator
        """
        # Store drug_name and target_condition in normalized_data for recommendations
        normalized_data["drug_name"] = drug_name
        normalized_data["target_condition"] = target_condition
        
        # Safely get data with defaults
        research_data = normalized_data.get("research_data", {})
        trials_data = normalized_data.get("trials_data", {})
        patent_data = normalized_data.get("patent_data", {})
        regulatory_data = normalized_data.get("regulatory_data", {})
        market_data = normalized_data.get("market_data", {})
        
        return {
            "drug_name": drug_name,
            "target_condition": target_condition,
            "case_type": self.case_type.name if self.case_type else "UNKNOWN",
            "repurposeability_score": score,
            "verdict": decision.get("verdict", "UNKNOWN"),
            "confidence": decision.get("confidence", "Unknown"),
            
            # From agents (with safe defaults)
            "research_papers": research_data.get("papers", []),
            "clinical_trials": trials_data.get("trials", []),
            "patents": patent_data.get("patents", []),
            "regulatory_status": regulatory_data,
            "market_feasibility": {
                "market_size": market_data.get("market_size", "To be determined"),
                "growth_rate": market_data.get("growth_rate", "Market analysis required"),
                "competition": market_data.get("competition", "Assessment needed"),
                "regulatory_path": regulatory_data.get("regulatory_path", regulatory_data.get("pathway", market_data.get("regulatory_path", "FDA IND required"))),
                "timeline": market_data.get("timeline", "36-48 months")
            },
            
            # CSV Data (NEW - shows real data from dataset)
            "db_drug_data": research_data.get("db_data"),
            
            # Drug Usage Information (NEW - comprehensive usage details)
            "drug_usage_info": self._generate_drug_usage_info(drug_name, target_condition, normalized_data),
            
            # Recommendations
            "recommendations": self._generate_final_recommendations(decision, normalized_data),
            
            # Metadata
            "analysis_metadata": {
                "case_type": self.case_type.name if self.case_type else "UNKNOWN",
                "agents_executed": list(self.agent_results.keys()),
                "scoring_weights": {
                    "science": "30%",
                    "trials": "25%",
                    "ip": "15%",
                    "regulatory": "20%",
                    "market": "10%"
                },
                "orchestration": "Multi-Agent Parallel Execution",
                "data_sources": [
                    research_data.get("data_source", "Unknown"),
                    trials_data.get("data_source", "Unknown"),
                    regulatory_data.get("data_source", "Unknown")
                ]
            }
        }
    
    def _generate_final_recommendations(self, decision: Dict, normalized_data: Dict) -> List[str]:
        """Generate final recommendations"""
        recommendations = [decision.get("recommendation", "Analysis completed")]
        
        # Safely get drug_name and target_condition
        drug_name = normalized_data.get("drug_name", "This drug")
        target_condition = normalized_data.get("target_condition", "the condition")
        
        # Check CSV data first (most important)
        trials_data = normalized_data.get("trials_data", {})
        db_evidence = trials_data.get("db_evidence", {})
        if db_evidence.get("already_approved"):
            record_count = db_evidence.get("record_count", 0)
            recommendations.insert(0, f"✅ {drug_name} is ALREADY APPROVED for {target_condition} in the dataset!")
            if record_count > 0:
                recommendations.insert(1, f"✅ Strong evidence: {record_count} records found in medicine_dataset.csv")
            else:
                recommendations.insert(1, "✅ Strong evidence from medicine_dataset.csv - repurposing already documented")
        
        # CSV regulatory data
        regulatory_data = normalized_data.get("regulatory_data", {})
        if regulatory_data.get("db_classification"):
            classification = regulatory_data["db_classification"]
            recommendations.append(f"✅ Regulatory Status: {classification} (from dataset)")
        
        # CSV manufacturers
        manufacturers = regulatory_data.get("db_manufacturers", [])
        if manufacturers and isinstance(manufacturers, list):
            recommendations.append(f"✅ Manufacturer(s): {', '.join(str(m) for m in manufacturers[:3])}")
        
        # Add specific recommendations based on data
        trials_count = trials_data.get("trials_count", 0)
        if trials_count > 0:
            recommendations.append(f"✅ {trials_count} clinical trial(s) found")
        
        if regulatory_data.get("fda_status"):
            recommendations.append("✅ FDA approved - expedited pathway possible")
        
        patent_data = normalized_data.get("patent_data", {})
        patents_count = patent_data.get("patents_count", 0)
        if patents_count > 0:
            recommendations.append(f"📄 {patents_count} patent(s) identified")
        
        # CSV research data
        research_data = normalized_data.get("research_data", {})
        db_data = research_data.get("db_data")
        if db_data and isinstance(db_data, dict):
            categories = db_data.get("categories", [])
            if categories and isinstance(categories, list):
                recommendations.append(f"✅ Drug Category: {', '.join(str(c) for c in categories[:3])}")
            dosage_forms = db_data.get("dosage_forms", [])
            if dosage_forms and isinstance(dosage_forms, list):
                recommendations.append(f"✅ Available Forms: {', '.join(str(d) for d in dosage_forms[:3])}")
        
        return recommendations
    
    def _generate_drug_usage_info(self, drug_name: str, target_condition: str, normalized_data: Dict) -> Dict:
        """
        Generate comprehensive drug usage information including:
        - Current uses and indications
        - Dosage information (strength, forms)
        - Administration details
        - Safety and classification
        - Manufacturer information
        """
        usage_info = {
            "drug_name": drug_name,
            "target_condition": target_condition,
            "current_uses": [],
            "dosage_information": {},
            "administration": {},
            "safety_info": {},
            "manufacturers": [],
            "classification": "",
            "is_approved_for_condition": False,
            "usage_evidence": []
        }
        
        # Get drug data from MongoDB
        research_data = normalized_data.get("research_data", {})
        db_data = research_data.get("db_data", {})
        
        if db_data and isinstance(db_data, dict):
            # Current uses/indications
            indications = db_data.get("indications", [])
            if indications:
                usage_info["current_uses"] = indications
                usage_info["is_approved_for_condition"] = target_condition.lower() in [ind.lower() for ind in indications]
            
            # Dosage information
            strengths = db_data.get("strengths", [])
            dosage_forms = db_data.get("dosage_forms", [])
            
            if strengths or dosage_forms:
                usage_info["dosage_information"] = {
                    "available_strengths": strengths[:10] if strengths else [],  # Limit to 10
                    "available_forms": dosage_forms if dosage_forms else [],
                    "recommended_strength": self._recommend_dosage_strength(strengths, dosage_forms),
                    "dosage_guidance": self._generate_dosage_guidance(dosage_forms, target_condition)
                }
            
            # Administration details
            if dosage_forms:
                usage_info["administration"] = {
                    "available_routes": dosage_forms,
                    "recommended_route": self._recommend_administration_route(dosage_forms, target_condition),
                    "administration_instructions": self._generate_administration_instructions(dosage_forms, target_condition)
                }
            
            # Classification and safety
            classification = db_data.get("classification", "")
            category = db_data.get("category", "")
            
            usage_info["classification"] = classification
            usage_info["safety_info"] = {
                "classification": classification,
                "category": category,
                "prescription_required": "Prescription" in classification if classification else False,
                "otc_available": "Over-the-Counter" in classification if classification else False,
                "safety_notes": self._generate_safety_notes(category, classification)
            }
            
            # Manufacturers
            manufacturers = db_data.get("manufacturers", [])
            if manufacturers:
                usage_info["manufacturers"] = manufacturers[:5]  # Top 5 manufacturers
        
        # Check if already approved for this condition
        trials_data = normalized_data.get("trials_data", {})
        db_evidence = trials_data.get("db_evidence", {})
        if db_evidence.get("already_approved"):
            usage_info["is_approved_for_condition"] = True
            usage_info["usage_evidence"].append({
                "type": "Database Approval",
                "source": "MongoDB Atlas",
                "message": f"{drug_name} is documented as approved for {target_condition}",
                "confidence": "High"
            })
        
        # Add clinical trial evidence
        trials = trials_data.get("trials", [])
        if trials:
            approved_trials = [t for t in trials if t.get("status", "").lower() == "approved"]
            if approved_trials:
                usage_info["usage_evidence"].append({
                    "type": "Clinical Trial",
                    "source": "ClinicalTrials.gov",
                    "message": f"Found {len(approved_trials)} approved trial(s) for this indication",
                    "confidence": "High"
                })
        
        # Generate usage summary
        usage_info["usage_summary"] = self._generate_usage_summary(usage_info)
        
        return usage_info
    
    def _recommend_dosage_strength(self, strengths: List[str], forms: List[str]) -> str:
        """Recommend appropriate dosage strength based on available options"""
        if not strengths:
            return "Consult healthcare provider for dosage"
        
        # Try to find a common/moderate strength
        numeric_strengths = []
        for s in strengths:
            try:
                # Extract number from "XXX mg"
                num = int(''.join(filter(str.isdigit, s.split()[0])))
                numeric_strengths.append((num, s))
            except:
                pass
        
        if numeric_strengths:
            # Return median strength
            numeric_strengths.sort()
            median_idx = len(numeric_strengths) // 2
            return numeric_strengths[median_idx][1]
        
        return strengths[0] if strengths else "Dosage to be determined"
    
    def _generate_dosage_guidance(self, forms: List[str], condition: str) -> str:
        """Generate dosage guidance based on form and condition"""
        if not forms:
            return "Dosage should be determined by a healthcare provider based on patient condition"
        
        guidance = []
        
        if "Tablet" in forms or "Capsule" in forms:
            guidance.append("Oral administration: Take with or without food as directed by physician")
        
        if "Injection" in forms:
            guidance.append("Injectable form: Administer by healthcare professional only")
        
        if "Cream" in forms or "Ointment" in forms:
            guidance.append("Topical application: Apply to affected area as directed")
        
        if "Syrup" in forms or "Drops" in forms:
            guidance.append("Liquid form: Measure dosage carefully using provided device")
        
        if "Inhaler" in forms:
            guidance.append("Inhalation: Use as directed, typically 1-2 puffs as needed")
        
        return ". ".join(guidance) if guidance else "Follow healthcare provider's instructions"
    
    def _recommend_administration_route(self, forms: List[str], condition: str) -> str:
        """Recommend best administration route for the condition"""
        # Priority: condition-specific recommendations
        condition_lower = condition.lower()
        
        if "infection" in condition_lower or "wound" in condition_lower:
            if "Cream" in forms or "Ointment" in forms:
                return "Topical"
            elif "Injection" in forms:
                return "Intramuscular/Intravenous"
        
        if "diabetes" in condition_lower or "pain" in condition_lower:
            if "Tablet" in forms:
                return "Oral"
            elif "Injection" in forms:
                return "Subcutaneous/Intramuscular"
        
        if "respiratory" in condition_lower or "asthma" in condition_lower:
            if "Inhaler" in forms:
                return "Inhalation"
        
        # Default recommendation
        if "Tablet" in forms or "Capsule" in forms:
            return "Oral"
        elif forms:
            return forms[0]
        
        return "To be determined by healthcare provider"
    
    def _generate_administration_instructions(self, forms: List[str], condition: str) -> List[str]:
        """Generate detailed administration instructions"""
        instructions = []
        
        if "Tablet" in forms:
            instructions.append("• Swallow tablet whole with water")
            instructions.append("• Do not crush or chew unless directed")
            instructions.append("• Take at the same time each day for consistency")
        
        if "Capsule" in forms:
            instructions.append("• Swallow capsule whole with water")
            instructions.append("• Do not open capsule contents")
        
        if "Injection" in forms:
            instructions.append("• Administer by trained healthcare professional only")
            instructions.append("• Rotate injection sites to prevent tissue damage")
            instructions.append("• Follow aseptic technique")
        
        if "Cream" in forms or "Ointment" in forms:
            instructions.append("• Clean and dry affected area before application")
            instructions.append("• Apply thin layer, gently rub in")
            instructions.append("• Wash hands after application")
        
        if "Inhaler" in forms:
            instructions.append("• Shake inhaler well before use")
            instructions.append("• Breathe out fully, then inhale medication")
            instructions.append("• Hold breath for 10 seconds after inhalation")
        
        if "Syrup" in forms:
            instructions.append("• Use provided measuring device")
            instructions.append("• Shake well before use")
            instructions.append("• Store in refrigerator if required")
        
        if not instructions:
            instructions.append("• Follow healthcare provider's specific instructions")
            instructions.append("• Read medication label carefully")
            instructions.append("• Do not exceed recommended dosage")
        
        return instructions
    
    def _generate_safety_notes(self, category: str, classification: str) -> List[str]:
        """Generate safety notes based on drug category and classification"""
        notes = []
        
        if "Prescription" in classification:
            notes.append("⚠️ Prescription medication - requires doctor's prescription")
            notes.append("⚠️ Do not share medication with others")
        
        if "Over-the-Counter" in classification:
            notes.append("✅ Available over-the-counter")
            notes.append("⚠️ Still consult healthcare provider for proper usage")
        
        if category:
            if "Antibiotic" in category:
                notes.append("⚠️ Complete full course even if symptoms improve")
                notes.append("⚠️ Do not use for viral infections")
            
            if "Antidiabetic" in category:
                notes.append("⚠️ Monitor blood glucose levels regularly")
                notes.append("⚠️ Risk of hypoglycemia - carry glucose source")
            
            if "Antiviral" in category:
                notes.append("⚠️ Start treatment as early as possible")
                notes.append("⚠️ Complete full course as prescribed")
        
        if not notes:
            notes.append("⚠️ Consult healthcare provider before use")
            notes.append("⚠️ Report any adverse effects immediately")
        
        return notes
    
    def _generate_usage_summary(self, usage_info: Dict) -> str:
        """Generate a comprehensive usage summary"""
        summary_parts = []
        
        drug_name = usage_info.get("drug_name", "This drug")
        target_condition = usage_info.get("target_condition", "the condition")
        
        # Approval status
        if usage_info.get("is_approved_for_condition"):
            summary_parts.append(f"{drug_name} is APPROVED for treating {target_condition}.")
        else:
            summary_parts.append(f"{drug_name} is being evaluated for repurposing to treat {target_condition}.")
        
        # Current uses
        current_uses = usage_info.get("current_uses", [])
        if current_uses:
            summary_parts.append(f"Currently approved for: {', '.join(current_uses[:3])}.")
        
        # Dosage forms
        dosage_info = usage_info.get("dosage_information", {})
        forms = dosage_info.get("available_forms", [])
        if forms:
            summary_parts.append(f"Available in: {', '.join(forms[:3])} form(s).")
        
        # Classification
        classification = usage_info.get("classification", "")
        if classification:
            summary_parts.append(f"Classification: {classification}.")
        
        return " ".join(summary_parts) if summary_parts else f"{drug_name} usage information for {target_condition}."
    
    # Helper methods
    def _assess_research_quality(self) -> str:
        papers = self.agent_results.get("research", {}).get("papers", [])
        if len(papers) >= 5:
            return "high"
        elif len(papers) >= 2:
            return "medium"
        return "low"
    
    def _extract_trial_phases(self) -> List[str]:
        trials = self.agent_results.get("trials", {}).get("trials", [])
        return list(set(t.get("phase", "") for t in trials if t.get("phase")))
    
    def _assess_ip_landscape(self) -> str:
        patents_count = len(self.agent_results.get("patents", {}).get("patents", []))
        if patents_count >= 3:
            return "strong"
        elif patents_count >= 1:
            return "moderate"
        return "none"
    
    def _format_market_feasibility(self, market_data: Dict) -> Dict:
        """
        Format market data to match Pydantic MarketFeasibility model
        """
        # Get regulatory path from regulatory agent
        regulatory_data = self.agent_results.get("regulatory", {})
        regulatory_path = regulatory_data.get("pathway", "FDA IND required")
        
        # Ensure all required fields are present
        return {
            "market_size": market_data.get("market_size", "To be determined"),
            "growth_rate": market_data.get("growth_rate", "Market analysis required"),
            "competition": market_data.get("competition", "Assessment needed"),
            "regulatory_path": regulatory_path,
            "timeline": market_data.get("timeline", "36-48 months")
        }

