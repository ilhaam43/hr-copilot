"""AI Knowledge sidebar configuration"""

from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

MENU = _("AI Knowledge")
ACCESSIBILITY = "ai_knowledge.sidebar.ai_knowledge_accessibility"
IMG_SRC = "images/ui/brain.svg"

SUBMENUS = [
    {
        "menu": _("Dashboard"),
        "redirect": reverse_lazy("ai_knowledge:dashboard"),
        "accessibility": "ai_knowledge.sidebar.dashboard_accessibility",
    },
    {
        "menu": _("Documents"),
        "redirect": reverse_lazy("ai_knowledge:document_list"),
        "accessibility": "ai_knowledge.sidebar.document_accessibility",
    },
    {
        "menu": _("Knowledge Base"),
        "redirect": reverse_lazy("ai_knowledge:knowledge_base_list"),
        "accessibility": "ai_knowledge.sidebar.knowledge_base_accessibility",
    },
    {
        "menu": _("Training Data"),
        "redirect": reverse_lazy("ai_knowledge:training_data_list"),
        "accessibility": "ai_knowledge.sidebar.training_data_accessibility",
    },
    {
        "menu": _("AI Intents"),
        "redirect": reverse_lazy("ai_knowledge:ai_intent_list"),
        "accessibility": "ai_knowledge.sidebar.ai_intent_accessibility",
    },
    {
        "menu": _("Categories"),
        "redirect": reverse_lazy("ai_knowledge:category_list"),
        "accessibility": "ai_knowledge.sidebar.category_accessibility",
    },
    {
        "menu": _("Analytics"),
        "redirect": reverse_lazy("ai_knowledge:analytics"),
        "accessibility": "ai_knowledge.sidebar.analytics_accessibility",
    },
]


def ai_knowledge_accessibility(request, submenu, user_perms, *args, **kwargs):
    """Check if user has access to AI Knowledge module"""
    return request.user.has_perm("ai_knowledge.view_aidocument")


def dashboard_accessibility(request, submenu, user_perms, *args, **kwargs):
    """Check if user has access to dashboard"""
    return request.user.has_perm("ai_knowledge.view_aidocument")


def document_accessibility(request, submenu, user_perms, *args, **kwargs):
    """Check if user has access to documents"""
    return request.user.has_perm("ai_knowledge.view_aidocument")


def knowledge_base_accessibility(request, submenu, user_perms, *args, **kwargs):
    """Check if user has access to knowledge base"""
    return request.user.has_perm("ai_knowledge.view_knowledgebaseentry")


def training_data_accessibility(request, submenu, user_perms, *args, **kwargs):
    """Check if user has access to training data"""
    return request.user.has_perm("ai_knowledge.view_trainingdata")


def ai_intent_accessibility(request, submenu, user_perms, *args, **kwargs):
    """Check if user has access to AI intents"""
    return request.user.has_perm("ai_knowledge.view_aiintent")


def category_accessibility(request, submenu, user_perms, *args, **kwargs):
    """Check if user has access to categories"""
    return request.user.has_perm("ai_knowledge.view_documentcategory")


def analytics_accessibility(request, submenu, user_perms, *args, **kwargs):
    """Check if user has access to analytics"""
    return request.user.has_perm("ai_knowledge.view_aidocument")