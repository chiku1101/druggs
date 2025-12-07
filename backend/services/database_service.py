"""
MongoDB Database Service for Medicine Dataset
Stores and queries medicine data in MongoDB
"""

import os
import pandas as pd
import certifi
from typing import List, Dict, Optional
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import MongoClient, ASCENDING, TEXT
from pymongo.errors import ConnectionFailure, DuplicateKeyError
import asyncio


class MongoDBService:
    """
    MongoDB service for storing and querying medicine data
    """
    
    def __init__(self, connection_string: str = None):
        """
        Initialize MongoDB connection
        
        Args:
            connection_string: MongoDB URI (default: MongoDB Atlas)
        """
        # Load environment variables
        from dotenv import load_dotenv
        load_dotenv()
        
        self.connection_string = connection_string or os.getenv(
            "MONGODB_URI", 
            "mongodb+srv://chaitanyasonar339_db_user:8dgTpyDen3dZUSTW@cluster0.bcjr0cw.mongodb.net/?appName=Cluster0"
        )
        self.database_name = "drug_repurposing"
        self.collection_name = "medicines"
        
        # Sync client for initial setup
        self.sync_client = None
        self.sync_db = None
        self.sync_collection = None
        
        # Async client for queries
        self.async_client = None
        self.async_db = None
        self.async_collection = None
        
        self.is_connected = False
        print("  🗄️ MongoDB Service initialized")
    
    def connect_sync(self) -> bool:
        """Establish synchronous connection to MongoDB"""
        try:
            self.sync_client = MongoClient(
                self.connection_string, 
                serverSelectionTimeoutMS=5000,
                tlsCAFile=certifi.where()  # Use certifi for SSL
            )
            # Test connection
            self.sync_client.admin.command('ping')
            self.sync_db = self.sync_client[self.database_name]
            self.sync_collection = self.sync_db[self.collection_name]
            self.is_connected = True
            print(f"  ✅ Connected to MongoDB Atlas: {self.database_name}")
            return True
        except ConnectionFailure as e:
            print(f"  ❌ MongoDB connection failed: {e}")
            self.is_connected = False
            return False
    
    async def connect_async(self) -> bool:
        """Establish asynchronous connection to MongoDB"""
        try:
            self.async_client = AsyncIOMotorClient(
                self.connection_string, 
                serverSelectionTimeoutMS=5000,
                tlsCAFile=certifi.where()  # Use certifi for SSL
            )
            # Test connection
            await self.async_client.admin.command('ping')
            self.async_db = self.async_client[self.database_name]
            self.async_collection = self.async_db[self.collection_name]
            self.is_connected = True
            print(f"  ✅ Async MongoDB Atlas connected: {self.database_name}")
            return True
        except Exception as e:
            print(f"  ❌ Async MongoDB connection failed: {e}")
            self.is_connected = False
            return False
    
    def create_indexes(self):
        """Create indexes for faster queries"""
        if self.sync_collection is None:
            return
        
        try:
            # Text index for full-text search
            self.sync_collection.create_index([("Name", TEXT), ("Indication", TEXT)])
            # Regular indexes
            self.sync_collection.create_index([("Name", ASCENDING)])
            self.sync_collection.create_index([("Category", ASCENDING)])
            self.sync_collection.create_index([("Indication", ASCENDING)])
            self.sync_collection.create_index([("Manufacturer", ASCENDING)])
            self.sync_collection.create_index([("Classification", ASCENDING)])
            print("  ✅ MongoDB indexes created")
        except Exception as e:
            print(f"  ⚠️ Index creation warning: {e}")
    
    def load_csv_to_mongodb(self, csv_path: str, force_reload: bool = False) -> int:
        """
        Load CSV data into MongoDB
        
        Args:
            csv_path: Path to the CSV file
            force_reload: If True, drop existing data and reload
            
        Returns:
            Number of documents inserted
        """
        if not self.is_connected:
            if not self.connect_sync():
                return 0
        
        # Check if data already exists
        existing_count = self.sync_collection.count_documents({})
        if existing_count > 0 and not force_reload:
            print(f"  ℹ️ MongoDB already has {existing_count} medicines (use force_reload=True to reload)")
            return existing_count
        
        if force_reload and existing_count > 0:
            print(f"  🗑️ Dropping existing {existing_count} documents...")
            self.sync_collection.drop()
        
        try:
            # Read CSV
            print(f"  📂 Loading CSV: {csv_path}")
            df = pd.read_csv(csv_path)
            
            # Convert to list of dicts
            records = df.to_dict('records')
            
            # Add unique ID to each record
            for i, record in enumerate(records):
                record['_id'] = f"MED_{i+1:06d}"
                # Clean up NaN values
                for key, value in record.items():
                    if pd.isna(value):
                        record[key] = None
            
            # Insert in batches for better performance
            batch_size = 5000
            total_inserted = 0
            
            for i in range(0, len(records), batch_size):
                batch = records[i:i + batch_size]
                try:
                    result = self.sync_collection.insert_many(batch, ordered=False)
                    total_inserted += len(result.inserted_ids)
                    print(f"    Inserted batch {i//batch_size + 1}: {len(result.inserted_ids)} documents")
                except DuplicateKeyError:
                    # Some duplicates, continue anyway
                    pass
            
            # Create indexes after loading
            self.create_indexes()
            
            print(f"  ✅ Loaded {total_inserted} medicines into MongoDB")
            return total_inserted
            
        except Exception as e:
            print(f"  ❌ Error loading CSV: {e}")
            return 0
    
    # ==================== QUERY METHODS ====================
    
    async def search_drug(self, drug_name: str, limit: int = 10) -> List[Dict]:
        """
        Search for a drug by name (fuzzy matching)
        """
        if self.async_collection is None:
            await self.connect_async()
        
        if self.async_collection is None:
            return []
        
        try:
            # Case-insensitive regex search
            cursor = self.async_collection.find(
                {"Name": {"$regex": drug_name, "$options": "i"}},
                {"_id": 0}  # Exclude MongoDB ID from results
            ).limit(limit)
            
            results = await cursor.to_list(length=limit)
            return results
        except Exception as e:
            print(f"  ❌ Search error: {e}")
            return []
    
    async def get_drug_details(self, drug_name: str) -> Dict:
        """
        Get aggregated details for a drug
        """
        if self.async_collection is None:
            await self.connect_async()
        
        if self.async_collection is None:
            return {}
        
        try:
            # Find all records for this drug
            cursor = self.async_collection.find(
                {"Name": {"$regex": f"^{drug_name}$", "$options": "i"}},
                {"_id": 0}
            )
            
            records = await cursor.to_list(length=100)
            
            if not records:
                # Try partial match
                cursor = self.async_collection.find(
                    {"Name": {"$regex": drug_name, "$options": "i"}},
                    {"_id": 0}
                ).limit(10)
                records = await cursor.to_list(length=10)
            
            if not records:
                return {}
            
            # Aggregate data from all records
            return {
                "name": records[0].get("Name"),
                "category": records[0].get("Category"),
                "dosage_forms": list(set(r.get("Dosage Form") for r in records if r.get("Dosage Form"))),
                "strengths": list(set(r.get("Strength") for r in records if r.get("Strength"))),
                "manufacturers": list(set(r.get("Manufacturer") for r in records if r.get("Manufacturer"))),
                "indications": list(set(r.get("Indication") for r in records if r.get("Indication"))),
                "classification": records[0].get("Classification"),
                "record_count": len(records),
                "source": "MongoDB"
            }
        except Exception as e:
            print(f"  ❌ Get details error: {e}")
            return {}
    
    async def search_by_indication(self, indication: str, limit: int = 20) -> List[Dict]:
        """
        Find drugs by indication/condition
        """
        if self.async_collection is None:
            await self.connect_async()
        
        if self.async_collection is None:
            return []
        
        try:
            cursor = self.async_collection.find(
                {"Indication": {"$regex": indication, "$options": "i"}},
                {"_id": 0}
            ).limit(limit)
            
            return await cursor.to_list(length=limit)
        except Exception as e:
            print(f"  ❌ Indication search error: {e}")
            return []
    
    async def search_by_category(self, category: str, limit: int = 20) -> List[Dict]:
        """
        Find drugs by category (Antibiotic, Antiviral, etc.)
        """
        if self.async_collection is None:
            await self.connect_async()
        
        if self.async_collection is None:
            return []
        
        try:
            cursor = self.async_collection.find(
                {"Category": {"$regex": category, "$options": "i"}},
                {"_id": 0}
            ).limit(limit)
            
            return await cursor.to_list(length=limit)
        except Exception as e:
            print(f"  ❌ Category search error: {e}")
            return []
    
    async def find_repurposing_opportunities(self, drug_name: str, target_condition: str) -> Dict:
        """
        Check if a drug is already approved for a condition (repurposing check)
        """
        if self.async_collection is None:
            await self.connect_async()
        
        if self.async_collection is None:
            return {"already_approved": False, "evidence": []}
        
        try:
            # Check if drug already treats this condition
            cursor = self.async_collection.find({
                "Name": {"$regex": drug_name, "$options": "i"},
                "Indication": {"$regex": target_condition, "$options": "i"}
            }, {"_id": 0})
            
            matches = await cursor.to_list(length=10)
            
            if matches:
                return {
                    "already_approved": True,
                    "evidence": matches,
                    "message": f"{drug_name} is already approved for {target_condition}",
                    "source": "MongoDB"
                }
            
            # Get drug info anyway
            drug_info = await self.get_drug_details(drug_name)
            
            return {
                "already_approved": False,
                "drug_info": drug_info,
                "message": f"{drug_name} not currently approved for {target_condition}",
                "potential_repurposing": True if drug_info else False,
                "source": "MongoDB"
            }
        except Exception as e:
            print(f"  ❌ Repurposing check error: {e}")
            return {"already_approved": False, "error": str(e)}
    
    async def get_statistics(self) -> Dict:
        """
        Get database statistics
        """
        if self.async_collection is None:
            await self.connect_async()
        
        if self.async_collection is None:
            return {}
        
        try:
            total = await self.async_collection.count_documents({})
            
            # Get unique counts using aggregation
            categories = await self.async_collection.distinct("Category")
            manufacturers = await self.async_collection.distinct("Manufacturer")
            indications = await self.async_collection.distinct("Indication")
            classifications = await self.async_collection.distinct("Classification")
            
            return {
                "total_records": total,
                "unique_categories": len(categories),
                "unique_manufacturers": len(manufacturers),
                "unique_indications": len(indications),
                "classifications": classifications,
                "database": "MongoDB",
                "collection": self.collection_name
            }
        except Exception as e:
            print(f"  ❌ Statistics error: {e}")
            return {}
    
    async def full_text_search(self, query: str, limit: int = 20) -> List[Dict]:
        """
        Full-text search across Name and Indication
        """
        if self.async_collection is None:
            await self.connect_async()
        
        if self.async_collection is None:
            return []
        
        try:
            cursor = self.async_collection.find(
                {"$text": {"$search": query}},
                {"_id": 0, "score": {"$meta": "textScore"}}
            ).sort([("score", {"$meta": "textScore"})]).limit(limit)
            
            return await cursor.to_list(length=limit)
        except Exception as e:
            # Fallback to regex search if text index not available
            return await self.search_drug(query, limit)
    
    def close(self):
        """Close MongoDB connections"""
        if self.sync_client:
            self.sync_client.close()
        if self.async_client:
            self.async_client.close()
        print("  🔌 MongoDB connections closed")


# ==================== INITIALIZATION HELPER ====================

def initialize_mongodb(csv_path: str = None, force_reload: bool = False) -> MongoDBService:
    """
    Helper function to initialize MongoDB with data
    
    Usage:
        db = initialize_mongodb("path/to/medicine_dataset.csv")
    """
    db = MongoDBService()
    
    if db.connect_sync():
        if csv_path:
            db.load_csv_to_mongodb(csv_path, force_reload)
    
    return db


# ==================== TEST ====================

if __name__ == "__main__":
    import asyncio
    
    async def test():
        # Initialize and load data
        csv_path = os.path.join(os.path.dirname(__file__), "medicine_dataset.csv")
        db = initialize_mongodb(csv_path)
        
        if not db.is_connected:
            print("❌ MongoDB not running! Start it with: brew services start mongodb-community")
            return
        
        # Test async queries
        await db.connect_async()
        
        print("\n--- Testing Queries ---")
        
        # Search drug
        results = await db.search_drug("Acetocillin")
        print(f"\n🔍 Search 'Acetocillin': {len(results)} results")
        if results:
            print(f"   First result: {results[0]}")
        
        # Get drug details
        details = await db.get_drug_details("Acetocillin")
        print(f"\n📋 Drug details: {details}")
        
        # Search by indication
        results = await db.search_by_indication("Infection")
        print(f"\n🏥 Drugs for 'Infection': {len(results)} results")
        
        # Repurposing check
        repurposing = await db.find_repurposing_opportunities("Acetocillin", "Diabetes")
        print(f"\n💊 Repurposing check: {repurposing}")
        
        # Statistics
        stats = await db.get_statistics()
        print(f"\n📊 Statistics: {stats}")
        
        db.close()
    
    asyncio.run(test())

