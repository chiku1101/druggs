"""
Market Agent - Analyzes market size, trends, and competition
"""

from .base_agent import BaseAgent
from typing import Dict, Any
import random


class MarketAgent(BaseAgent):
    """
    Analyzes market opportunity for drug-condition combination
    """
    
    def __init__(self):
        super().__init__("MarketAgent")
        self.timeout = 15
        
    async def execute(self, drug_name: str, target_condition: str) -> Dict[str, Any]:
        """
        Analyze market opportunity
        """
        market_analysis = self._analyze_market(drug_name, target_condition)
        
        return {
            "market_feasibility": market_analysis,
            "data_source": "Market analysis"
        }
    
    def _analyze_market(self, drug_name: str, target_condition: str) -> Dict[str, Any]:
        """
        Analyze market opportunity based on condition and drug
        """
        condition_lower = target_condition.lower()
        
        # Known market data for common conditions
        market_data = {
            "cancer": {
                "market_size": "$230B",
                "growth_rate": "7.5% CAGR",
                "competition": "High",
                "unmet_need": "Moderate",
                "patient_population": "19.5M new cases/year globally"
            },
            "pcos": {
                "market_size": "$4.2B",
                "growth_rate": "8.3% CAGR",
                "competition": "Low-Moderate",
                "unmet_need": "High",
                "patient_population": "6-26% of women of reproductive age"
            },
            "cardiovascular": {
                "market_size": "$180B",
                "growth_rate": "5.2% CAGR",
                "competition": "High",
                "unmet_need": "Moderate",
                "patient_population": "17.9M deaths/year"
            },
            "hypertension": {
                "market_size": "$45B",
                "growth_rate": "4.1% CAGR",
                "competition": "High",
                "unmet_need": "Low",
                "patient_population": "1.28B cases globally"
            },
            "diabetes": {
                "market_size": "$95B",
                "growth_rate": "5.6% CAGR",
                "competition": "High",
                "unmet_need": "Moderate",
                "patient_population": "537M cases globally"
            },
            "alzheimer": {
                "market_size": "$15B",
                "growth_rate": "9.2% CAGR",
                "competition": "Moderate",
                "unmet_need": "Very High",
                "patient_population": "57M cases globally"
            }
        }
        
        # Find matching market data
        market_info = None
        for condition_key, data in market_data.items():
            if condition_key in condition_lower:
                market_info = data
                break
        
        # Default market analysis if no match
        if not market_info:
            market_info = {
                "market_size": "$2-10B",
                "growth_rate": "6-8% CAGR",
                "competition": "Moderate",
                "unmet_need": "Moderate",
                "patient_population": "To be determined"
            }
        
        return {
            "market_size": market_info["market_size"],
            "growth_rate": market_info["growth_rate"],
            "competition": market_info["competition"],
            "unmet_need": market_info["unmet_need"],
            "patient_population": market_info["patient_population"],
            "regulatory_path": "505(b)(2) pathway available for approved drugs",
            "timeline": "18-36 months to commercialization",
            "exclusivity": "3-7 years market exclusivity potential"
        }
