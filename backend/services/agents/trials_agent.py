"""
Clinical Trials Agent - Fetches data from ClinicalTrials.gov API
"""

from .base_agent import BaseAgent
from typing import Dict, Any, List
import aiohttp
import json
from datetime import datetime


class TrialsAgent(BaseAgent):
    """
    Fetches clinical trials data from ClinicalTrials.gov API v2
    """
    
    def __init__(self):
        super().__init__("TrialsAgent")
        self.trials_base_url = "https://clinicaltrials.gov/api/v2/studies"
        self.timeout = 20
        
    async def execute(self, drug_name: str, target_condition: str) -> Dict[str, Any]:
        """
        Fetch clinical trials for drug-condition combination
        """
        trials = []
        
        try:
            trials = await self._search_trials(drug_name, target_condition)
        except Exception as e:
            print(f"Clinical trials search failed: {e}")
        
        return {
            "clinical_trials": trials,
            "total_trials_found": len(trials),
            "data_source": "ClinicalTrials.gov"
        }
    
    async def _search_trials(self, drug_name: str, target_condition: str) -> List[Dict[str, Any]]:
        """
        Search ClinicalTrials.gov for relevant trials
        """
        trials = []
        
        # Build query
        query = f'({drug_name}) AND ({target_condition})'
        
        params = {
            "query.cond": target_condition,
            "query.intr": drug_name,
            "pageSize": 10,
            "format": "json"
        }
        
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(
                    self.trials_base_url,
                    params=params,
                    timeout=aiohttp.ClientTimeout(total=15)
                ) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        
                        # Extract trials
                        studies = data.get("studies", [])
                        for study in studies[:8]:  # Get top 8
                            trial = self._extract_trial_info(study)
                            if trial:
                                trials.append(trial)
            except Exception as e:
                print(f"Error fetching trials: {e}")
        
        return trials
    
    def _extract_trial_info(self, study: Dict) -> Dict[str, Any]:
        """
        Extract relevant trial information
        """
        try:
            protocol_section = study.get("protocolSection", {})
            id_module = protocol_section.get("identificationModule", {})
            status_module = protocol_section.get("statusModule", {})
            design_module = protocol_section.get("designModule", {})
            
            nct_id = id_module.get("nctId", "Unknown")
            title = id_module.get("officialTitle", id_module.get("briefTitle", "Unknown"))
            
            # Status
            overall_status = status_module.get("overallStatus", "Unknown")
            
            # Phase
            phases = design_module.get("phases", [])
            phase = phases[0] if phases else "Phase Unknown"
            
            # Enrollment
            enrollment = status_module.get("enrollmentInfo", {}).get("count", 0)
            
            # Completion date
            completion_date = status_module.get("completionDateStruct", {}).get("date", "TBD")
            
            return {
                "id": nct_id,
                "title": title,
                "status": overall_status,
                "phase": phase,
                "participants": int(enrollment) if enrollment else 0,
                "completion_date": completion_date,
                "url": f"https://clinicaltrials.gov/ct2/show/{nct_id}"
            }
        except Exception as e:
            print(f"Error extracting trial info: {e}")
            return None
