#!/usr/bin/env python
"""
Script to load asset dummy data directly using Django ORM
"""

import os
import sys
import django
from datetime import datetime, timedelta
from decimal import Decimal
import random

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'horilla.settings')
django.setup()

from asset.models import AssetCategory, AssetLot, Asset

def load_asset_data():
    print("Loading Asset Management dummy data...")
    
    # Clear existing data
    print("Clearing existing data...")
    Asset.objects.all().delete()
    AssetLot.objects.all().delete()
    AssetCategory.objects.all().delete()
    
    # Create Asset Categories
    categories_data = [
        {"name": "IT Equipment", "description": "Computers, laptops, servers, and networking equipment"},
        {"name": "Office Furniture", "description": "Desks, chairs, cabinets, and meeting room furniture"},
        {"name": "Vehicles", "description": "Company cars, motorcycles, and transportation equipment"},
        {"name": "Office Equipment", "description": "Printers, scanners, projectors, and office machines"},
        {"name": "Security Equipment", "description": "CCTV cameras, access control systems, and security devices"},
        {"name": "Manufacturing Equipment", "description": "Industrial machines, tools, and production equipment"}
    ]
    
    categories = {}
    for i, cat_data in enumerate(categories_data, 100):
        category = AssetCategory.objects.create(
            id=i,
            asset_category_name=cat_data["name"],
            asset_category_description=cat_data["description"]
        )
        categories[cat_data["name"]] = category
        print(f"Created category: {category.asset_category_name}")
    
    # Create Asset Lots
    lots_data = [
        {"number": "LOT-IT-2023-001", "description": "IT Equipment Batch Q1 2023"},
        {"number": "LOT-FURN-2023-001", "description": "Office Furniture Batch Q1 2023"},
        {"number": "LOT-VEH-2023-001", "description": "Vehicle Purchase Batch 2023"},
        {"number": "LOT-OFF-2023-001", "description": "Office Equipment Batch Q1 2023"},
        {"number": "LOT-SEC-2023-001", "description": "Security Equipment Installation 2023"},
        {"number": "LOT-MFG-2023-001", "description": "Manufacturing Equipment Upgrade 2023"},
        {"number": "LOT-IT-2023-002", "description": "IT Equipment Batch Q2 2023"},
        {"number": "LOT-FURN-2023-002", "description": "Office Furniture Batch Q2 2023"},
        {"number": "LOT-VEH-2023-002", "description": "Vehicle Maintenance Equipment 2023"}
    ]
    
    lots = {}
    for i, lot_data in enumerate(lots_data, 100):
        lot = AssetLot.objects.create(
            id=i,
            lot_number=lot_data["number"],
            lot_description=lot_data["description"]
        )
        lots[lot_data["number"]] = lot
        print(f"Created lot: {lot.lot_number}")
    
    # Create Assets
    assets_data = [
        # IT Equipment
        {"name": "Laptop Dell Latitude 5520", "cost": Decimal('15000000.00'), "category": "IT Equipment", "lot": "LOT-IT-2023-001"},
        {"name": "Laptop HP EliteBook 840", "cost": Decimal('18000000.00'), "category": "IT Equipment", "lot": "LOT-IT-2023-001"},
        {"name": "Desktop Dell OptiPlex 7090", "cost": Decimal('12000000.00'), "category": "IT Equipment", "lot": "LOT-IT-2023-001"},
        {"name": "Monitor LG 24 inch", "cost": Decimal('2500000.00'), "category": "IT Equipment", "lot": "LOT-IT-2023-001"},
        {"name": "Monitor Samsung 27 inch", "cost": Decimal('3500000.00'), "category": "IT Equipment", "lot": "LOT-IT-2023-001"},
        {"name": "Server Dell PowerEdge R740", "cost": Decimal('85000000.00'), "category": "IT Equipment", "lot": "LOT-IT-2023-002"},
        {"name": "Switch Cisco Catalyst 2960", "cost": Decimal('8500000.00'), "category": "IT Equipment", "lot": "LOT-IT-2023-002"},
        {"name": "Router Cisco ISR 4331", "cost": Decimal('12500000.00'), "category": "IT Equipment", "lot": "LOT-IT-2023-002"},
        {"name": "UPS APC Smart-UPS 1500VA", "cost": Decimal('4500000.00'), "category": "IT Equipment", "lot": "LOT-IT-2023-002"},
        {"name": "Tablet iPad Air", "cost": Decimal('8500000.00'), "category": "IT Equipment", "lot": "LOT-IT-2023-002"},
        
        # Office Furniture
        {"name": "Meja Kerja Executive", "cost": Decimal('3500000.00'), "category": "Office Furniture", "lot": "LOT-FURN-2023-001"},
        {"name": "Kursi Kantor Ergonomis", "cost": Decimal('2500000.00'), "category": "Office Furniture", "lot": "LOT-FURN-2023-001"},
        {"name": "Lemari Arsip 4 Pintu", "cost": Decimal('4500000.00'), "category": "Office Furniture", "lot": "LOT-FURN-2023-001"},
        {"name": "Meja Meeting 8 Orang", "cost": Decimal('8500000.00'), "category": "Office Furniture", "lot": "LOT-FURN-2023-001"},
        {"name": "Kursi Meeting", "cost": Decimal('1500000.00'), "category": "Office Furniture", "lot": "LOT-FURN-2023-001"},
        {"name": "Rak Buku 5 Tingkat", "cost": Decimal('2800000.00'), "category": "Office Furniture", "lot": "LOT-FURN-2023-002"},
        {"name": "Sofa Ruang Tamu 3 Dudukan", "cost": Decimal('6500000.00'), "category": "Office Furniture", "lot": "LOT-FURN-2023-002"},
        {"name": "Meja Resepsionis", "cost": Decimal('5500000.00'), "category": "Office Furniture", "lot": "LOT-FURN-2023-002"},
        
        # Vehicles
        {"name": "Toyota Avanza 2022", "cost": Decimal('22000000.00'), "category": "Vehicles", "lot": "LOT-VEH-2023-001"},
        {"name": "Honda CR-V 2023", "cost": Decimal('45000000.00'), "category": "Vehicles", "lot": "LOT-VEH-2023-001"},
        {"name": "Isuzu D-Max 2022", "cost": Decimal('38000000.00'), "category": "Vehicles", "lot": "LOT-VEH-2023-001"},
        {"name": "Honda Beat 2023", "cost": Decimal('18500000.00'), "category": "Vehicles", "lot": "LOT-VEH-2023-002"},
        {"name": "Yamaha NMAX 2023", "cost": Decimal('32500000.00'), "category": "Vehicles", "lot": "LOT-VEH-2023-002"},
        
        # Office Equipment
        {"name": "Printer HP LaserJet Pro", "cost": Decimal('4500000.00'), "category": "Office Equipment", "lot": "LOT-OFF-2023-001"},
        {"name": "Scanner Canon DR-C225", "cost": Decimal('8500000.00'), "category": "Office Equipment", "lot": "LOT-OFF-2023-001"},
        {"name": "Proyektor Epson EB-X41", "cost": Decimal('6500000.00'), "category": "Office Equipment", "lot": "LOT-OFF-2023-001"},
        {"name": "Mesin Fotokopi Canon iR2625", "cost": Decimal('25000000.00'), "category": "Office Equipment", "lot": "LOT-OFF-2023-001"},
        {"name": "Shredder Fellowes 79Ci", "cost": Decimal('3500000.00'), "category": "Office Equipment", "lot": "LOT-OFF-2023-001"},
        {"name": "Laminator GBC Fusion 3000L", "cost": Decimal('2800000.00'), "category": "Office Equipment", "lot": "LOT-OFF-2023-001"},
        
        # Security Equipment
        {"name": "CCTV Hikvision DS-2CD2143G0", "cost": Decimal('2500000.00'), "category": "Security Equipment", "lot": "LOT-SEC-2023-001"},
        {"name": "DVR Hikvision DS-7608NI", "cost": Decimal('4500000.00'), "category": "Security Equipment", "lot": "LOT-SEC-2023-001"},
        {"name": "Access Control ZKTeco inBio160", "cost": Decimal('8500000.00'), "category": "Security Equipment", "lot": "LOT-SEC-2023-001"},
        {"name": "Alarm System Paradox SP4000", "cost": Decimal('6500000.00'), "category": "Security Equipment", "lot": "LOT-SEC-2023-001"},
        
        # Manufacturing Equipment
        {"name": "Mesin CNC Haas VF-2", "cost": Decimal('85000000.00'), "category": "Manufacturing Equipment", "lot": "LOT-MFG-2023-001"},
        {"name": "Kompresor Atlas Copco GA22", "cost": Decimal('12500000.00'), "category": "Manufacturing Equipment", "lot": "LOT-MFG-2023-001"},
        {"name": "Forklift Toyota 8FBE15U", "cost": Decimal('18500000.00'), "category": "Manufacturing Equipment", "lot": "LOT-MFG-2023-001"},
        {"name": "Welding Machine Lincoln Electric", "cost": Decimal('25000000.00'), "category": "Manufacturing Equipment", "lot": "LOT-MFG-2023-001"}
    ]
    
    statuses = ["Available", "In use", "Not-Available"]
    
    for i, asset_data in enumerate(assets_data, 1000):
        # Generate random dates
        purchase_date = datetime.now().date() - timedelta(days=random.randint(30, 365))
        expiry_date = purchase_date + timedelta(days=random.randint(1095, 1825))  # 3-5 years
        status = random.choice(statuses)
        
        asset = Asset.objects.create(
            id=i,
            asset_name=asset_data["name"],
            asset_tracking_id=f"AST{i:04d}",
            asset_purchase_date=purchase_date,
            asset_purchase_cost=asset_data["cost"],
            asset_category_id=categories[asset_data["category"]],
            asset_status=status,
            asset_lot_number_id=lots[asset_data["lot"]],
            expiry_date=expiry_date,
            notify_before=30
        )
        print(f"Created asset: {asset.asset_name} - {asset.asset_status}")
    
    print("\nAsset dummy data loaded successfully!")
    print(f"Total records created:")
    print(f"- Asset Categories: {AssetCategory.objects.count()}")
    print(f"- Asset Lots: {AssetLot.objects.count()}")
    print(f"- Assets: {Asset.objects.count()}")

if __name__ == "__main__":
    load_asset_data()