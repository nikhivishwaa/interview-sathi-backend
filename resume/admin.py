from django.contrib import admin
from django.utils.html import format_html
from django.utils.text import Truncator
from resume.models import Resume


@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ( "id", "user_display", "name", "status", "is_valid_resume",
                     "matches_user", "uploaded_at", "short_reject_reason")
    list_filter = ( "status", "is_valid_resume", "matches_user", "uploaded_at")
    search_fields = ( "name", "user__username", "user__email", "user__first_name", "user__last_name")
    readonly_fields = ( "uploaded_at", "parsed_text", "parsed_json_pretty", "lambda_raw_pretty")
    date_hierarchy = "uploaded_at"
    ordering = ("-uploaded_at",)

    fieldsets = (
        ("Owner", {
            "fields": ("user",),
        }),
        ("File", {
            "fields": ("file", "name", "uploaded_at"),
        }),
        ("Status & Flags", {
            "fields": (
                "status",
                "reject_reason",
                "is_valid_resume",
                "matches_user",
            ),
        }),
        ("Parsed Data", {
            "classes": ("collapse",),
            "fields": (
                "parsed_text",
                "parsed_json_pretty",
            ),
        }),
        ("Raw Lambda Response", {
            "classes": ("collapse",),
            "fields": ("lambda_raw_pretty",),
        }),
    )
    def user_display(self, obj: Resume):
        """Compact user display for list page."""
        if not obj.user:
            return "-"
        return f"{obj.user.get_full_name() or obj.user.username} ({obj.user.email})"

    user_display.short_description = "User"

    def short_reject_reason(self, obj: Resume):
        if not obj.reject_reason:
            return ""
        return Truncator(obj.reject_reason).chars(60)

    short_reject_reason.short_description = "Reject reason"

    def parsed_json_pretty(self, obj: Resume):
        if not obj.parsed_json:
            return "-"
        from pprint import pformat

        return format_html(
            "<pre style='white-space: pre-wrap; font-size: 12px;'>{}</pre>",
            pformat(obj.parsed_json),
        )

    parsed_json_pretty.short_description = "Parsed JSON"

    def lambda_raw_pretty(self, obj: Resume):
        if not obj.lambda_raw:
            return "-"
        from pprint import pformat

        return format_html(
            "<pre style='white-space: pre-wrap; font-size: 12px;'>{}</pre>",
            pformat(obj.lambda_raw),
        )

    lambda_raw_pretty.short_description = "Lambda Raw"
