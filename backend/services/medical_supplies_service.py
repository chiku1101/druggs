"""
Medical Supplies and Components Service
Provides information about medical equipment and supplies needed for drug administration
"""

from typing import Dict, List, Optional

class MedicalSuppliesService:
    """
    Service to manage medical supplies and components database
    """
    
    def __init__(self):
        self.supplies_database = self._load_medical_supplies()
        print("✅ Medical supplies database initialized")
    
    def _load_medical_supplies(self) -> Dict:
        """
        Load comprehensive medical supplies database
        """
        supplies = {
            "MC001": {
                "component_id": "MC001",
                "name": "Syringe 5ml",
                "category": "Consumable",
                "description": "Sterile disposable syringe",
                "brand": "Hindustan Syringes",
                "material": "Plastic",
                "compatibility": "Universal",
                "price_in_inr": 8,
                "stock_quantity": 500,
                "drug_types": ["Injectable", "Intramuscular", "Intravenous", "Subcutaneous"]
            },
            "MC002": {
                "component_id": "MC002",
                "name": "Surgical Gloves",
                "category": "Protective",
                "description": "Latex powdered gloves",
                "brand": "Surelife",
                "material": "Latex",
                "compatibility": "Universal",
                "price_in_inr": 120,
                "stock_quantity": 300,
                "drug_types": ["All drug administration"]
            },
            "MC003": {
                "component_id": "MC003",
                "name": "ECG Electrodes",
                "category": "Monitoring",
                "description": "Disposable ECG pads",
                "brand": "BPL",
                "material": "Gel + Foam",
                "compatibility": "ECG Machines",
                "price_in_inr": 150,
                "stock_quantity": 200,
                "drug_types": ["Cardiac monitoring during administration"]
            },
            "MC004": {
                "component_id": "MC004",
                "name": "Nebulizer Kit",
                "category": "Respiratory",
                "description": "Mask, tube, chamber",
                "brand": "Omron",
                "material": "PVC",
                "compatibility": "Omron Nebulizers",
                "price_in_inr": 250,
                "stock_quantity": 150,
                "drug_types": ["Inhalation", "Nebulized medications", "Respiratory drugs"]
            },
            "MC005": {
                "component_id": "MC005",
                "name": "Stethoscope Diaphragm",
                "category": "Diagnostic",
                "description": "Replacement diaphragm",
                "brand": "Littmann",
                "material": "Rubber",
                "compatibility": "Classic III",
                "price_in_inr": 450,
                "stock_quantity": 80,
                "drug_types": ["Patient monitoring"]
            },
            "MC006": {
                "component_id": "MC006",
                "name": "BP Cuff Small",
                "category": "Diagnostic",
                "description": "Pediatric size cuff",
                "brand": "Rossmax",
                "material": "Nylon",
                "compatibility": "Aneroid/Digital BP Monitor",
                "price_in_inr": 350,
                "stock_quantity": 120,
                "drug_types": ["Blood pressure monitoring", "Antihypertensive drugs"]
            },
            "MC007": {
                "component_id": "MC007",
                "name": "Oxygen Mask Adult",
                "category": "Respiratory",
                "description": "Soft mask with tube",
                "brand": "Romsons",
                "material": "Plastic",
                "compatibility": "O2 Supply",
                "price_in_inr": 70,
                "stock_quantity": 400,
                "drug_types": ["Oxygen therapy", "Respiratory support"]
            },
            "MC008": {
                "component_id": "MC008",
                "name": "IV Cannula 22G",
                "category": "Consumable",
                "description": "Sterile cannula",
                "brand": "Denlay",
                "material": "Teflon",
                "compatibility": "Universal",
                "price_in_inr": 32,
                "stock_quantity": 800,
                "drug_types": ["Intravenous", "IV medications", "Infusion therapy"]
            },
            "MC009": {
                "component_id": "MC009",
                "name": "Test Strips - Glucometer",
                "category": "Laboratory",
                "description": "Blood glucose test strips",
                "brand": "Accu-Chek",
                "material": "Paper/Enzyme",
                "compatibility": "Accu-Chek Devices",
                "price_in_inr": 950,
                "stock_quantity": 90,
                "drug_types": ["Diabetes monitoring", "Antidiabetic drugs", "Insulin"]
            },
            "MC010": {
                "component_id": "MC010",
                "name": "Pulse Oximeter Sensor",
                "category": "Monitoring",
                "description": "Replacement SpO2 sensor",
                "brand": "BPL",
                "material": "Silicone",
                "compatibility": "BPL Monitors",
                "price_in_inr": 1200,
                "stock_quantity": 50,
                "drug_types": ["Oxygen saturation monitoring", "Respiratory drugs"]
            },
            "MC011": {
                "component_id": "MC011",
                "name": "Digital Thermometer Probe Cover",
                "category": "Consumable",
                "description": "Disposable probe covers",
                "brand": "Omron",
                "material": "Plastic",
                "compatibility": "Omron Thermometers",
                "price_in_inr": 60,
                "stock_quantity": 300,
                "drug_types": ["Temperature monitoring", "Antipyretics"]
            },
            "MC012": {
                "component_id": "MC012",
                "name": "Suction Catheter 10Fr",
                "category": "Surgical",
                "description": "Sterile suction tube",
                "brand": "Romsons",
                "material": "PVC",
                "compatibility": "Universal",
                "price_in_inr": 18,
                "stock_quantity": 700,
                "drug_types": ["Airway management", "Respiratory care"]
            },
            "MC013": {
                "component_id": "MC013",
                "name": "Ventilator Circuit",
                "category": "Respiratory",
                "description": "Heated breathing circuit",
                "brand": "Dräger",
                "material": "Silicone",
                "compatibility": "Dräger ICU Ventilators",
                "price_in_inr": 3800,
                "stock_quantity": 20,
                "drug_types": ["Mechanical ventilation", "Sedatives", "Muscle relaxants"]
            },
            "MC014": {
                "component_id": "MC014",
                "name": "Ultrasound Gel",
                "category": "Diagnostic",
                "description": "Conductive gel 5L",
                "brand": "Aquasonic",
                "material": "Gel",
                "compatibility": "All Ultrasound Machines",
                "price_in_inr": 450,
                "stock_quantity": 40,
                "drug_types": ["Diagnostic procedures", "Pain management injections"]
            },
            "MC015": {
                "component_id": "MC015",
                "name": "X-Ray Lead Apron",
                "category": "Protective",
                "description": "0.5mm LE protection apron",
                "brand": "KMI",
                "material": "Lead",
                "compatibility": "Radiology",
                "price_in_inr": 5500,
                "stock_quantity": 15,
                "drug_types": ["Radiological procedures", "Contrast agents"]
            }
        }
        
        return supplies
    
    def get_supplies_for_drug_route(self, route: str) -> List[Dict]:
        """
        Get required supplies based on drug administration route
        """
        supplies = []
        route_lower = route.lower()
        
        for supply_id, supply_data in self.supplies_database.items():
            drug_types = [dt.lower() for dt in supply_data.get("drug_types", [])]
            
            # Match based on route
            if any(route_lower in dt for dt in drug_types) or any(dt in route_lower for dt in drug_types):
                supplies.append(supply_data)
        
        return supplies
    
    def get_supplies_for_condition(self, condition: str) -> List[Dict]:
        """
        Get monitoring/diagnostic supplies needed for specific conditions
        """
        supplies = []
        condition_lower = condition.lower()
        
        # Condition-specific supply mapping
        condition_supply_map = {
            "diabetes": ["MC009", "MC001", "MC002"],  # Glucometer, Syringe, Gloves
            "cardiac": ["MC003", "MC006", "MC002"],  # ECG, BP Cuff, Gloves
            "respiratory": ["MC004", "MC007", "MC010", "MC012"],  # Nebulizer, O2 Mask, Pulse Ox, Suction
            "cancer": ["MC008", "MC001", "MC002", "MC013"],  # IV Cannula, Syringe, Gloves, Ventilator
            "hypertension": ["MC006", "MC002"],  # BP Cuff, Gloves
            "pain": ["MC001", "MC002", "MC014"],  # Syringe, Gloves, Ultrasound Gel
        }
        
        # Find matching supplies
        for key, supply_ids in condition_supply_map.items():
            if key in condition_lower:
                for supply_id in supply_ids:
                    if supply_id in self.supplies_database:
                        supplies.append(self.supplies_database[supply_id])
        
        return supplies
    
    def get_supplies_for_drug_class(self, drug_class: str) -> List[Dict]:
        """
        Get supplies needed for specific drug classes
        """
        supplies = []
        drug_class_lower = drug_class.lower()
        
        # Drug class to supply mapping
        class_supply_map = {
            "injectable": ["MC001", "MC008", "MC002"],  # Syringe, IV Cannula, Gloves
            "intravenous": ["MC008", "MC002"],  # IV Cannula, Gloves
            "nebulized": ["MC004", "MC010"],  # Nebulizer, Pulse Oximeter
            "antidiabetic": ["MC009", "MC001", "MC002"],  # Glucometer, Syringe, Gloves
            "cardiovascular": ["MC003", "MC006", "MC002"],  # ECG, BP Cuff, Gloves
            "respiratory": ["MC004", "MC007", "MC010"],  # Nebulizer, O2 Mask, Pulse Ox
        }
        
        for key, supply_ids in class_supply_map.items():
            if key in drug_class_lower:
                for supply_id in supply_ids:
                    if supply_id in self.supplies_database:
                        supplies.append(self.supplies_database[supply_id])
        
        return supplies
    
    def get_all_supplies(self) -> List[Dict]:
        """
        Get all medical supplies
        """
        return list(self.supplies_database.values())
    
    def search_supply(self, query: str) -> List[Dict]:
        """
        Search supplies by name, category, or description
        """
        query_lower = query.lower()
        results = []
        
        for supply_data in self.supplies_database.values():
            if (query_lower in supply_data["name"].lower() or
                query_lower in supply_data["category"].lower() or
                query_lower in supply_data["description"].lower()):
                results.append(supply_data)
        
        return results
    
    def calculate_supply_cost(self, supplies: List[Dict]) -> Dict:
        """
        Calculate total cost and availability of supplies
        """
        total_cost = sum(s["price_in_inr"] for s in supplies)
        all_available = all(s["stock_quantity"] > 0 for s in supplies)
        low_stock = [s for s in supplies if s["stock_quantity"] < 50]
        
        return {
            "total_cost_inr": total_cost,
            "all_available": all_available,
            "low_stock_items": len(low_stock),
            "supply_count": len(supplies)
        }

