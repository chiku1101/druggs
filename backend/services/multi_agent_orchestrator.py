"""
Multi-Agent Orchestrator for Drug Repurposing Analysis
Coordinates specialized agents running in parallel
"""

import asyncio
from typing import Dict, List, Optional, Any
from enum import Enum
import json


class CaseType(Enum):
    """Case detection types"""
    SINGLE_DRUG_DISEASE = 1  # Normal drug + disease input
    DRUG_ONLY = 2            # Drug only, find conditions
    DISEASE_ONLY = 3         # Disease only, find drugs
    TREND_INTELLIGENCE = 4   # No input, market trends


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
    
    def detect_case(self, drug_name: Optional[str], target_condition: Optional[str]) -> CaseType:
        """
        Case Detection Logic (from diagram)
        """
        if drug_name and target_condition:
            return CaseType.SINGLE_DRUG_DISEASE
        elif drug_name and not target_condition:
            return CaseType.DRUG_ONLY
        elif not drug_name and target_condition:
            return CaseType.DISEASE_ONLY
        else:
            return CaseType.TREND_INTELLIGENCE
    
    async def orchestrate(self, drug_name: Optional[str], target_condition: Optional[str]) -> Dict:
        """
        Main orchestration method - runs agents in parallel
        """
        # Step 1: Case Detection
        self.case_type = self.detect_case(drug_name, target_condition)
        print(f"🔍 Case Type Detected: {self.case_type.name}")
        
        # Step 2: Multi-Agent Execution (Parallel)
        print("🤖 Launching Multi-Agent System...")
        
        if self.case_type == CaseType.TREND_INTELLIGENCE:
            return await self._execute_trend_analytics()
        else:
            return await self._execute_multi_agent_flow(drug_name, target_condition)
    
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

