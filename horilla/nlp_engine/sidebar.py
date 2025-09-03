"""nlp_engine/sidebar.py

To set Horilla sidebar for NLP Engine
"""

from django.urls import reverse
from django.utils.translation import gettext_lazy as trans

MENU = trans("NLP Engine")
IMG_SRC = "images/ui/chatbot.svg"

SUBMENUS = [
    {
        "menu": trans("Dashboard"),
        "redirect": reverse("nlp-dashboard"),
    },
    {
        "menu": trans("Text Analysis"),
        "redirect": reverse("analyze-text"),
    },
    {
        "menu": trans("Analysis Results"),
        "redirect": reverse("analysis-list"),
    },
    {
        "menu": trans("AI Chatbot"),
        "redirect": reverse("chatbot-view"),
    },
]