"""
Base Agent Class - All specialized agents inherit from this
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List
import asyncio


class BaseAgent(ABC):
    """
    Abstract base class for all agents
    """
    
    def __init__(self, name: str):
        self.name = name
        self.timeout = 30  # seconds
        
    @abstractmethod
    async def execute(self, drug_name: str, target_condition: str) -> Dict[str, Any]:
        """
        Execute agent task
        Returns a dictionary with agent-specific results
        """
        pass
    
    async def run_with_timeout(self, drug_name: str, target_condition: str) -> Dict[str, Any]:
        """
        Execute with timeout protection
        """
        try:
            result = await asyncio.wait_for(
                self.execute(drug_name, target_condition),
                timeout=self.timeout
            )
            return {
                "success": True,
                "data": result,
                "agent": self.name
            }
        except asyncio.TimeoutError:
            return {
                "success": False,
                "error": f"{self.name} timed out after {self.timeout}s",
                "agent": self.name,
                "data": {}
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "agent": self.name,
                "data": {}
            }
    
    def _sanitize_query(self, query: str) -> str:
        """Sanitize input for API calls"""
        return query.strip().replace('"', '').replace("'", "")
