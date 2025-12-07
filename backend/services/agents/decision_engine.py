"""
Decision Engine - Makes Go/No-Go decision for drug repurposing
"""

from typing import Dict, Any


class DecisionEngine:
    """
    Makes Go/No-Go recommendations based on overall score and evidence
    """
    
    # Decision thresholds
    THRESHOLDS = {
        "go": 70,           # Strong recommendation to proceed
        "consider": 50,     # Moderate - consider with caution
        "no_go": 0          # Below 50 - not recommended
    }
    
    def __init__(self):
        pass
    
    def make_decision(self, score_data: Dict[str, Any], 
                     agent_results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Make Go/No-Go decision
        """
        overall_score = score_data.get("overall_score", 0)
        confidence = score_data.get("confidence", 0)
        
        verdict = self._determine_verdict(overall_score)
        reasoning = self._build_reasoning(score_data, agent_results, verdict)
        risk_factors = self._identify_risk_factors(score_data, agent_results)
        next_steps = self._recommend_next_steps(verdict, score_data)
        
        return {
            "verdict": verdict,
            "overall_score": overall_score,
            "confidence": confidence,
            "reasoning": reasoning,
            "risk_factors": risk_factors,
            "next_steps": next_steps,
            "recommendation": self._get_recommendation_text(verdict),
            "decision_timestamp": self._get_timestamp()
        }
    
    def _determine_verdict(self, score: float) -> str:
        """
        Determine verdict based on score
        """
        if score >= self.THRESHOLDS["go"]:
            return "GO"
        elif score >= self.THRESHOLDS["consider"]:
            return "CONSIDER"
        else:
            return "NO_GO"
    
    def _build_reasoning(self, score_data: Dict[str, Any],
                        agent_results: Dict[str, Any],
                        verdict: str) -> list:
        """
        Build detailed reasoning for decision
        """
        reasoning = []
        scores = score_data.get("score_breakdown", {})
        
        # Research evidence
        research_score = scores.get("research_score", 0)
        if research_score > 70:
            reasoning.append("Strong research evidence supporting repurposing")
        elif research_score > 50:
            reasoning.append("Moderate research evidence available")
        else:
            reasoning.append("Limited research evidence - further studies needed")
        
        # Clinical trial evidence
        trials_score = scores.get("trials_score", 0)
        trials_result = agent_results.get("TrialsAgent", {})
        num_trials = len(trials_result.get("data", {}).get("clinical_trials", []))
        
        if trials_score > 70:
            reasoning.append(f"Strong clinical trial support ({num_trials} trials found)")
        elif trials_score > 50:
            reasoning.append(f"Some clinical trial evidence ({num_trials} trials)")
        else:
            reasoning.append("Limited clinical trial evidence - Phase I/II needed")
        
        # Regulatory pathway
        regulatory_score = scores.get("regulatory_score", 0)
        reg_result = agent_results.get("RegulatoryAgent", {})
        pathway = reg_result.get("data", {}).get("regulatory_pathway", {})
        
        if "505(b)(2)" in pathway.get("pathway", ""):
            reasoning.append("FDA 505(b)(2) pathway available - expedited approval possible")
        else:
            reasoning.append("Standard IND pathway required")
        
        # Market opportunity
        market_score = scores.get("market_score", 0)
        if market_score > 70:
            reasoning.append("Strong market opportunity and commercial viability")
        elif market_score > 50:
            reasoning.append("Moderate market opportunity")
        else:
            reasoning.append("Limited market opportunity - niche indication")
        
        # Patent landscape
        patents_score = scores.get("patents_score", 0)
        if patents_score > 70:
            reasoning.append("Patent landscape favorable for protection")
        else:
            reasoning.append("Patent protection opportunities available")
        
        return reasoning
    
    def _identify_risk_factors(self, score_data: Dict[str, Any],
                              agent_results: Dict[str, Any]) -> list:
        """
        Identify potential risk factors
        """
        risks = []
        scores = score_data.get("score_breakdown", {})
        confidence = score_data.get("confidence", 0)
        
        # Low individual scores
        if scores.get("research_score", 0) < 40:
            risks.append({
                "factor": "Insufficient research evidence",
                "severity": "High",
                "mitigation": "Conduct comprehensive literature review"
            })
        
        if scores.get("trials_score", 0) < 40:
            risks.append({
                "factor": "No or limited clinical trial data",
                "severity": "High",
                "mitigation": "Plan Phase II proof-of-concept trial"
            })
        
        if scores.get("regulatory_score", 0) < 50:
            risks.append({
                "factor": "Unclear regulatory pathway",
                "severity": "Moderate",
                "mitigation": "Consult with FDA for guidance"
            })
        
        # Low confidence
        if confidence < 0.6:
            risks.append({
                "factor": "Low data completeness",
                "severity": "Moderate",
                "mitigation": "Gather additional evidence"
            })
        
        # Failed agents
        for agent_name, result in agent_results.items():
            if not result.get("success"):
                risks.append({
                    "factor": f"{agent_name} could not retrieve data",
                    "severity": "Low",
                    "mitigation": "Use alternative data sources"
                })
        
        return risks
    
    def _recommend_next_steps(self, verdict: str, score_data: Dict[str, Any]) -> list:
        """
        Recommend next steps based on verdict
        """
        steps = []
        scores = score_data.get("score_breakdown", {})
        
        if verdict == "GO":
            steps = [
                "1. Conduct regulatory pre-IND meeting with FDA",
                "2. Design Phase II clinical trial protocol",
                "3. Identify clinical trial sites and investigators",
                "4. Prepare IND application",
                "5. Launch clinical development program"
            ]
        elif verdict == "CONSIDER":
            steps = [
                "1. Conduct additional literature review",
                "2. Engage clinical experts for consultation",
                "3. Evaluate patent landscape thoroughly",
                "4. Assess competitive landscape",
                "5. Consider pilot/feasibility studies before full development"
            ]
        else:  # NO_GO
            steps = [
                "1. Identify evidence gaps that need to be addressed",
                "2. Monitor literature for new developments",
                "3. Consider alternative drug-condition combinations",
                "4. Re-evaluate if new evidence emerges"
            ]
        
        return steps
    
    def _get_recommendation_text(self, verdict: str) -> str:
        """
        Get human-readable recommendation
        """
        recommendations = {
            "GO": "PROCEED with drug repurposing program - Strong scientific and commercial case",
            "CONSIDER": "CONSIDER with caution - Additional evidence and risk assessment needed",
            "NO_GO": "DO NOT PROCEED - Insufficient evidence and/or unfavorable risk-benefit profile"
        }
        
        return recommendations.get(verdict, "Unable to determine recommendation")
    
    def _get_timestamp(self) -> str:
        """
        Get current timestamp
        """
        from datetime import datetime
        return datetime.now().isoformat()
