from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from employee.models import Employee, Department
from base.models import HorillaModel


class BudgetCategory(HorillaModel):
    """
    Budget Category model for organizing budget items
    """
    name = models.CharField(max_length=100, verbose_name=_("Category Name"))
    description = models.TextField(blank=True, null=True, verbose_name=_("Description"))
    is_active = models.BooleanField(default=True, verbose_name=_("Is Active"))
    
    class Meta:
        verbose_name = _("Budget Category")
        verbose_name_plural = _("Budget Categories")
        
    def __str__(self):
        return self.name


class Budget(HorillaModel):
    """
    Main Budget model
    """
    BUDGET_STATUS_CHOICES = [
        ('draft', _('Draft')),
        ('approved', _('Approved')),
        ('active', _('Active')),
        ('completed', _('Completed')),
        ('cancelled', _('Cancelled')),
    ]
    
    name = models.CharField(max_length=200, verbose_name=_("Budget Name"))
    description = models.TextField(blank=True, null=True, verbose_name=_("Description"))
    department = models.ForeignKey(
        Department, 
        on_delete=models.CASCADE, 
        verbose_name=_("Department"),
        related_name="budgets"
    )
    category = models.ForeignKey(
        BudgetCategory, 
        on_delete=models.CASCADE, 
        verbose_name=_("Category"),
        related_name="budgets"
    )
    total_amount = models.DecimalField(
        max_digits=15, 
        decimal_places=2, 
        verbose_name=_("Total Amount")
    )
    allocated_amount = models.DecimalField(
        max_digits=15, 
        decimal_places=2, 
        default=0,
        verbose_name=_("Allocated Amount")
    )
    spent_amount = models.DecimalField(
        max_digits=15, 
        decimal_places=2, 
        default=0,
        verbose_name=_("Spent Amount")
    )
    start_date = models.DateField(verbose_name=_("Start Date"))
    end_date = models.DateField(verbose_name=_("End Date"))
    status = models.CharField(
        max_length=20, 
        choices=BUDGET_STATUS_CHOICES, 
        default='draft',
        verbose_name=_("Status")
    )
    created_by = models.ForeignKey(
        Employee, 
        on_delete=models.CASCADE, 
        verbose_name=_("Created By"),
        related_name="created_budgets"
    )
    approved_by = models.ForeignKey(
        Employee, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        verbose_name=_("Approved By"),
        related_name="approved_budgets"
    )
    approved_date = models.DateTimeField(
        null=True, 
        blank=True, 
        verbose_name=_("Approved Date")
    )
    
    class Meta:
        verbose_name = _("Budget")
        verbose_name_plural = _("Budgets")
        ordering = ['-created_at']
        
    def __str__(self):
        return f"{self.name} - {self.department.department}"
    
    @property
    def remaining_amount(self):
        return self.total_amount - self.spent_amount
    
    @property
    def utilization_percentage(self):
        if self.total_amount > 0:
            return (self.spent_amount / self.total_amount) * 100
        return 0


class BudgetAllocation(HorillaModel):
    """
    Budget Allocation model for tracking budget allocations
    """
    budget = models.ForeignKey(
        Budget, 
        on_delete=models.CASCADE, 
        verbose_name=_("Budget"),
        related_name="allocations"
    )
    allocated_to = models.ForeignKey(
        Employee, 
        on_delete=models.CASCADE, 
        verbose_name=_("Allocated To"),
        related_name="budget_allocations"
    )
    amount = models.DecimalField(
        max_digits=15, 
        decimal_places=2, 
        verbose_name=_("Amount")
    )
    purpose = models.CharField(max_length=200, verbose_name=_("Purpose"))
    allocation_date = models.DateField(verbose_name=_("Allocation Date"))
    is_active = models.BooleanField(default=True, verbose_name=_("Is Active"))
    
    class Meta:
        verbose_name = _("Budget Allocation")
        verbose_name_plural = _("Budget Allocations")
        ordering = ['-allocation_date']
        
    def __str__(self):
        return f"{self.budget.name} - {self.allocated_to.employee_first_name} - {self.amount}"


class BudgetExpense(HorillaModel):
    """
    Budget Expense model for tracking expenses against budget
    """
    EXPENSE_STATUS_CHOICES = [
        ('pending', _('Pending')),
        ('approved', _('Approved')),
        ('rejected', _('Rejected')),
        ('paid', _('Paid')),
    ]
    
    budget = models.ForeignKey(
        Budget, 
        on_delete=models.CASCADE, 
        verbose_name=_("Budget"),
        related_name="expenses"
    )
    allocation = models.ForeignKey(
        BudgetAllocation, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True,
        verbose_name=_("Allocation"),
        related_name="expenses"
    )
    employee = models.ForeignKey(
        Employee, 
        on_delete=models.CASCADE, 
        verbose_name=_("Employee"),
        related_name="budget_expenses"
    )
    description = models.TextField(verbose_name=_("Description"))
    amount = models.DecimalField(
        max_digits=15, 
        decimal_places=2, 
        verbose_name=_("Amount")
    )
    expense_date = models.DateField(verbose_name=_("Expense Date"))
    receipt = models.FileField(
        upload_to='budget_receipts/', 
        null=True, 
        blank=True,
        verbose_name=_("Receipt")
    )
    status = models.CharField(
        max_length=20, 
        choices=EXPENSE_STATUS_CHOICES, 
        default='pending',
        verbose_name=_("Status")
    )
    approved_by = models.ForeignKey(
        Employee, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        verbose_name=_("Approved By"),
        related_name="approved_expenses"
    )
    approved_date = models.DateTimeField(
        null=True, 
        blank=True, 
        verbose_name=_("Approved Date")
    )
    remarks = models.TextField(
        blank=True, 
        null=True, 
        verbose_name=_("Remarks")
    )
    
    class Meta:
        verbose_name = _("Budget Expense")
        verbose_name_plural = _("Budget Expenses")
        ordering = ['-expense_date']
        
    def __str__(self):
        return f"{self.budget.name} - {self.employee.employee_first_name} - {self.amount}"