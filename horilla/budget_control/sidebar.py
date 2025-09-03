from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.context_processors import PermWrapper

MENU = _("Budget Control")
IMG_SRC = "images/ui/budget.svg"
ACCESSIBILITY = "budget_control.sidebar.menu_accessibility"

SUBMENUS = [
    {
        "menu": _("Dashboard"),
        "redirect": reverse("budget-dashboard"),
        "accessibility": "budget_control.sidebar.dashboard_accessibility",
    },
    {
        "menu": _("Budgets"),
        "redirect": reverse("budget-list"),
        "accessibility": "budget_control.sidebar.budget_accessibility",
    },
    {
        "menu": _("Expenses"),
        "redirect": reverse("expense-list"),
        "accessibility": "budget_control.sidebar.expense_accessibility",
    },
    {
        "menu": _("Categories"),
        "redirect": reverse("category-list"),
        "accessibility": "budget_control.sidebar.category_accessibility",
    },
]


def menu_accessibility(request, menu, user_perms, *args, **kwargs):
    """
    Check if user has access to budget control menu
    """
    return (
        request.user.is_superuser
        or request.user.has_perm("budget_control.view_budget")
        or request.user.has_perm("budget_control.add_budget")
        or request.user.has_perm("budget_control.view_budgetexpense")
        or request.user.has_perm("budget_control.add_budgetexpense")
    )


def dashboard_accessibility(request, submenu, user_perms, *args, **kwargs):
    """
    Check if user has access to budget dashboard
    """
    return (
        request.user.is_superuser
        or request.user.has_perm("budget_control.view_budget")
        or request.user.has_perm("budget_control.view_budgetexpense")
    )


def budget_accessibility(request, submenu, user_perms, *args, **kwargs):
    """
    Check if user has access to budget management
    """
    return (
        request.user.is_superuser
        or request.user.has_perm("budget_control.view_budget")
        or request.user.has_perm("budget_control.add_budget")
        or request.user.has_perm("budget_control.change_budget")
    )





def expense_accessibility(request, submenu, user_perms, *args, **kwargs):
    """
    Check if user has access to expense management
    """
    return (
        request.user.is_superuser
        or request.user.has_perm("budget_control.view_budgetexpense")
        or request.user.has_perm("budget_control.add_budgetexpense")
        or request.user.has_perm("budget_control.change_budgetexpense")
    )


def category_accessibility(request, submenu, user_perms, *args, **kwargs):
    """
    Check if user has access to category management
    """
    return (
        request.user.is_superuser
        or request.user.has_perm("budget_control.view_budgetcategory")
        or request.user.has_perm("budget_control.add_budgetcategory")
        or request.user.has_perm("budget_control.change_budgetcategory")
    )