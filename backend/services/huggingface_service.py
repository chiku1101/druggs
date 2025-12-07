"""
Hugging Face Service for Medicine Dataset Integration
Fetches real medicine data from Hugging Face datasets
"""

import os
from typing import Dict, List, Optional
from datasets import load_dataset
from huggingface_hub import hf_hub_download
import pandas as pd
import json

class HuggingFaceMedicineService:
    """
    Service to fetch and query medicine datasets from Hugging Face
    """
    
    def __init__(self):
        self.medicine_cache = {}
        self.datasets_loaded = False
        self.medicine_database = {}
        
    async def initialize_datasets(self):
        """
        Load medicine datasets from Hugging Face
        """
        if self.datasets_loaded:
            return
        
        try:
            print("📦 Loading medicine datasets from Hugging Face...")
            
            # Try to load Hugging Face medical dataset
            try:
                print("  → Loading medical_medicine_dataset from Hugging Face...")
                hf_data = await self._load_huggingface_medical_dataset()
                if hf_data:
                    self.medicine_database.update(hf_data)
                    print(f"  ✅ Loaded {len(hf_data)} medicines from Hugging Face")
            except Exception as e:
                print(f"  ⚠️  Could not load Hugging Face dataset: {e}")
                print("  → Using built-in comprehensive database")
            
            # Load common medicines from built-in comprehensive database
            common_medicines = self._load_common_medicines()
            self.medicine_database.update(common_medicines)
            
            self.datasets_loaded = True
            print(f"✅ Total medicines loaded: {len(self.medicine_database)}")
            
        except Exception as e:
            print(f"⚠️  Error loading datasets: {e}")
            print("  → Using built-in medicine database")
            self.medicine_database = self._load_common_medicines()
            self.datasets_loaded = True
    
    async def _load_huggingface_medical_dataset(self) -> Dict:
        """
        Load medical dataset from Hugging Face
        """
        try:
            # Load the medical medicine dataset
            dataset = load_dataset("darkknight25/medical_medicine_dataset", split="train")
            
            medicines = {}
            for entry in dataset:
                medicine_name = entry.get("medicine_name", "").strip()
                if not medicine_name:
                    continue
                
                # Normalize medicine name
                name_lower = medicine_name.lower()
                
                # Extract information
                description = entry.get("description", "")
                uses = entry.get("uses", "")
                side_effects = entry.get("side_effects", "")
                
                # Parse uses into indications
                indications = []
                if uses:
                    # Simple parsing - split by common delimiters
                    uses_list = uses.replace(",", ";").split(";")
                    indications = [use.strip() for use in uses_list if use.strip()]
                
                # Parse side effects
                side_effects_list = []
                if side_effects:
                    side_effects_list = [se.strip() for se in side_effects.replace(",", ";").split(";") if se.strip()]
                
                medicines[name_lower] = {
                    "name": medicine_name,
                    "generic_name": medicine_name,  # May need refinement
                    "indications": indications if indications else ["See description"],
                    "description": description,
                    "side_effects": side_effects_list,
                    "source": "Hugging Face medical_medicine_dataset",
                    "fda_approved": True,  # Assume approved if in dataset
                    "repurposing_potential": []  # To be determined
                }
            
            return medicines
            
        except Exception as e:
            print(f"  ⚠️  Error loading Hugging Face dataset: {e}")
            return {}
    
    def _load_drug_dataset(self) -> Dict:
        """
        Load drug information dataset
        """
        medicines = {}
        
        # Common FDA-approved drugs with their information
        common_drugs = [
            {
                "name": "Metformin",
                "generic_name": "Metformin",
                "indications": ["Type 2 Diabetes", "PCOS"],
                "mechanism": "Biguanide, decreases hepatic glucose production",
                "class": "Antidiabetic",
                "fda_approved": True,
                "repurposing_potential": ["Cancer", "Aging", "Cardiovascular Disease"]
            },
            {
                "name": "Aspirin",
                "generic_name": "Acetylsalicylic Acid",
                "indications": ["Pain", "Fever", "Cardiovascular Prevention"],
                "mechanism": "COX-1 and COX-2 inhibition",
                "class": "NSAID",
                "fda_approved": True,
                "repurposing_potential": ["Colorectal Cancer", "Preeclampsia"]
            },
            {
                "name": "Sildenafil",
                "generic_name": "Sildenafil Citrate",
                "indications": ["Erectile Dysfunction", "Pulmonary Hypertension"],
                "mechanism": "PDE-5 inhibition",
                "class": "Phosphodiesterase Inhibitor",
                "fda_approved": True,
                "repurposing_potential": ["Altitude Sickness", "Raynaud's Phenomenon"]
            },
            {
                "name": "Thalidomide",
                "generic_name": "Thalidomide",
                "indications": ["Multiple Myeloma", "Leprosy"],
                "mechanism": "Immunomodulatory, antiangiogenic",
                "class": "Immunomodulator",
                "fda_approved": True,
                "repurposing_potential": ["Crohn's Disease", "Behçet's Disease"]
            },
            {
                "name": "Zinc",
                "generic_name": "Zinc Sulfate",
                "indications": ["Zinc Deficiency", "Diarrhea (adjunct)"],
                "mechanism": "Immune function, enzyme cofactor",
                "class": "Mineral Supplement",
                "fda_approved": True,
                "repurposing_potential": ["Common Cold", "Wound Healing"]
            }
        ]
        
        for drug in common_drugs:
            medicines[drug["name"].lower()] = drug
        
        return medicines
    
    async def _load_pubmed_dataset(self) -> Dict:
        """
        Load PubMed medical literature dataset
        """
        try:
            # Load a sample of PubMed dataset (this is a large dataset, so we load a subset)
            dataset = load_dataset("pubmed_qa", "pqa_labeled", split="train[:1000]")
            
            # Extract drug mentions from abstracts
            medicines = {}
            for item in dataset:
                # Extract potential drug names from abstracts
                abstract = item.get("context", "")
                # Simple extraction - in production, use NER models
                # This is a placeholder for actual drug extraction
                pass
            
            return {}
        except Exception as e:
            print(f"  ⚠️  PubMed dataset loading skipped: {e}")
            return {}
    
    def _load_common_medicines(self) -> Dict:
        """
        Load comprehensive common medicines database
        """
        medicines = {
            "metformin": {
                "name": "Metformin",
                "generic_name": "Metformin Hydrochloride",
                "indications": ["Type 2 Diabetes", "PCOS"],
                "mechanism": "Activates AMPK, inhibits hepatic gluconeogenesis",
                "class": "Biguanide Antidiabetic",
                "fda_approved": True,
                "repurposing_potential": ["Cancer", "Aging", "Cardiovascular Disease", "NAFLD"],
                "side_effects": ["GI upset", "Lactic acidosis (rare)"],
                "interactions": ["Alcohol", "Contrast media"]
            },
            "aspirin": {
                "name": "Aspirin",
                "generic_name": "Acetylsalicylic Acid",
                "indications": ["Pain", "Fever", "Cardiovascular Prevention", "Stroke Prevention"],
                "mechanism": "Irreversible COX-1 and COX-2 inhibition",
                "class": "Salicylate NSAID",
                "fda_approved": True,
                "repurposing_potential": ["Colorectal Cancer", "Preeclampsia", "Alzheimer's"],
                "side_effects": ["GI bleeding", "Reye's syndrome (children)"],
                "interactions": ["Warfarin", "Other NSAIDs"]
            },
            "sildenafil": {
                "name": "Sildenafil",
                "generic_name": "Sildenafil Citrate",
                "indications": ["Erectile Dysfunction", "Pulmonary Arterial Hypertension"],
                "mechanism": "PDE-5 inhibition, increases cGMP",
                "class": "Phosphodiesterase-5 Inhibitor",
                "fda_approved": True,
                "repurposing_potential": ["Altitude Sickness", "Raynaud's", "Heart Failure"],
                "side_effects": ["Headache", "Flushing", "Dyspepsia"],
                "interactions": ["Nitrates", "Alpha-blockers"]
            },
            "thalidomide": {
                "name": "Thalidomide",
                "generic_name": "Thalidomide",
                "indications": ["Multiple Myeloma", "Erythema Nodosum Leprosum"],
                "mechanism": "Immunomodulatory, antiangiogenic, TNF-alpha inhibition",
                "class": "Immunomodulator",
                "fda_approved": True,
                "repurposing_potential": ["Crohn's Disease", "Behçet's", "Graft vs Host Disease"],
                "side_effects": ["Teratogenicity", "Peripheral neuropathy", "Thrombosis"],
                "interactions": ["Alcohol", "Sedatives"]
            },
            "zinc": {
                "name": "Zinc",
                "generic_name": "Zinc Sulfate",
                "indications": ["Zinc Deficiency", "Diarrhea (adjunct to ORS)"],
                "mechanism": "Cofactor for enzymes, immune function",
                "class": "Essential Mineral",
                "fda_approved": True,
                "repurposing_potential": ["Common Cold", "Wound Healing", "Acne"],
                "side_effects": ["Nausea", "Metallic taste"],
                "interactions": ["Copper", "Antibiotics"]
            },
            "ibuprofen": {
                "name": "Ibuprofen",
                "generic_name": "Ibuprofen",
                "indications": ["Pain", "Fever", "Inflammation"],
                "mechanism": "COX-1 and COX-2 inhibition",
                "class": "NSAID",
                "fda_approved": True,
                "repurposing_potential": ["Alzheimer's Disease", "Parkinson's"],
                "side_effects": ["GI upset", "Renal impairment"],
                "interactions": ["Aspirin", "Warfarin"]
            },
            "atorvastatin": {
                "name": "Atorvastatin",
                "generic_name": "Atorvastatin Calcium",
                "indications": ["Hyperlipidemia", "Cardiovascular Prevention"],
                "mechanism": "HMG-CoA reductase inhibition",
                "class": "Statin",
                "fda_approved": True,
                "repurposing_potential": ["Alzheimer's", "Cancer", "Osteoporosis"],
                "side_effects": ["Myopathy", "Hepatotoxicity"],
                "interactions": ["Grapefruit", "Cyclosporine"]
            },
            "metoprolol": {
                "name": "Metoprolol",
                "generic_name": "Metoprolol Tartrate",
                "indications": ["Hypertension", "Angina", "Heart Failure"],
                "mechanism": "Beta-1 adrenergic receptor blockade",
                "class": "Beta Blocker",
                "fda_approved": True,
                "repurposing_potential": ["Anxiety", "Migraine Prevention"],
                "side_effects": ["Bradycardia", "Fatigue"],
                "interactions": ["Calcium channel blockers", "Digoxin"]
            }
        }
        
        return medicines
    
    async def search_medicine(self, drug_name: str) -> Optional[Dict]:
        """
        Search for medicine in the database
        """
        await self.initialize_datasets()
        
        drug_lower = drug_name.lower().strip()
        
        # Direct match
        if drug_lower in self.medicine_database:
            return self.medicine_database[drug_lower]
        
        # Fuzzy search
        for key, value in self.medicine_database.items():
            if drug_lower in key or key in drug_lower:
                return value
        
        # Search by generic name
        for key, value in self.medicine_database.items():
            generic = value.get("generic_name", "").lower()
            if drug_lower in generic or generic in drug_lower:
                return value
        
        return None
    
    async def get_repurposing_opportunities(self, drug_name: str) -> List[str]:
        """
        Get known repurposing opportunities for a drug
        """
        medicine = await self.search_medicine(drug_name)
        if medicine:
            return medicine.get("repurposing_potential", [])
        return []
    
    async def get_all_medicines(self) -> List[Dict]:
        """
        Get all medicines in the database
        """
        await self.initialize_datasets()
        return list(self.medicine_database.values())
    
    async def search_medicines_by_condition(self, condition: str) -> List[Dict]:
        """
        Find medicines that could be repurposed for a condition
        """
        await self.initialize_datasets()
        
        condition_lower = condition.lower()
        matches = []
        
        for drug_name, drug_data in self.medicine_database.items():
            # Check repurposing potential
            repurposing = drug_data.get("repurposing_potential", [])
            for potential in repurposing:
                if condition_lower in potential.lower() or potential.lower() in condition_lower:
                    matches.append(drug_data)
                    break
            
            # Check current indications
            indications = drug_data.get("indications", [])
            for indication in indications:
                if condition_lower in indication.lower() or indication.lower() in condition_lower:
                    matches.append(drug_data)
                    break
        
        return matches
    
    async def get_medicine_details(self, drug_name: str) -> Optional[Dict]:
        """
        Get comprehensive details about a medicine
        """
        medicine = await self.search_medicine(drug_name)
        if not medicine:
            return None
        
        return {
            "name": medicine.get("name"),
            "generic_name": medicine.get("generic_name"),
            "indications": medicine.get("indications", []),
            "mechanism": medicine.get("mechanism"),
            "class": medicine.get("class"),
            "fda_approved": medicine.get("fda_approved", False),
            "repurposing_potential": medicine.get("repurposing_potential", []),
            "side_effects": medicine.get("side_effects", []),
            "interactions": medicine.get("interactions", [])
        }

