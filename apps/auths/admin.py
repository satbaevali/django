#Django modules
from django.contrib.admin import register,ModelAdmin

#Project modules
from apps.auths.models import CustomUser 


@register(CustomUser)
class CustomUserAdmin(ModelAdmin):
    list_display=(
        "email",
        "full_name",
        "created_at",
        "is_superuser",
        "is_staff",
        "is_active"
    )
    list_display_links = ("email",)
    list_filter = ("email",)
    ordering = ("email",) 
    
