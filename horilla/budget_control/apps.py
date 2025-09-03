from django.apps import AppConfig
from django.urls import include, path


class BudgetControlConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "budget_control"
    verbose_name = "Budget Control"

    def ready(self):
        from horilla import horilla_settings
        from horilla.urls import urlpatterns

        # Add budget_control to APPS list
        horilla_settings.APPS.append(self.name)

        # Add URL patterns
        urlpatterns.append(
            path("budget-control/", include("budget_control.urls"))
        )