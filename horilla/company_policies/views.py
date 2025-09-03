from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.core.paginator import Paginator
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from employee.models import Employee
from base.models import Company
from .models import (
    PolicyCategory,
    CompanyPolicyDocument,
    PolicyAcknowledgment,
    PolicyTraining,
    PolicyTrainingParticipant
)
from .forms import (
    PolicyCategoryForm,
    CompanyPolicyDocumentForm,
    PolicyAcknowledgmentForm,
    PolicyTrainingForm,
    PolicyTrainingParticipantForm,
    PolicySearchForm
)


@login_required
def policy_dashboard(request):
    """Dashboard utama untuk manajemen kebijakan perusahaan"""
    context = {
        'total_categories': PolicyCategory.objects.count(),
        'total_documents': CompanyPolicyDocument.objects.count(),
        'active_documents': CompanyPolicyDocument.objects.filter(status='active').count(),
        'pending_acknowledgments': PolicyAcknowledgment.objects.filter(is_acknowledged=False).count(),
        'recent_documents': CompanyPolicyDocument.objects.order_by('-created_at')[:5],
        'recent_trainings': PolicyTraining.objects.order_by('-training_date')[:5],
    }
    return render(request, 'company_policies/dashboard.html', context)


# Policy Category Views
@login_required
def policy_category_list(request):
    """Daftar kategori kebijakan"""
    categories = PolicyCategory.objects.all().order_by('name')
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        categories = categories.filter(
            Q(name__icontains=search_query) | 
            Q(description__icontains=search_query)
        )
    
    paginator = Paginator(categories, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
    }
    return render(request, 'company_policies/category_list.html', context)


@login_required
def policy_category_create(request):
    """Membuat kategori kebijakan baru"""
    if request.method == 'POST':
        form = PolicyCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, _('Kategori kebijakan berhasil dibuat.'))
            return redirect('company_policies:category_list')
    else:
        form = PolicyCategoryForm()
    
    context = {'form': form, 'title': _('Buat Kategori Kebijakan')}
    return render(request, 'company_policies/category_form.html', context)


@login_required
def policy_category_edit(request, pk):
    """Edit kategori kebijakan"""
    category = get_object_or_404(PolicyCategory, pk=pk)
    
    if request.method == 'POST':
        form = PolicyCategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, _('Kategori kebijakan berhasil diperbarui.'))
            return redirect('company_policies:category_list')
    else:
        form = PolicyCategoryForm(instance=category)
    
    context = {'form': form, 'category': category, 'title': _('Edit Kategori Kebijakan')}
    return render(request, 'company_policies/category_form.html', context)


@login_required
def policy_category_delete(request, pk):
    """Hapus kategori kebijakan"""
    category = get_object_or_404(PolicyCategory, pk=pk)
    
    if request.method == 'POST':
        category.delete()
        messages.success(request, _('Kategori kebijakan berhasil dihapus.'))
        return redirect('company_policies:category_list')
    
    context = {'category': category}
    return render(request, 'company_policies/category_confirm_delete.html', context)


# Policy Document Views
@login_required
def policy_document_list(request):
    """Daftar dokumen kebijakan"""
    documents = CompanyPolicyDocument.objects.select_related('category').order_by('-created_at')
    
    # Search and filter
    form = PolicySearchForm(request.GET)
    if form.is_valid():
        search_query = form.cleaned_data.get('search_query')
        category = form.cleaned_data.get('category')
        status = form.cleaned_data.get('status')
        company = form.cleaned_data.get('company')
        
        if search_query:
            documents = documents.filter(
                Q(title__icontains=search_query) |
                Q(content__icontains=search_query) |
                Q(legal_basis__icontains=search_query)
            )
        
        if category:
            documents = documents.filter(category=category)
        
        if status:
            documents = documents.filter(status=status)
        
        if company:
            documents = documents.filter(company_id=company)
    
    paginator = Paginator(documents, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search_form': form,
    }
    return render(request, 'company_policies/document_list.html', context)


@login_required
def policy_document_detail(request, pk):
    """Detail dokumen kebijakan"""
    document = get_object_or_404(CompanyPolicyDocument, pk=pk)
    
    # Check if current user has acknowledged this policy
    user_acknowledgment = None
    if hasattr(request.user, 'employee'):
        user_acknowledgment = PolicyAcknowledgment.objects.filter(
            employee=request.user.employee,
            policy_document=document
        ).first()
    
    context = {
        'document': document,
        'user_acknowledgment': user_acknowledgment,
    }
    return render(request, 'company_policies/document_detail.html', context)


@login_required
def policy_document_create(request):
    """Membuat dokumen kebijakan baru"""
    if request.method == 'POST':
        form = CompanyPolicyDocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, _('Dokumen kebijakan berhasil dibuat.'))
            return redirect('company_policies:document_list')
    else:
        form = CompanyPolicyDocumentForm()
    
    context = {'form': form, 'title': _('Buat Dokumen Kebijakan')}
    return render(request, 'company_policies/document_form.html', context)


@login_required
def policy_document_edit(request, pk):
    """Edit dokumen kebijakan"""
    document = get_object_or_404(CompanyPolicyDocument, pk=pk)
    
    if request.method == 'POST':
        form = CompanyPolicyDocumentForm(request.POST, request.FILES, instance=document)
        if form.is_valid():
            form.save()
            messages.success(request, _('Dokumen kebijakan berhasil diperbarui.'))
            return redirect('company_policies:document_detail', pk=document.pk)
    else:
        form = CompanyPolicyDocumentForm(instance=document)
    
    context = {'form': form, 'document': document, 'title': _('Edit Dokumen Kebijakan')}
    return render(request, 'company_policies/document_form.html', context)


@login_required
def policy_document_delete(request, pk):
    """Hapus dokumen kebijakan"""
    document = get_object_or_404(CompanyPolicyDocument, pk=pk)
    
    if request.method == 'POST':
        document.delete()
        messages.success(request, _('Dokumen kebijakan berhasil dihapus.'))
        return redirect('company_policies:document_list')
    
    context = {'document': document}
    return render(request, 'company_policies/document_confirm_delete.html', context)


# Policy Acknowledgment Views
@login_required
def policy_acknowledge(request, document_pk):
    """Acknowledge kebijakan oleh karyawan"""
    document = get_object_or_404(CompanyPolicyDocument, pk=document_pk)
    
    if not hasattr(request.user, 'employee'):
        messages.error(request, _('Anda harus terdaftar sebagai karyawan untuk mengakui kebijakan.'))
        return redirect('company_policies:document_detail', pk=document_pk)
    
    employee = request.user.employee
    
    # Check if already acknowledged
    acknowledgment, created = PolicyAcknowledgment.objects.get_or_create(
        employee=employee,
        policy_document=document,
        defaults={'is_acknowledged': False}
    )
    
    if request.method == 'POST':
        form = PolicyAcknowledgmentForm(request.POST, instance=acknowledgment)
        if form.is_valid():
            ack = form.save(commit=False)
            if ack.is_acknowledged:
                ack.acknowledged_at = timezone.now()
            ack.save()
            
            if ack.is_acknowledged:
                messages.success(request, _('Kebijakan berhasil diakui.'))
            else:
                messages.info(request, _('Status acknowledgment diperbarui.'))
            
            return redirect('company_policies:document_detail', pk=document_pk)
    else:
        form = PolicyAcknowledgmentForm(instance=acknowledgment)
    
    context = {
        'form': form,
        'document': document,
        'acknowledgment': acknowledgment,
    }
    return render(request, 'company_policies/acknowledge_form.html', context)


@login_required
def acknowledgment_list(request):
    """Daftar acknowledgment kebijakan"""
    acknowledgments = PolicyAcknowledgment.objects.select_related(
        'employee', 'policy_document'
    ).order_by('-acknowledged_at')
    
    # Filter
    status_filter = request.GET.get('status', '')
    if status_filter == 'acknowledged':
        acknowledgments = acknowledgments.filter(is_acknowledged=True)
    elif status_filter == 'pending':
        acknowledgments = acknowledgments.filter(is_acknowledged=False)
    
    paginator = Paginator(acknowledgments, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'status_filter': status_filter,
    }
    return render(request, 'company_policies/acknowledgment_list.html', context)


# Policy Training Views
@login_required
def training_list(request):
    """Daftar training kebijakan"""
    trainings = PolicyTraining.objects.select_related('policy_category').order_by('-training_date')
    
    paginator = Paginator(trainings, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {'page_obj': page_obj}
    return render(request, 'company_policies/training_list.html', context)


@login_required
def training_detail(request, pk):
    """Detail training kebijakan"""
    training = get_object_or_404(PolicyTraining, pk=pk)
    participants = PolicyTrainingParticipant.objects.filter(training=training).select_related('employee')
    
    context = {
        'training': training,
        'participants': participants,
    }
    return render(request, 'company_policies/training_detail.html', context)


@login_required
def training_create(request):
    """Membuat training kebijakan baru"""
    if request.method == 'POST':
        form = PolicyTrainingForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, _('Training kebijakan berhasil dibuat.'))
            return redirect('company_policies:training_list')
    else:
        form = PolicyTrainingForm()
    
    context = {'form': form, 'title': _('Buat Training Kebijakan')}
    return render(request, 'company_policies/training_form.html', context)


@login_required
def training_edit(request, pk):
    """Edit training kebijakan"""
    training = get_object_or_404(PolicyTraining, pk=pk)
    
    if request.method == 'POST':
        form = PolicyTrainingForm(request.POST, instance=training)
        if form.is_valid():
            form.save()
            messages.success(request, _('Training kebijakan berhasil diperbarui.'))
            return redirect('company_policies:training_detail', pk=training.pk)
    else:
        form = PolicyTrainingForm(instance=training)
    
    context = {'form': form, 'training': training, 'title': _('Edit Training Kebijakan')}
    return render(request, 'company_policies/training_form.html', context)


@login_required
@require_http_methods(["GET", "POST"])
def api_policy_categories(request):
    """API endpoint untuk mendapatkan kategori kebijakan"""
    if request.method == 'GET':
        categories = PolicyCategory.objects.all().values('id', 'name', 'category_type')
        return JsonResponse({'categories': list(categories)})
    
    elif request.method == 'POST':
        form = PolicyCategoryForm(request.POST)
        if form.is_valid():
            category = form.save()
            return JsonResponse({
                'success': True,
                'category': {
                    'id': category.id,
                    'name': category.name,
                    'category_type': category.category_type
                }
            })
        else:
            return JsonResponse({'success': False, 'errors': form.errors})


@login_required
def policy_statistics(request):
    """Statistik kebijakan perusahaan"""
    stats = {
        'total_categories': PolicyCategory.objects.count(),
        'total_documents': CompanyPolicyDocument.objects.count(),
        'active_documents': CompanyPolicyDocument.objects.filter(status='active').count(),
        'draft_documents': CompanyPolicyDocument.objects.filter(status='draft').count(),
        'archived_documents': CompanyPolicyDocument.objects.filter(status='archived').count(),
        'total_acknowledgments': PolicyAcknowledgment.objects.count(),
        'pending_acknowledgments': PolicyAcknowledgment.objects.filter(is_acknowledged=False).count(),
        'completed_acknowledgments': PolicyAcknowledgment.objects.filter(is_acknowledged=True).count(),
        'total_trainings': PolicyTraining.objects.count(),
        'upcoming_trainings': PolicyTraining.objects.filter(training_date__gt=timezone.now()).count(),
    }
    
    # Category breakdown
    category_stats = []
    for category in PolicyCategory.objects.all():
        category_stats.append({
            'name': category.name,
            'document_count': CompanyPolicyDocument.objects.filter(category=category).count(),
            'training_count': PolicyTraining.objects.filter(policy_category=category).count(),
        })
    
    context = {
        'stats': stats,
        'category_stats': category_stats,
    }
    return render(request, 'company_policies/statistics.html', context)