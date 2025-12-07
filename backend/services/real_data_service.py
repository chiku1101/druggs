"""
Real Medical Data Integration Service
Fetches genuine drug data from real medical databases and APIs
"""

import aiohttp
import asyncio
from typing import Dict, List, Optional
import json

class RealMedicalDataService:
    """
    Service to fetch real drug data from legitimate medical databases
    """
    
    def __init__(self):
        self.openfda_base = "https://api.fda.gov/drug"
        self.clinicaltrials_base = "https://clinicaltrials.gov/api/v2"
        self.pubchem_base = "https://pubchem.ncbi.nlm.nih.gov/rest/pug"
        print("✅ Real medical data service initialized")
    
    async def fetch_drug_from_openfda(self, drug_name: str) -> Optional[Dict]:
        """
        Fetch real drug information from OpenFDA API
        """
        try:
            async with aiohttp.ClientSession() as session:
                # Search FDA drug labels
                url = f"{self.openfda_base}/label.json"
                params = {
                    "search": f'openfda.brand_name:"{drug_name}" OR openfda.generic_name:"{drug_name}"',
                    "limit": 1
                }
                
                async with session.get(url, params=params, timeout=10) as response:
                    if response.status == 200:
                        data = await response.json()
                        if data.get("results"):
                            result = data["results"][0]
                            return self._parse_fda_label(result, drug_name)
        except Exception as e:
            print(f"  ⚠️  OpenFDA fetch failed for {drug_name}: {str(e)[:100]}")
        
        return None
    
    def _parse_fda_label(self, fda_data: Dict, drug_name: str) -> Dict:
        """
        Parse FDA label data into usable format
        """
        openfda = fda_data.get("openfda", {})
        
        # Extract indications
        indications = fda_data.get("indications_and_usage", [])
        if indications:
            indications = indications[0].split(". ")[:3]  # First 3 sentences
        
        # Extract mechanism
        mechanism = fda_data.get("mechanism_of_action", ["Not specified"])
        if mechanism:
            mechanism = mechanism[0][:200]  # First 200 chars
        
        # Extract warnings/side effects
        warnings = fda_data.get("warnings", [])
        side_effects = []
        if warnings:
            side_effects = warnings[0].split(". ")[:5]
        
        return {
            "name": drug_name,
            "generic_name": openfda.get("generic_name", [drug_name])[0] if openfda.get("generic_name") else drug_name,
            "brand_names": openfda.get("brand_name", []),
            "indications": indications if indications else ["See FDA label"],
            "mechanism": mechanism,
            "manufacturer": openfda.get("manufacturer_name", ["Unknown"])[0] if openfda.get("manufacturer_name") else "Unknown",
            "route": openfda.get("route", []),
            "warnings": side_effects[:3] if side_effects else [],
            "fda_approved": True,
            "source": "FDA Official Database",
            "substance_name": openfda.get("substance_name", [])
        }
    
    async def fetch_clinical_trials(self, drug_name: str, condition: str = None) -> List[Dict]:
        """
        Fetch REAL clinical trials from ClinicalTrials.gov
        """
        try:
            async with aiohttp.ClientSession() as session:
                # Build query
                query = drug_name
                if condition:
                    query = f"{drug_name} AND {condition}"
                
                url = f"{self.clinicaltrials_base}/studies"
                params = {
                    "query.term": query,
                    "pageSize": 5,
                    "format": "json"
                }
                
                async with session.get(url, params=params, timeout=10) as response:
                    if response.status == 200:
                        data = await response.json()
                        studies = data.get("studies", [])
                        return [self._parse_clinical_trial(study) for study in studies]
        except Exception as e:
            print(f"  ⚠️  ClinicalTrials.gov fetch failed: {str(e)[:100]}")
        
        return []
    
    def _parse_clinical_trial(self, study: Dict) -> Dict:
        """
        Parse clinical trial data
        """
        protocol = study.get("protocolSection", {})
        identification = protocol.get("identificationModule", {})
        status = protocol.get("statusModule", {})
        design = protocol.get("designModule", {})
        
        # Extract phase
        phases = design.get("phases", ["Not Applicable"])
        phase = phases[0] if phases else "Not Specified"
        
        return {
            "id": identification.get("nctId", "NCT00000000"),
            "title": identification.get("briefTitle", "Study title not available"),
            "status": status.get("overallStatus", "Unknown"),
            "phase": phase,
            "completion_date": status.get("completionDateStruct", {}).get("date", "Not specified"),
            "participants": status.get("enrollmentInfo", {}).get("count", 0),
            "source": "ClinicalTrials.gov"
        }
    
    async def fetch_pubchem_data(self, drug_name: str) -> Optional[Dict]:
        """
        Fetch drug data from PubChem
        """
        try:
            async with aiohttp.ClientSession() as session:
                # Search for compound
                search_url = f"{self.pubchem_base}/compound/name/{drug_name}/JSON"
                
                async with session.get(search_url, timeout=10) as response:
                    if response.status == 200:
                        data = await response.json()
                        if data.get("PC_Compounds"):
                            compound = data["PC_Compounds"][0]
                            return self._parse_pubchem_data(compound, drug_name)
        except Exception as e:
            print(f"  ⚠️  PubChem fetch failed for {drug_name}: {str(e)[:100]}")
        
        return None
    
    def _parse_pubchem_data(self, compound: Dict, drug_name: str) -> Dict:
        """
        Parse PubChem compound data
        """
        props = compound.get("props", [])
        
        # Extract properties
        molecular_formula = None
        molecular_weight = None
        
        for prop in props:
            label = prop.get("urn", {}).get("label", "")
            if "Molecular Formula" in label:
                molecular_formula = prop.get("value", {}).get("sval")
            elif "Molecular Weight" in label:
                molecular_weight = prop.get("value", {}).get("fval")
        
        return {
            "name": drug_name,
            "pubchem_cid": compound.get("id", {}).get("id", {}).get("cid"),
            "molecular_formula": molecular_formula,
            "molecular_weight": molecular_weight,
            "source": "PubChem/NIH"
        }
    
    async def get_comprehensive_drug_data(self, drug_name: str, condition: str = None) -> Dict:
        """
        Fetch comprehensive data from all sources
        """
        print(f"📡 Fetching REAL data for {drug_name}...")
        
        # Fetch from multiple sources in parallel
        tasks = [
            self.fetch_drug_from_openfda(drug_name),
            self.fetch_clinical_trials(drug_name, condition),
            self.fetch_pubchem_data(drug_name)
        ]
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        fda_data = results[0] if not isinstance(results[0], Exception) else None
        clinical_trials = results[1] if not isinstance(results[1], Exception) else []
        pubchem_data = results[2] if not isinstance(results[2], Exception) else None
        
        # Combine all data
        comprehensive_data = {
            "drug_name": drug_name,
            "real_data_available": fda_data is not None or len(clinical_trials) > 0,
            "fda_data": fda_data,
            "clinical_trials": clinical_trials,
            "pubchem_data": pubchem_data,
            "data_sources": []
        }
        
        if fda_data:
            comprehensive_data["data_sources"].append("FDA Official Database")
        if clinical_trials:
            comprehensive_data["data_sources"].append(f"ClinicalTrials.gov ({len(clinical_trials)} trials)")
        if pubchem_data:
            comprehensive_data["data_sources"].append("PubChem/NIH")
        
        print(f"  ✅ Found real data from: {', '.join(comprehensive_data['data_sources'])}")
        
        return comprehensive_data
    
    async def search_pubmed_papers(self, drug_name: str, condition: str) -> List[Dict]:
        """
        Search for real research papers on PubMed
        Note: This requires NCBI E-utilities API
        """
        try:
            base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
            search_term = f"{drug_name} AND {condition} AND repurposing"
            
            async with aiohttp.ClientSession() as session:
                # Search PubMed
                search_url = f"{base_url}/esearch.fcgi"
                params = {
                    "db": "pubmed",
                    "term": search_term,
                    "retmax": 5,
                    "retmode": "json"
                }
                
                async with session.get(search_url, params=params, timeout=10) as response:
                    if response.status == 200:
                        data = await response.json()
                        pmids = data.get("esearchresult", {}).get("idlist", [])
                        
                        if pmids:
                            # Fetch summaries
                            summary_url = f"{base_url}/esummary.fcgi"
                            summary_params = {
                                "db": "pubmed",
                                "id": ",".join(pmids),
                                "retmode": "json"
                            }
                            
                            async with session.get(summary_url, params=summary_params, timeout=10) as sum_response:
                                if sum_response.status == 200:
                                    sum_data = await sum_response.json()
                                    papers = []
                                    for pmid in pmids:
                                        paper_data = sum_data.get("result", {}).get(pmid, {})
                                        if paper_data:
                                            papers.append({
                                                "title": paper_data.get("title", ""),
                                                "authors": ", ".join(paper_data.get("authors", [])[:3]),
                                                "journal": paper_data.get("source", ""),
                                                "year": paper_data.get("pubdate", "").split()[0] if paper_data.get("pubdate") else "",
                                                "pmid": pmid,
                                                "source": "PubMed/NCBI"
                                            })
                                    return papers
        except Exception as e:
            print(f"  ⚠️  PubMed search failed: {str(e)[:100]}")
        
        return []

