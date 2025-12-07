"""
Multi-Agent Orchestrator - Runs all agents in parallel
"""

import asyncio
from typing import Dict, Any, List
from .research_agent import ResearchAgent
from .trials_agent import TrialsAgent
from .patent_agent import PatentAgent
from .regulatory_agent import RegulatoryAgent
from .market_agent import MarketAgent


class MultiAgentOrchestrator:
    """
    Orchestrates execution of multiple agents in parallel
    """
    
    def __init__(self):
        self.agents = {
            "ResearchAgent": ResearchAgent(),
            "TrialsAgent": TrialsAgent(),
            "PatentAgent": PatentAgent(),
            "RegulatoryAgent": RegulatoryAgent(),
            "MarketAgent": MarketAgent()
        }
    
    async def execute(self, 
                     drug_name: str, 
                     target_condition: str,
                     agent_names: List[str] = None) -> Dict[str, Any]:
        """
        Execute specified agents in parallel
        
        Args:
            drug_name: Name of the drug
            target_condition: Target condition for repurposing
            agent_names: List of agent names to run. If None, run all agents.
        
        Returns:
            Dictionary with results from all agents
        """
        
        if agent_names is None:
            agent_names = list(self.agents.keys())
        
        # Filter agents to run
        agents_to_run = {
            name: self.agents[name] 
            for name in agent_names 
            if name in self.agents
        }
        
        print(f"🚀 Starting {len(agents_to_run)} agents in parallel...")
        
        # Create tasks for all agents
        tasks = {
            name: agent.run_with_timeout(drug_name, target_condition)
            for name, agent in agents_to_run.items()
        }
        
        # Execute all tasks concurrently
        results = await asyncio.gather(*tasks.values(), return_exceptions=True)
        
        # Combine results
        agent_results = {}
        for (agent_name, _), result in zip(tasks.items(), results):
            if isinstance(result, Exception):
                agent_results[agent_name] = {
                    "success": False,
                    "error": str(result),
                    "agent": agent_name
                }
            else:
                agent_results[agent_name] = result
        
        # Print summary
        successful = sum(1 for r in agent_results.values() if r.get("success"))
        print(f"✅ {successful}/{len(agents_to_run)} agents completed successfully")
        
        return {
            "orchestration_complete": True,
            "agents_executed": len(agents_to_run),
            "agents_successful": successful,
            "results": agent_results
        }
    
    async def execute_with_strategy(self,
                                   drug_name: str,
                                   target_condition: str,
                                   strategy: str = "full") -> Dict[str, Any]:
        """
        Execute agents based on strategy
        
        Strategies:
            - "full": Run all agents
            - "quick": Run only essential agents (Research, Trials)
            - "deep": Run all agents with extended timeouts
        """
        
        strategies = {
            "quick": ["ResearchAgent", "TrialsAgent"],
            "full": list(self.agents.keys()),
            "deep": list(self.agents.keys())
        }
        
        agent_names = strategies.get(strategy, list(self.agents.keys()))
        
        if strategy == "deep":
            # Increase timeouts for deeper analysis
            for agent in self.agents.values():
                agent.timeout = 40
        
        return await self.execute(drug_name, target_condition, agent_names)
