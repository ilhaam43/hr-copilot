#!/usr/bin/env python3
"""
Demo Script: AI Knowledge Status Monitoring

Script ini mendemonstrasikan cara menggunakan berbagai fitur monitoring
status pemrosesan dan training data dalam sistem AI Knowledge.

Usage:
    python manage.py shell < DEMO_STATUS_MONITORING.py
"""

import os
import sys
import django
from datetime import datetime, timedelta
import json

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'horilla.settings')
django.setup()

from ai_knowledge.models import (
    AIDocument, DocumentCategory, DocumentProcessingLog, 
    TrainingData, AIIntent, KnowledgeBaseEntry
)
from django.contrib.auth.models import User
from django.utils import timezone

print("🚀 AI Knowledge Status Monitoring Demo")
print("=" * 50)

# 1. Cek Status Dokumen
print("\n📄 1. STATUS DOKUMEN")
print("-" * 30)

documents = AIDocument.objects.all()[:10]
if documents:
    print(f"Total dokumen: {AIDocument.objects.count()}")
    print("\nStatus breakdown:")
    
    status_counts = {
        'pending': AIDocument.objects.filter(status='pending').count(),
        'processing': AIDocument.objects.filter(status='processing').count(), 
        'completed': AIDocument.objects.filter(status='completed').count(),
        'failed': AIDocument.objects.filter(status='failed').count()
    }
    
    for status, count in status_counts.items():
        emoji = {
            'pending': '🔘',
            'processing': '🟡', 
            'completed': '🟢',
            'failed': '🔴'
        }
        print(f"  {emoji[status]} {status.capitalize()}: {count}")
    
    print("\nDokumen terbaru:")
    for doc in documents:
        status_emoji = {
            'pending': '🔘',
            'processing': '🟡',
            'completed': '🟢', 
            'failed': '🔴'
        }.get(doc.status, '❓')
        
        progress = getattr(doc, 'processing_progress', 0) or 0
        print(f"  {status_emoji} {doc.title[:40]:<40} | {doc.status:<10} | {progress}%")
else:
    print("❌ Tidak ada dokumen ditemukan")
    print("💡 Tip: Upload dokumen melalui /ai-knowledge/upload/")

# 2. Cek Processing Logs
print("\n📋 2. PROCESSING LOGS")
print("-" * 30)

recent_logs = DocumentProcessingLog.objects.order_by('-created_at')[:10]
if recent_logs:
    print(f"Total logs: {DocumentProcessingLog.objects.count()}")
    print("\nLog terbaru:")
    
    for log in recent_logs:
        level_emoji = {
            'success': '✅',
            'error': '❌',
            'warning': '⚠️',
            'info': 'ℹ️'
        }.get(log.level, '📝')
        
        doc_title = log.document.title[:30] if log.document else "System"
        timestamp = log.created_at.strftime("%H:%M:%S")
        message = log.message[:50] + "..." if len(log.message) > 50 else log.message
        
        print(f"  {level_emoji} [{timestamp}] {doc_title:<30} | {message}")
else:
    print("❌ Tidak ada processing logs")

# 3. Cek Training Data Status
print("\n🧠 3. TRAINING DATA STATUS")
print("-" * 30)

training_data = TrainingData.objects.all()[:5]
if training_data:
    print(f"Total training data: {TrainingData.objects.count()}")
    print("\nTraining data terbaru:")
    
    for data in training_data:
        created_date = data.created_at.strftime("%Y-%m-%d") if hasattr(data, 'created_at') else "Unknown"
        intent_label = data.intent_label[:30] if data.intent_label else "No label"
        training_type = data.training_type
        print(f"  📊 {intent_label:<30} | Type: {training_type:<12} | Created: {created_date}")
else:
    print("❌ Tidak ada training data")
    print("💡 Tip: Buat training data melalui /ai-knowledge/training-data/create/")

# 4. Cek AI Intents Status
print("\n🎯 4. AI INTENTS STATUS")
print("-" * 30)

intents = AIIntent.objects.all()[:5]
if intents:
    print(f"Total AI intents: {AIIntent.objects.count()}")
    print("\nAI Intents:")
    
    for intent in intents:
        created_date = intent.created_at.strftime("%Y-%m-%d") if hasattr(intent, 'created_at') else "Unknown"
        description = intent.description[:20] if intent.description else "No description"
        
        print(f"  🎯 {intent.name[:30]:<30} | {description:<20} | Created: {created_date}")
else:
    print("❌ Tidak ada AI intents")
    print("💡 Tip: Buat AI intent melalui /ai-knowledge/intents/create/")

# 5. Cek Knowledge Base Status
print("\n📚 5. KNOWLEDGE BASE STATUS")
print("-" * 30)

knowledge_entries = KnowledgeBaseEntry.objects.all()[:5]
if knowledge_entries:
    print(f"Total knowledge entries: {KnowledgeBaseEntry.objects.count()}")
    print("\nKnowledge entries:")
    
    for entry in knowledge_entries:
        category = entry.category.name if entry.category else "Uncategorized"
        created_date = entry.created_at.strftime("%Y-%m-%d") if hasattr(entry, 'created_at') else "Unknown"
        status = "✅ Available"
        print(f"  📖 {entry.title[:30]:<30} | {category:<15} | {status}")
else:
    print("❌ Tidak ada knowledge base entries")
    print("💡 Tip: Buat knowledge entry melalui /ai-knowledge/knowledge-base/create/")

# 6. System Health Check
print("\n🏥 6. SYSTEM HEALTH CHECK")
print("-" * 30)

# Cek dokumen yang stuck di processing
stuck_processing = AIDocument.objects.filter(
    status='processing',
    updated_at__lt=timezone.now() - timedelta(hours=1)
)

if stuck_processing.exists():
    print(f"⚠️  {stuck_processing.count()} dokumen mungkin stuck di processing (>1 jam)")
    for doc in stuck_processing[:3]:
        print(f"    📄 {doc.title} - Last update: {doc.updated_at}")
else:
    print("✅ Tidak ada dokumen yang stuck di processing")

# Cek error logs dalam 24 jam terakhir
error_logs = DocumentProcessingLog.objects.filter(
    level='error',
    created_at__gte=timezone.now() - timedelta(days=1)
)

if error_logs.exists():
    print(f"❌ {error_logs.count()} error logs dalam 24 jam terakhir")
    print("   Error terbaru:")
    for log in error_logs[:3]:
        print(f"    🔴 {log.message[:60]}")
else:
    print("✅ Tidak ada error dalam 24 jam terakhir")

# 7. Performance Metrics
print("\n📊 7. PERFORMANCE METRICS")
print("-" * 30)

# Average processing time
processing_logs = DocumentProcessingLog.objects.filter(
    created_at__gte=timezone.now() - timedelta(days=7)
)

if processing_logs.exists():
    print(f"📈 Total processing logs (7 hari): {processing_logs.count()}")
    
    # Success rate
    total_processes = DocumentProcessingLog.objects.filter(
        created_at__gte=timezone.now() - timedelta(days=7)
    ).count()
    
    success_processes = DocumentProcessingLog.objects.filter(
        level='success',
        created_at__gte=timezone.now() - timedelta(days=7)
    ).count()
    
    success_rate = (success_processes / total_processes * 100) if total_processes > 0 else 0
    print(f"📊 Success rate (7 hari): {success_rate:.1f}%")
else:
    print("❌ Tidak ada data performa tersedia")

# 8. Recommendations
print("\n💡 8. REKOMENDASI")
print("-" * 30)

recommendations = []

if AIDocument.objects.filter(status='failed').exists():
    recommendations.append("🔄 Ada dokumen yang gagal diproses - pertimbangkan untuk reprocess")

if AIDocument.objects.filter(status='pending').count() > 10:
    recommendations.append("⏳ Banyak dokumen pending - cek kapasitas processing")

if not TrainingData.objects.exists():
    recommendations.append("🧠 Belum ada training data - mulai buat training data untuk AI")

if AIIntent.objects.count() < 5:
    recommendations.append("🎯 Sedikit AI intents - tambah lebih banyak intent untuk coverage yang lebih baik")

if not recommendations:
    recommendations.append("✅ Sistem berjalan dengan baik!")

for rec in recommendations:
    print(f"  {rec}")

print("\n" + "=" * 50)
print("🎉 Demo selesai! Gunakan URL berikut untuk monitoring:")
print("   📊 Dashboard: /ai-knowledge/")
print("   📄 Documents: /ai-knowledge/documents/")
print("   📋 Logs: /ai-knowledge/processing-logs/")
print("   📈 Analytics: /ai-knowledge/analytics/")
print("=" * 50)