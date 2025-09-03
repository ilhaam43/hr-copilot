from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from .models import AIDocument, DocumentCategory, TrainingData, AIIntent, KnowledgeBaseEntry
import os

class DocumentUploadForm(forms.ModelForm):
    """Form for uploading AI training documents"""
    
    class Meta:
        model = AIDocument
        fields = ['title', 'description', 'file', 'category']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('Enter document title')
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': _('Enter document description (optional)')
            }),
            'file': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf,.docx,.doc,.txt,.xlsx,.xls'
            }),
            'category': forms.Select(attrs={
                'class': 'form-control'
            })
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = DocumentCategory.objects.filter(is_active=True)
        self.fields['category'].empty_label = _('Select a category')
    
    def clean_file(self):
        file = self.cleaned_data.get('file')
        if file:
            # Check file size (max 50MB)
            if file.size > 50 * 1024 * 1024:
                raise ValidationError(_('File size cannot exceed 50MB.'))
            
            # Check file extension
            allowed_extensions = ['.pdf', '.docx', '.doc', '.txt', '.xlsx', '.xls']
            file_extension = os.path.splitext(file.name)[1].lower()
            if file_extension not in allowed_extensions:
                raise ValidationError(
                    _('File type not supported. Allowed types: PDF, Word, Excel, Text files.')
                )
        
        return file
    
    def clean_title(self):
        title = self.cleaned_data.get('title')
        if title:
            # Check for duplicate titles in the same category
            category = self.cleaned_data.get('category')
            if category:
                existing = AIDocument.objects.filter(
                    title__iexact=title, 
                    category=category
                ).exclude(pk=self.instance.pk if self.instance else None)
                if existing.exists():
                    raise ValidationError(
                        _('A document with this title already exists in the selected category.')
                    )
        return title

class DocumentCategoryForm(forms.ModelForm):
    """Form for managing document categories"""
    
    class Meta:
        model = DocumentCategory
        fields = ['name', 'description', 'color', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('Enter category name')
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': _('Enter category description')
            }),
            'color': forms.TextInput(attrs={
                'class': 'form-control',
                'type': 'color'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }
    
    def clean_name(self):
        name = self.cleaned_data.get('name')
        if name:
            existing = DocumentCategory.objects.filter(
                name__iexact=name
            ).exclude(pk=self.instance.pk if self.instance else None)
            if existing.exists():
                raise ValidationError(_('A category with this name already exists.'))
        return name

class TrainingDataForm(forms.ModelForm):
    """Form for managing training data"""
    
    class Meta:
        model = TrainingData
        fields = [
            'name', 'training_type', 'input_text', 'expected_output',
            'intent_label', 'confidence_threshold', 'source_document'
        ]
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('Enter training data name')
            }),
            'training_type': forms.Select(attrs={
                'class': 'form-control'
            }),
            'input_text': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': _('Enter input text for training')
            }),
            'expected_output': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': _('Enter expected output')
            }),
            'intent_label': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('Enter intent label (optional)')
            }),
            'confidence_threshold': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0.0',
                'max': '1.0',
                'step': '0.1'
            }),
            'source_document': forms.Select(attrs={
                'class': 'form-control'
            })
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['source_document'].queryset = AIDocument.objects.filter(
            status__in=['processed', 'approved']
        )
        self.fields['source_document'].empty_label = _('Select source document (optional)')
        self.fields['source_document'].required = False

class AIIntentForm(forms.ModelForm):
    """Form for managing AI intents"""
    
    examples_text = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 4,
            'placeholder': _('Enter example phrases, one per line')
        }),
        help_text=_('Enter example phrases that trigger this intent, one per line'),
        required=False
    )
    
    responses_text = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 4,
            'placeholder': _('Enter possible responses, one per line')
        }),
        help_text=_('Enter possible responses for this intent, one per line'),
        required=False
    )
    
    entities_text = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': _('Enter required entities, one per line')
        }),
        help_text=_('Enter required entities for this intent, one per line'),
        required=False
    )
    
    class Meta:
        model = AIIntent
        fields = [
            'name', 'description', 'confidence_score', 'is_active'
        ]
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('Enter intent name')
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': _('Enter intent description')
            }),
            'confidence_score': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0.0',
                'max': '1.0',
                'step': '0.1'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            # Populate text fields from JSON data
            self.fields['examples_text'].initial = '\n'.join(self.instance.examples or [])
            self.fields['responses_text'].initial = '\n'.join(self.instance.responses or [])
            self.fields['entities_text'].initial = '\n'.join(self.instance.entities or [])
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        
        # Convert text fields to JSON arrays
        examples_text = self.cleaned_data.get('examples_text', '')
        responses_text = self.cleaned_data.get('responses_text', '')
        entities_text = self.cleaned_data.get('entities_text', '')
        
        instance.examples = [line.strip() for line in examples_text.split('\n') if line.strip()]
        instance.responses = [line.strip() for line in responses_text.split('\n') if line.strip()]
        instance.entities = [line.strip() for line in entities_text.split('\n') if line.strip()]
        
        if commit:
            instance.save()
        return instance

class KnowledgeBaseEntryForm(forms.ModelForm):
    """Form for managing knowledge base entries"""
    
    class Meta:
        model = KnowledgeBaseEntry
        fields = [
            'title', 'content', 'entry_type', 'keywords', 
            'source_document', 'confidence_score', 'is_active'
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('Enter entry title')
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 6,
                'placeholder': _('Enter knowledge base content')
            }),
            'entry_type': forms.Select(attrs={
                'class': 'form-control'
            }),
            'keywords': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('Enter keywords separated by commas')
            }),
            'source_document': forms.Select(attrs={
                'class': 'form-control'
            }),
            'confidence_score': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0.0',
                'max': '1.0',
                'step': '0.1'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['source_document'].queryset = AIDocument.objects.filter(
            status__in=['processed', 'approved']
        )

class DocumentSearchForm(forms.Form):
    """Form for searching documents"""
    query = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': _('Search documents...'),
            'autocomplete': 'off'
        })
    )
    
    category = forms.ModelChoiceField(
        queryset=DocumentCategory.objects.filter(is_active=True),
        required=False,
        empty_label=_('All Categories'),
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )
    
    status = forms.ChoiceField(
        choices=[('', _('All Status'))] + AIDocument.STATUS_CHOICES,
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )
    
    file_type = forms.CharField(
        max_length=10,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': _('File type (e.g., pdf, docx)')
        })
    )