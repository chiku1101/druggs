"""
Scoring Engine - Weighted scoring system for repurposeability
"""

from typing import Dict, Any
import math


class ScoringEngine:
    """
    Calculates repurposeability score based on evidence from all agents
    Uses weighted scoring system
    """
    
    # Weights for different evidence sources (sum = 100)
    WEIGHTS = {
        "research": 25,      # Research papers evidence
        "trials": 30,        # Clinical trial evidence (most important)
        "patents": 10,       # Patent landscape
        "regulatory": 20,    # Regulatory pathway clarity
        "market": 15         # Market opportunity
    }
    
    def __init__(self):
        assert sum(self.WEIGHTS.values()) == 100, "Weights must sum to 100"
    
    def calculate_score(self, agent_results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculate overall repurposeability score
        
        Returns a score from 0-100 with breakdown by category
        """
        
        scores = {
            "research_score": self._score_research(agent_results),
            "trials_score": self._score_trials(agent_results),
            "patents_score": self._score_patents(agent_results),
            "regulatory_score": self._score_regulatory(agent_results),
            "market_score": self._score_market(agent_results)
        }
        
        # Calculate weighted overall score
        overall_score = (
            scores["research_score"] * (self.WEIGHTS["research"] / 100) +
            scores["trials_score"] * (self.WEIGHTS["trials"] / 100) +
            scores["patents_score"] * (self.WEIGHTS["patents"] / 100) +
            scores["regulatory_score"] * (self.WEIGHTS["regulatory"] / 100) +
            scores["market_score"] * (self.WEIGHTS["market"] / 100)
        )
        
        return {
            "overall_score": round(overall_score, 1),
            "score_breakdown": scores,
            "weights": self.WEIGHTS,
            "confidence": self._calculate_confidence(agent_results)
        }
    
    def _score_research(self, agent_results: Dict[str, Any]) -> int:
        """
        Score based on research papers
        """
        research_result = agent_results.get("ResearchAgent", {})
        
        if not research_result.get("success"):
            return 20  # Base score if agent failed
        
        papers = research_result.get("data", {}).get("research_papers", [])
        
        if not papers:
            return 30  # No papers found
        
        # Score based on number and relevance of papers
        num_papers = len(papers)
        avg_relevance = sum(p.get("relevance", 50) for p in papers) / len(papers) if papers else 50
        
        # Scoring logic
        score = 30  # Base
        score += min(30, num_papers * 5)  # Papers count
        score += (avg_relevance - 50) * 0.8  # Relevance quality
        
        return min(100, max(20, round(score)))
    
    def _score_trials(self, agent_results: Dict[str, Any]) -> int:
        """
        Score based on clinical trials
        """
        trials_result = agent_results.get("TrialsAgent", {})
        
        if not trials_result.get("success"):
            return 20  # Base score if agent failed
        
        trials = trials_result.get("data", {}).get("clinical_trials", [])
        
        if not trials:
            return 30  # No trials found
        
        # Score based on trials
        num_trials = len(trials)
        
        # Check trial phases
        score = 30  # Base
        
        for trial in trials:
            phase = trial.get("phase", "").lower()
            status = trial.get("status", "").lower()
            
            if "phase 3" in phase:
                score += 20
            elif "phase 2" in phase:
                score += 15
            elif "phase 1" in phase:
                score += 8
            
            if "recruiting" in status:
                score += 5
            elif "active" in status:
                score += 8
        
        # Cap based on number of trials
        if num_trials >= 3:
            score = min(100, score + 15)
        elif num_trials == 2:
            score = min(100, score + 10)
        
        return min(100, max(20, score))
    
    def _score_patents(self, agent_results: Dict[str, Any]) -> int:
        """
        Score based on patent landscape
        """
        patents_result = agent_results.get("PatentAgent", {})
        
        if not patents_result.get("success"):
            return 30  # Base score if agent failed
        
        patents = patents_result.get("data", {}).get("patents", [])
        
        if not patents:
            return 35  # No patents found, but could be opportunity
        
        # Score based on patents
        score = 40  # Base
        
        num_patents = len(patents)
        score += min(30, num_patents * 5)
        
        # Check patent status
        for patent in patents:
            if patent.get("status") == "Granted":
                score += 5
        
        return min(100, max(30, score))
    
    def _score_regulatory(self, agent_results: Dict[str, Any]) -> int:
        """
        Score based on regulatory pathway
        """
        regulatory_result = agent_results.get("RegulatoryAgent", {})
        
        if not regulatory_result.get("success"):
            return 40  # Base score if agent failed
        
        data = regulatory_result.get("data", {})
        fda_status = data.get("fda_status", {})
        regulatory_pathway = data.get("regulatory_pathway", {})
        
        score = 50  # Base
        
        # FDA approval status
        if fda_status.get("approved"):
            score += 30  # Major boost if already approved
        else:
            score += 10
        
        # Check pathway
        pathway = regulatory_pathway.get("pathway", "").lower()
        if "505(b)(2)" in pathway:
            score += 15  # Expedited pathway
        
        return min(100, max(40, score))
    
    def _score_market(self, agent_results: Dict[str, Any]) -> int:
        """
        Score based on market opportunity
        """
        market_result = agent_results.get("MarketAgent", {})
        
        if not market_result.get("success"):
            return 50  # Base score if agent failed
        
        market = market_result.get("data", {}).get("market_feasibility", {})
        
        score = 50  # Base
        
        # Market size
        market_size = market.get("market_size", "")
        if "$" in market_size:
            try:
                # Extract number
                num_str = market_size.replace("$", "").replace("B", "").replace("M", "")
                num = float(num_str)
                if num > 50:
                    score += 20
                elif num > 10:
                    score += 15
                else:
                    score += 8
            except:
                pass
        
        # Unmet need
        unmet_need = market.get("unmet_need", "").lower()
        if "very high" in unmet_need or "high" in unmet_need:
            score += 15
        elif "moderate" in unmet_need:
            score += 8
        
        # Competition
        competition = market.get("competition", "").lower()
        if "low" in competition:
            score += 10
        
        return min(100, max(50, score))
    
    def _calculate_confidence(self, agent_results: Dict[str, Any]) -> float:
        """
        Calculate confidence level (0-1) based on data completeness
        """
        successful_agents = sum(
            1 for result in agent_results.values() 
            if result.get("success")
        )
        
        total_agents = len(agent_results)
        
        if total_agents == 0:
            return 0.0
        
        confidence = successful_agents / total_agents
        
        # Lower confidence if critical agents failed
        critical_agents = {"ResearchAgent", "TrialsAgent"}
        failed_critical = any(
            agent in critical_agents 
            for agent, result in agent_results.items()
            if not result.get("success")
        )
        
        if failed_critical:
            confidence *= 0.7
        
        return round(confidence, 2)
