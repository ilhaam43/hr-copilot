#!/usr/bin/env python
"""
Script untuk menghasilkan data dummy untuk sistem Asset Management
Mencakup AssetCategory, AssetLot, dan Asset dengan data yang realistis
"""

import os
import sys
import django
import json
from datetime import datetime, timedelta
from decimal import Decimal
from faker import Faker
import random

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'horilla.settings')
django.setup()

from asset.models import AssetCategory, AssetLot, Asset
from base.models import Company
from employee.models import Employee

fake = Faker('id_ID')  # Indonesian locale

def generate_asset_categories():
    """
    Generate realistic asset categories
    """
    categories = [
        {
            "model": "asset.assetcategory",
            "pk": 100,
            "fields": {
                "asset_category_name": "IT Equipment",
                "asset_category_description": "Peralatan teknologi informasi seperti laptop, desktop, server, dan perangkat jaringan",
                "is_active": True,
                "created_at": "2023-01-15T08:00:00Z",
                "company_id": []
            }
        },
        {
            "model": "asset.assetcategory",
            "pk": 101,
            "fields": {
                "asset_category_name": "Office Furniture",
                "asset_category_description": "Furniture kantor seperti meja, kursi, lemari, dan rak",
                "is_active": True,
                "created_at": "2023-01-15T08:15:00Z",
                "company_id": []
            }
        },
        {
            "model": "asset.assetcategory",
            "pk": 102,
            "fields": {
                "asset_category_name": "Vehicles",
                "asset_category_description": "Kendaraan perusahaan seperti mobil, motor, dan truk",
                "is_active": True,
                "created_at": "2023-01-15T08:30:00Z",
                "company_id": []
            }
        },
        {
            "model": "asset.assetcategory",
            "pk": 103,
            "fields": {
                "asset_category_name": "Office Equipment",
                "asset_category_description": "Peralatan kantor seperti printer, scanner, proyektor, dan mesin fotokopi",
                "is_active": True,
                "created_at": "2023-01-15T08:45:00Z",
                "company_id": []
            }
        },
        {
            "model": "asset.assetcategory",
            "pk": 104,
            "fields": {
                "asset_category_name": "Security Equipment",
                "asset_category_description": "Peralatan keamanan seperti CCTV, alarm, dan access control",
                "is_active": True,
                "created_at": "2023-01-15T09:00:00Z",
                "company_id": []
            }
        },
        {
            "model": "asset.assetcategory",
            "pk": 105,
            "fields": {
                "asset_category_name": "Manufacturing Equipment",
                "asset_category_description": "Peralatan produksi dan manufaktur",
                "is_active": True,
                "created_at": "2023-01-15T09:15:00Z",
                "company_id": []
            }
        }
    ]
    return categories

def generate_asset_lots():
    """
    Generate asset lots/batches
    """
    lots = []
    lot_names = [
        "BATCH-IT-2023-001", "BATCH-FURNITURE-2023-001", "BATCH-VEHICLE-2023-001",
        "BATCH-OFFICE-2023-001", "BATCH-SECURITY-2023-001", "BATCH-MFG-2023-001",
        "BATCH-IT-2023-002", "BATCH-FURNITURE-2023-002", "BATCH-VEHICLE-2023-002"
    ]
    
    descriptions = [
        "Batch pembelian peralatan IT Q1 2023",
        "Batch pembelian furniture kantor Q1 2023",
        "Batch pembelian kendaraan operasional 2023",
        "Batch pembelian peralatan kantor Q1 2023",
        "Batch pembelian sistem keamanan 2023",
        "Batch pembelian peralatan manufaktur Q1 2023",
        "Batch pembelian peralatan IT Q2 2023",
        "Batch pembelian furniture kantor Q2 2023",
        "Batch pembelian kendaraan operasional Q2 2023"
    ]
    
    for i, (lot_name, description) in enumerate(zip(lot_names, descriptions)):
        lots.append({
            "model": "asset.assetlot",
            "pk": 100 + i,
            "fields": {
                "lot_number": lot_name,
                "lot_description": description,
                "is_active": True,
                "created_at": fake.date_time_between(start_date='-1y', end_date='now').isoformat() + 'Z',
                "company_id": []
            }
        })
    
    return lots

def generate_assets():
    """
    Generate realistic assets with various categories
    """
    assets = []
    
    # IT Equipment assets
    it_assets = [
        {"name": "Laptop Dell Latitude 5520", "cost": "15000000.00", "category": 100, "lot": 100},
        {"name": "Laptop HP EliteBook 840", "cost": "18000000.00", "category": 100, "lot": 100},
        {"name": "Desktop Dell OptiPlex 7090", "cost": "12000000.00", "category": 100, "lot": 100},
        {"name": "Monitor LG 24 inch", "cost": "2500000.00", "category": 100, "lot": 100},
        {"name": "Monitor Samsung 27 inch", "cost": "3500000.00", "category": 100, "lot": 100},
        {"name": "Server Dell PowerEdge R740", "cost": "85000000.00", "category": 100, "lot": 106},
        {"name": "Switch Cisco Catalyst 2960", "cost": "8500000.00", "category": 100, "lot": 106},
        {"name": "Router Cisco ISR 4331", "cost": "12500000.00", "category": 100, "lot": 106},
        {"name": "UPS APC Smart-UPS 1500VA", "cost": "4500000.00", "category": 100, "lot": 106},
        {"name": "Tablet iPad Air", "cost": "8500000.00", "category": 100, "lot": 106}
    ]
    
    # Office Furniture assets
    furniture_assets = [
        {"name": "Meja Kerja Executive", "cost": "3500000.00", "category": 101, "lot": 101},
        {"name": "Kursi Kantor Ergonomis", "cost": "2500000.00", "category": 101, "lot": 101},
        {"name": "Lemari Arsip 4 Pintu", "cost": "4500000.00", "category": 101, "lot": 101},
        {"name": "Meja Meeting 8 Orang", "cost": "8500000.00", "category": 101, "lot": 101},
        {"name": "Kursi Meeting", "cost": "1500000.00", "category": 101, "lot": 101},
        {"name": "Rak Buku 5 Tingkat", "cost": "2800000.00", "category": 101, "lot": 107},
        {"name": "Sofa Ruang Tamu 3 Dudukan", "cost": "6500000.00", "category": 101, "lot": 107},
        {"name": "Meja Resepsionis", "cost": "5500000.00", "category": 101, "lot": 107}
    ]
    
    # Vehicle assets
    vehicle_assets = [
        {"name": "Toyota Avanza 2022", "cost": "220000000.00", "category": 102, "lot": 102},
        {"name": "Honda CR-V 2023", "cost": "450000000.00", "category": 102, "lot": 102},
        {"name": "Isuzu D-Max 2022", "cost": "380000000.00", "category": 102, "lot": 102},
        {"name": "Honda Beat 2023", "cost": "18500000.00", "category": 102, "lot": 108},
        {"name": "Yamaha NMAX 2023", "cost": "32500000.00", "category": 102, "lot": 108}
    ]
    
    # Office Equipment assets
    office_equipment_assets = [
        {"name": "Printer HP LaserJet Pro", "cost": "4500000.00", "category": 103, "lot": 103},
        {"name": "Scanner Canon DR-C225", "cost": "8500000.00", "category": 103, "lot": 103},
        {"name": "Proyektor Epson EB-X41", "cost": "6500000.00", "category": 103, "lot": 103},
        {"name": "Mesin Fotokopi Canon iR2625", "cost": "25000000.00", "category": 103, "lot": 103},
        {"name": "Shredder Fellowes 79Ci", "cost": "3500000.00", "category": 103, "lot": 103},
        {"name": "Laminator GBC Fusion 3000L", "cost": "2800000.00", "category": 103, "lot": 103}
    ]
    
    # Security Equipment assets
    security_assets = [
        {"name": "CCTV Hikvision DS-2CD2143G0", "cost": "2500000.00", "category": 104, "lot": 104},
        {"name": "DVR Hikvision DS-7608NI", "cost": "4500000.00", "category": 104, "lot": 104},
        {"name": "Access Control ZKTeco inBio160", "cost": "8500000.00", "category": 104, "lot": 104},
        {"name": "Alarm System Paradox SP4000", "cost": "6500000.00", "category": 104, "lot": 104}
    ]
    
    # Manufacturing Equipment assets
    manufacturing_assets = [
        {"name": "Mesin CNC Haas VF-2", "cost": "850000000.00", "category": 105, "lot": 105},
        {"name": "Kompresor Atlas Copco GA22", "cost": "125000000.00", "category": 105, "lot": 105},
        {"name": "Forklift Toyota 8FBE15U", "cost": "185000000.00", "category": 105, "lot": 105},
        {"name": "Welding Machine Lincoln Electric", "cost": "25000000.00", "category": 105, "lot": 105}
    ]
    
    all_assets = it_assets + furniture_assets + vehicle_assets + office_equipment_assets + security_assets + manufacturing_assets
    
    statuses = ["Available", "In use", "Not-Available"]
    status_weights = [0.6, 0.3, 0.1]  # 60% Available, 30% In use, 10% Not-Available
    
    for i, asset_data in enumerate(all_assets):
        # Generate purchase date between 6 months to 2 years ago
        purchase_date = fake.date_between(start_date='-2y', end_date='-6m')
        
        # Generate expiry date 3-5 years from purchase date
        expiry_date = purchase_date + timedelta(days=random.randint(1095, 1825))
        
        # Generate tracking ID
        tracking_id = f"AST-{asset_data['category']}-{str(100 + i).zfill(4)}"
        
        # Select status with weights
        status = random.choices(statuses, weights=status_weights)[0]
        
        assets.append({
            "model": "asset.asset",
            "pk": 100 + i,
            "fields": {
                "asset_name": asset_data["name"],
                "owner": None,  # Will be set when assigned
                "asset_description": f"Aset {asset_data['name']} dengan kondisi baik dan siap digunakan",
                "asset_tracking_id": tracking_id,
                "asset_purchase_date": purchase_date.isoformat(),
                "asset_purchase_cost": float(asset_data["cost"]),
                "asset_category_id": asset_data["category"],
                "asset_status": status,
                "asset_lot_number_id": asset_data["lot"],
                "expiry_date": expiry_date.isoformat(),
                "notify_before": random.randint(7, 30),
                "is_active": True,
                "created_at": fake.date_time_between(start_date=purchase_date, end_date='now').isoformat() + 'Z'
            }
        })
    
    return assets

def main():
    """
    Main function to generate all dummy data
    """
    print("Generating Asset Management dummy data...")
    
    # Generate all data
    categories = generate_asset_categories()
    lots = generate_asset_lots()
    assets = generate_assets()
    
    # Combine all data
    all_data = categories + lots + assets
    
    # Save to JSON file
    output_file = 'asset_dummy_data.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_data, f, indent=2, ensure_ascii=False)
    
    print(f"\nDummy data generated successfully!")
    print(f"Total records: {len(all_data)}")
    print(f"- Asset Categories: {len(categories)}")
    print(f"- Asset Lots: {len(lots)}")
    print(f"- Assets: {len(assets)}")
    print(f"\nData saved to: {output_file}")
    print(f"\nTo load the data into database, run:")
    print(f"python manage.py loaddata {output_file}")

if __name__ == '__main__':
    main()