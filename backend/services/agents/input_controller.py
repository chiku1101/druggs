"""
Input Controller - Detects case type and routes to appropriate agents
"""

from typing import Dict, Any
from enum import Enum


class CaseType(Enum):
    """Types of drug repurposing cases"""
    KNOWN_REPURPOSING = "known_repurposing"  # Well-established case
    LIKELY_REPURPOSING = "likely_repurposing"  # Strong evidence
    EXPLORATORY = "exploratory"  # Preliminary research needed
    NOVEL = "novel"  # No established evidence


class InputController:
    """
    Detects case type based on input
    Routes to appropriate agents based on case complexity
    """
    
    # Known repurposing cases with established evidence
    KNOWN_CASES = {
        ("metformin", "cancer"): CaseType.KNOWN_REPURPOSING,
        ("metformin", "pcos"): CaseType.KNOWN_REPURPOSING,
        ("aspirin", "cardiovascular"): CaseType.KNOWN_REPURPOSING,
        ("sildenafil", "pulmonary hypertension"): CaseType.KNOWN_REPURPOSING,
        ("thalidomide", "multiple myeloma"): CaseType.KNOWN_REPURPOSING,
        ("zinc", "diarrhea"): CaseType.KNOWN_REPURPOSING,
    }
    
    def __init__(self):
        pass
    
    def detect_case_type(self, drug_name: str, target_condition: str) -> Dict[str, Any]:
        """
        Detect the type of case and determine analysis strategy
        """
        drug_lower = drug_name.lower().strip()
        condition_lower = target_condition.lower().strip()
        
        case_type = self._match_case_type(drug_lower, condition_lower)
        
        return {
            "case_type": case_type.value,
            "drug_name": drug_name,
            "target_condition": target_condition,
            "agents_to_run": self._get_required_agents(case_type),
            "priority_level": self._get_priority(case_type),
            "estimated_analysis_time": self._get_analysis_time(case_type)
        }
    
    def _match_case_type(self, drug_lower: str, condition_lower: str) -> CaseType:
        """
        Match input against known cases
        """
        # Exact match
        for (drug, condition), case_type in self.KNOWN_CASES.items():
            if drug.lower() in drug_lower and condition.lower() in condition_lower:
                return case_type
        
        # Partial match for known drugs
        known_drugs = ["metformin", "aspirin", "sildenafil", "thalidomide", "zinc", "ibuprofen"]
        if any(drug in drug_lower for drug in known_drugs):
            return CaseType.LIKELY_REPURPOSING
        
        # Check if condition is well-studied
        well_studied_conditions = ["cancer", "diabetes", "cardiovascular", "hypertension", "pcos"]
        if any(cond in condition_lower for cond in well_studied_conditions):
            return CaseType.EXPLORATORY
        
        # Default: novel case
        return CaseType.NOVEL
    
    def _get_required_agents(self, case_type: CaseType) -> list:
        """
        Determine which agents to run based on case type
        """
        agents = {
            CaseType.KNOWN_REPURPOSING: [
                "ResearchAgent",
                "TrialsAgent",
                "PatentAgent",
                "RegulatoryAgent",
                "MarketAgent"
            ],
            CaseType.LIKELY_REPURPOSING: [
                "ResearchAgent",
                "TrialsAgent",
                "PatentAgent",
                "RegulatoryAgent",
                "MarketAgent"
            ],
            CaseType.EXPLORATORY: [
                "ResearchAgent",
                "TrialsAgent",
                "RegulatoryAgent"
            ],
            CaseType.NOVEL: [
                "ResearchAgent",
                "RegulatoryAgent"
            ]
        }
        
        return agents.get(case_type, ["ResearchAgent"])
    
    def _get_priority(self, case_type: CaseType) -> int:
        """
        Get priority level (1-5, where 5 is highest)
        """
        priorities = {
            CaseType.KNOWN_REPURPOSING: 5,
            CaseType.LIKELY_REPURPOSING: 4,
            CaseType.EXPLORATORY: 3,
            CaseType.NOVEL: 2
        }
        
        return priorities.get(case_type, 1)
    
    def _get_analysis_time(self, case_type: CaseType) -> str:
        """
        Get estimated analysis time
        """
        times = {
            CaseType.KNOWN_REPURPOSING: "1-2 minutes",
            CaseType.LIKELY_REPURPOSING: "2-3 minutes",
            CaseType.EXPLORATORY: "3-5 minutes",
            CaseType.NOVEL: "5-10 minutes"
        }
        
        return times.get(case_type, "5 minutes")
