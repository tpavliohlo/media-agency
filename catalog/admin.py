from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from catalog.models import Newspaper, Redactor, Topic

# Register your models here.
@admin.register(Redactor)
class RedactorAdmin(admin.ModelAdmin):
    list_display =  UserAdmin.list_display + ("years_of_experience",)
    fieldsets = UserAdmin.fieldsets + (
        ("Additional info", {"fields": ("years_of_experience",)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            (
                "Additional info",
                {
                    "fields": (
                        "first_name",
                        "last_name",
                        "years_of_experience",
                    )
                }
            )
        )
    )


@admin.register(Newspaper)
class NewspaperAdmin(admin.ModelAdmin):
    search_fields = ("title",)
    list_after = ("redactors")


admin.site.register(Topic)
