from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Budget, BudgetCategory, BudgetAllocation, BudgetExpense
from employee.models import Employee, Department
from base.forms import ModelForm


class BudgetCategoryForm(ModelForm):
    """
    Form for Budget Category
    """
    class Meta:
        model = BudgetCategory
        fields = ['name', 'description', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'oh-input w-100'}),
            'description': forms.Textarea(attrs={'class': 'oh-input w-100', 'rows': 3}),
        }


class BudgetForm(ModelForm):
    """
    Form for Budget
    """
    class Meta:
        model = Budget
        fields = [
            'name', 'description', 'department', 'category', 
            'total_amount', 'start_date', 'end_date', 'status'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'oh-input w-100'}),
            'description': forms.Textarea(attrs={'class': 'oh-input w-100', 'rows': 3}),
            'department': forms.Select(attrs={'class': 'oh-select oh-select-2 w-100'}),
            'category': forms.Select(attrs={'class': 'oh-select oh-select-2 w-100'}),
            'total_amount': forms.NumberInput(attrs={'class': 'oh-input w-100', 'step': '0.01'}),
            'start_date': forms.DateInput(attrs={'class': 'oh-input w-100', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'oh-input w-100', 'type': 'date'}),
            'status': forms.Select(attrs={'class': 'oh-select oh-select-2 w-100'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['department'].queryset = Department.objects.filter(is_active=True)
        self.fields['category'].queryset = BudgetCategory.objects.filter(is_active=True)


class BudgetAllocationForm(ModelForm):
    """
    Form for Budget Allocation
    """
    class Meta:
        model = BudgetAllocation
        fields = ['budget', 'allocated_to', 'amount', 'purpose', 'allocation_date']
        widgets = {
            'budget': forms.Select(attrs={'class': 'oh-select oh-select-2 w-100'}),
            'allocated_to': forms.Select(attrs={'class': 'oh-select oh-select-2 w-100'}),
            'amount': forms.NumberInput(attrs={'class': 'oh-input w-100', 'step': '0.01'}),
            'purpose': forms.TextInput(attrs={'class': 'oh-input w-100'}),
            'allocation_date': forms.DateInput(attrs={'class': 'oh-input w-100', 'type': 'date'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['budget'].queryset = Budget.objects.filter(status__in=['approved', 'active'])
        self.fields['allocated_to'].queryset = Employee.objects.filter(is_active=True)


class BudgetExpenseForm(ModelForm):
    """
    Form for Budget Expense
    """
    class Meta:
        model = BudgetExpense
        fields = [
            'budget', 'allocation', 'description', 'amount', 
            'expense_date', 'receipt'
        ]
        widgets = {
            'budget': forms.Select(attrs={'class': 'oh-select oh-select-2 w-100'}),
            'allocation': forms.Select(attrs={'class': 'oh-select oh-select-2 w-100'}),
            'description': forms.Textarea(attrs={'class': 'oh-input w-100', 'rows': 3}),
            'amount': forms.NumberInput(attrs={'class': 'oh-input w-100', 'step': '0.01'}),
            'expense_date': forms.DateInput(attrs={'class': 'oh-input w-100', 'type': 'date'}),
            'receipt': forms.FileInput(attrs={'class': 'oh-input w-100'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['budget'].queryset = Budget.objects.filter(status__in=['approved', 'active'])
        self.fields['allocation'].queryset = BudgetAllocation.objects.filter(is_active=True)
        self.fields['allocation'].required = False


class BudgetExpenseApprovalForm(ModelForm):
    """
    Form for Budget Expense Approval
    """
    class Meta:
        model = BudgetExpense
        fields = ['status', 'remarks']
        widgets = {
            'status': forms.Select(attrs={'class': 'oh-select oh-select-2 w-100'}),
            'remarks': forms.Textarea(attrs={'class': 'oh-input w-100', 'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Limit status choices for approval
        self.fields['status'].choices = [
            ('approved', _('Approved')),
            ('rejected', _('Rejected')),
        ]


class BudgetFilterForm(forms.Form):
    """
    Form for filtering budgets
    """
    department = forms.ModelChoiceField(
        queryset=Department.objects.filter(is_active=True),
        required=False,
        empty_label=_('All Departments'),
        widget=forms.Select(attrs={'class': 'oh-select oh-select-2 w-100'})
    )
    category = forms.ModelChoiceField(
        queryset=BudgetCategory.objects.filter(is_active=True),
        required=False,
        empty_label=_('All Categories'),
        widget=forms.Select(attrs={'class': 'oh-select oh-select-2 w-100'})
    )
    status = forms.ChoiceField(
        choices=[('', _('All Status'))] + Budget.BUDGET_STATUS_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'oh-select oh-select-2 w-100'})
    )
    start_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'class': 'oh-input w-100', 'type': 'date'})
    )
    end_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'class': 'oh-input w-100', 'type': 'date'})
    )