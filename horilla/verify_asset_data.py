#!/usr/bin/env python
import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'horilla.settings')
django.setup()

from asset.models import Asset, AssetCategory, AssetLot

print('=== Asset Data Verification ===')
print(f'Asset Categories: {AssetCategory.objects.count()}')
print(f'Asset Lots: {AssetLot.objects.count()}')
print(f'Assets: {Asset.objects.count()}')

print('\n=== Asset Categories ===')
for category in AssetCategory.objects.all():
    print(f'- {category.asset_category_name}')

print('\n=== Sample Assets ===')
for asset in Asset.objects.all()[:10]:
    print(f'- {asset.asset_name}: Rp {asset.asset_purchase_cost:,.2f} ({asset.asset_status})')

print('\n=== Assets by Category ===')
for category in AssetCategory.objects.all():
    count = Asset.objects.filter(asset_category_id=category).count()
    print(f'- {category.asset_category_name}: {count} assets')

print('\n=== Assets by Status ===')
status_counts = {}
for asset in Asset.objects.all():
    status = asset.asset_status
    status_counts[status] = status_counts.get(status, 0) + 1

for status, count in status_counts.items():
    print(f'- {status}: {count} assets')

print('\nData verification completed successfully!')