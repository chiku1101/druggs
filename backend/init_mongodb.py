#!/usr/bin/env python3
"""
MongoDB Initialization Script
Run this once to load the medicine dataset into MongoDB
"""

import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from services.database_service import initialize_mongodb

def main():
    print("=" * 50)
    print("🗄️  MongoDB Initialization for Drug Repurposing")
    print("=" * 50)
    
    # Path to CSV file
    csv_path = os.path.join(
        os.path.dirname(__file__), 
        "services", 
        "medicine_dataset.csv"
    )
    
    if not os.path.exists(csv_path):
        print(f"❌ CSV file not found: {csv_path}")
        return
    
    print(f"\n📂 CSV Path: {csv_path}")
    
    # Check if force reload
    force_reload = "--force" in sys.argv
    if force_reload:
        print("⚠️  Force reload enabled - will drop existing data")
    
    # Initialize MongoDB
    print("\n🔌 Connecting to MongoDB...")
    db = initialize_mongodb(csv_path, force_reload=force_reload)
    
    if db.is_connected:
        print("\n" + "=" * 50)
        print("✅ MongoDB initialized successfully!")
        print("=" * 50)
        print("\n📌 Connection Details:")
        print(f"   URI: {db.connection_string}")
        print(f"   Database: {db.database_name}")
        print(f"   Collection: {db.collection_name}")
        print("\n🚀 You can now start the backend with: python main.py")
    else:
        print("\n" + "=" * 50)
        print("❌ MongoDB initialization failed!")
        print("=" * 50)
        print("\n💡 Make sure MongoDB is running:")
        print("   macOS: brew services start mongodb-community")
        print("   Linux: sudo systemctl start mongod")
        print("   Docker: docker run -d -p 27017:27017 mongo")
    
    db.close()

if __name__ == "__main__":
    main()

