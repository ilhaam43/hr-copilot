from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AiKnowledgeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ai_knowledge'
    verbose_name = _('AI Knowledge Management')
