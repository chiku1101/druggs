"""
Medicine Dataset CSV Service
Loads and queries the real medicine_dataset.csv file
"""

import pandas as pd
import os
from typing import Dict, List, Optional
from fuzzywuzzy import fuzz
import asyncio

class MedicineDatasetService:
    """
    Service to load and query the medicine_dataset.csv file
    Provides genuine drug information from the dataset
    """
    
    def __init__(self, csv_path: str = None):
        if csv_path is None:
            # Default path relative to this file
            current_dir = os.path.dirname(os.path.abspath(__file__))
            csv_path = os.path.join(current_dir, "medicine_dataset.csv")
        
        self.csv_path = csv_path
        self.df = None
        self.loaded = False
        print(f"✅ Medicine Dataset Service initialized (CSV: {csv_path})")
    
    async def load_dataset(self):
        """
        Load the CSV dataset into memory
        """
        if self.loaded and self.df is not None:
            return
        
        try:
            print(f"📂 Loading medicine dataset from CSV ({self.csv_path})...")
            
            # Load CSV with pandas
            self.df = pd.read_csv(self.csv_path)
            
            # Clean column names (remove spaces, make lowercase)
            self.df.columns = self.df.columns.str.strip().str.lower()
            
            # Clean data
            self.df = self.df.dropna(subset=['name'])  # Remove rows without drug names
            
            self.loaded = True
            print(f"  ✅ Loaded {len(self.df)} medicines from CSV")
            print(f"  📊 Columns: {', '.join(self.df.columns.tolist())}")
            
        except Exception as e:
            print(f"  ❌ Error loading CSV: {e}")
            self.df = pd.DataFrame()  # Empty dataframe as fallback
            self.loaded = True
    
    async def search_drug(self, drug_name: str) -> List[Dict]:
        """
        Search for a drug by name (fuzzy matching)
        Returns all matching records
        """
        await self.load_dataset()
        
        if self.df.empty:
            return []
        
        drug_name_lower = drug_name.lower().strip()
        
        # Exact match first
        exact_matches = self.df[self.df['name'].str.lower() == drug_name_lower]
        
        if len(exact_matches) > 0:
            return self._dataframe_to_dict_list(exact_matches)
        
        # Fuzzy match (similarity > 80)
        matches = []
        for idx, row in self.df.iterrows():
            similarity = fuzz.ratio(drug_name_lower, str(row['name']).lower())
            if similarity >= 80:
                matches.append((similarity, row))
        
        # Sort by similarity and take top 10
        matches.sort(key=lambda x: x[0], reverse=True)
        top_matches = [row for _, row in matches[:10]]
        
        if top_matches:
            return self._dataframe_to_dict_list(pd.DataFrame(top_matches))
        
        return []
    
    async def search_by_indication(self, indication: str) -> List[Dict]:
        """
        Find all drugs used for a specific indication
        """
        await self.load_dataset()
        
        if self.df.empty:
            return []
        
        indication_lower = indication.lower().strip()
        
        # Search in indication column
        matches = self.df[
            self.df['indication'].str.lower().str.contains(indication_lower, na=False)
        ]
        
        return self._dataframe_to_dict_list(matches.head(20))  # Limit to 20
    
    async def search_by_category(self, category: str) -> List[Dict]:
        """
        Find all drugs in a specific category
        """
        await self.load_dataset()
        
        if self.df.empty:
            return []
        
        category_lower = category.lower().strip()
        
        matches = self.df[
            self.df['category'].str.lower().str.contains(category_lower, na=False)
        ]
        
        return self._dataframe_to_dict_list(matches.head(20))
    
    async def get_drug_details(self, drug_name: str) -> Optional[Dict]:
        """
        Get comprehensive details for a specific drug
        Aggregates all records for the drug
        """
        drugs = await self.search_drug(drug_name)
        
        if not drugs:
            return None
        
        # Aggregate data from all records
        first_drug = drugs[0]
        
        # Collect all unique values
        all_categories = list(set(d.get('category', '') for d in drugs if d.get('category')))
        all_forms = list(set(d.get('dosage form', '') for d in drugs if d.get('dosage form')))
        all_indications = list(set(d.get('indication', '') for d in drugs if d.get('indication')))
        all_manufacturers = list(set(d.get('manufacturer', '') for d in drugs if d.get('manufacturer')))
        all_classifications = list(set(d.get('classification', '') for d in drugs if d.get('classification')))
        
        # Get strength range
        strengths = [d.get('strength', '') for d in drugs if d.get('strength')]
        strength_range = f"{min(strengths, key=len)} - {max(strengths, key=len)}" if strengths else "Variable"
        
        return {
            "name": first_drug.get('name', drug_name),
            "generic_name": first_drug.get('name', drug_name),
            "categories": all_categories,
            "dosage_forms": all_forms,
            "strength_range": strength_range,
            "indications": all_indications,
            "manufacturers": all_manufacturers,
            "classifications": all_classifications,
            "record_count": len(drugs),
            "fda_approved": "Prescription" in all_classifications or "Over-the-Counter" in all_classifications,
            "source": "medicine_dataset.csv",
            "all_records": drugs[:5]  # Include first 5 records for details
        }
    
    async def find_repurposing_opportunities(self, drug_name: str, target_condition: str) -> Dict:
        """
        Find repurposing opportunities for a drug
        Checks if drug is already used for the condition, or if similar drugs are
        """
        await self.load_dataset()
        
        if self.df.empty:
            return {
                "already_approved": False,
                "similar_drugs_count": 0,
                "similar_drugs": [],
                "evidence_level": "unknown"
            }
        
        drug_name_lower = drug_name.lower().strip()
        condition_lower = target_condition.lower().strip()
        
        # Direct check: drug name matches AND indication matches
        matching_records = self.df[
            (self.df['name'].str.lower() == drug_name_lower) &
            (self.df['indication'].str.lower() == condition_lower)
        ]
        
        already_used = len(matching_records) > 0
        record_count = len(matching_records)
        
        # Get drug records for category matching
        drug_records = await self.search_drug(drug_name)
        
        # Find similar drugs used for this condition
        similar_drugs = await self.search_by_indication(target_condition)
        
        # Filter by same category
        drug_categories = list(set(r.get('category', '') for r in drug_records if r.get('category')))
        similar_in_category = [
            d for d in similar_drugs
            if any(cat.lower() in str(d.get('category', '')).lower() for cat in drug_categories)
        ]
        
        return {
            "already_approved": already_used,
            "record_count": record_count,
            "similar_drugs_count": len(similar_in_category),
            "similar_drugs": similar_in_category[:5],
            "evidence_level": "approved" if already_used else "investigational",
            "confidence": "high" if record_count > 10 else "moderate" if record_count > 0 else "low"
        }
    
    async def get_statistics(self) -> Dict:
        """
        Get dataset statistics
        """
        await self.load_dataset()
        
        if self.df.empty:
            return {}
        
        return {
            "total_drugs": len(self.df),
            "unique_drug_names": self.df['name'].nunique(),
            "categories": self.df['category'].value_counts().to_dict(),
            "indications": self.df['indication'].value_counts().head(10).to_dict(),
            "manufacturers": self.df['manufacturer'].value_counts().head(10).to_dict(),
            "classifications": self.df['classification'].value_counts().to_dict()
        }
    
    def _dataframe_to_dict_list(self, df: pd.DataFrame) -> List[Dict]:
        """
        Convert pandas DataFrame to list of dictionaries
        """
        if df.empty:
            return []
        
        return df.to_dict('records')
    
    async def search_fuzzy(self, query: str, limit: int = 10) -> List[Dict]:
        """
        Fuzzy search across all columns
        """
        await self.load_dataset()
        
        if self.df.empty:
            return []
        
        query_lower = query.lower().strip()
        matches = []
        
        for idx, row in self.df.iterrows():
            # Check all text columns
            text_to_search = ' '.join([
                str(row.get('name', '')),
                str(row.get('category', '')),
                str(row.get('indication', '')),
                str(row.get('manufacturer', ''))
            ]).lower()
            
            if query_lower in text_to_search:
                similarity = fuzz.partial_ratio(query_lower, text_to_search)
                matches.append((similarity, row))
        
        # Sort by similarity
        matches.sort(key=lambda x: x[0], reverse=True)
        top_matches = [row for _, row in matches[:limit]]
        
        return self._dataframe_to_dict_list(pd.DataFrame(top_matches))

