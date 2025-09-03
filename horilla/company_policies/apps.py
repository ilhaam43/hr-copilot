from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class CompanyPoliciesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'company_policies'
    verbose_name = _('Kebijakan Perusahaan')
    
    def ready(self):
        # Import signals jika diperlukan
        pass