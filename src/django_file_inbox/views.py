import os
import re
import typing
from datetime import datetime
from pathlib import Path
from typing import Any

from django.conf import settings
from django.http import HttpResponse
from django.views.generic import ListView, TemplateView

if typing.TYPE_CHECKING:
    _Base = TemplateView
else:
    _Base = object


BASE_TEMPLATE = getattr(settings, "FILE_INBOX_BASE_TEMPLATE", "base.html")
BASE_TEMPLATE_BLOCK = getattr(settings, "FILE_INBOX_BLOCK", "content")


class BlockTemplatePreprocessorView(_Base):
    template_base_name: str

    def render_to_response(self, context: dict[str, Any], **response_kwargs: Any) -> HttpResponse:
        base_template_dir = Path(__file__).resolve().parent
        template = base_template_dir / "templates" / self.template_base_name
        replacements = {
            "block": r"""\{\%\s+(customblock)\s+(.*)\s+\%\}""",
            "endblock": r"""\{\%\s+(endcustomblock)\s+(.*)\s+\%\}""",
        }

        preprocessed_template = base_template_dir / "templates" / self.get_template_names()[0]
        with Path.open(preprocessed_template, mode="w") as new_template:
            with Path.open(template) as old_template:
                contents = old_template.read()
                for tagname, re_str in replacements.items():
                    contents = re.sub(re_str, f"{{% {tagname} {BASE_TEMPLATE_BLOCK} %}}", contents)

            new_template.write(contents)
            new_template.seek(0)

        return super().render_to_response(context, **response_kwargs)


class Inbox(BlockTemplatePreprocessorView, ListView):
    """
    Displays list of mails in file-based EmailBackend inbox
    """

    template_base_name = "django_file_inbox/inbox_template.html"
    template_name = "django_file_inbox/processed/inbox.html"

    context_object_name = "mail_list"
    paginate_by = getattr(settings, "FILE_INBOX_PAGINATION", 10)

    @staticmethod
    def _table_classes() -> str:
        if hasattr(settings, "FILE_INBOX_TABLE_CLASSES"):
            return settings.FILE_INBOX_TABLE_CLASSES

        if hasattr(settings, "FILE_INBOX_BOOTSTRAP"):
            return "table table-striped table-bordered table-hover"

        return ""

    @staticmethod
    def _table_style() -> str:
        return "table-layout: fixed; width: 100%; border-collapse: collapse;"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        classes = self._table_classes()
        context["file_inbox_table_classes"] = classes
        context["file_inbox_table_style"] = self._table_style() if not classes else ""
        context["file_inbox_base_template"] = BASE_TEMPLATE
        return context

    def get_queryset(self):  # noqa: PLR6301
        path = settings.EMAIL_FILE_PATH
        mail_list = os.listdir(path)
        mail_list.sort(reverse=True)
        mail_list = [{"filename": filename} for filename in mail_list if filename != ".gitkeep"]
        for mail in mail_list:
            subject = mail_from = mail_to = ts = False
            email_contents = (settings.EMAIL_FILE_PATH / mail["filename"]).read_text()
            for line in email_contents:
                if line.startswith("Subject:"):
                    subject = True
                    mail["subject"] = line[8:].strip()
                if line.startswith("From: "):
                    mail_from = True
                    mail["from"] = line[6:].strip()
                if line.startswith("To: "):
                    mail_to = True
                    mail["to"] = line[4:].strip()
                if line.startswith("Date: "):
                    ts = True
                    mail["timestamp"] = line[6:].strip()

                if subject and mail_from and mail_to and ts:
                    break

        return mail_list


class InboxMail(BlockTemplatePreprocessorView, TemplateView):
    """
    Displays specific mail from the file-based EmailBackend inbox
    """

    template_base_name = "django_file_inbox/inbox_email_template.html"
    template_name = "django_file_inbox/processed/inbox_email.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        filename = context["filename"]
        date_time = " ".join(Path(filename).stem.split("-")[:2])

        context["timestamp"] = datetime.strptime(date_time, "%Y%m%d %H%M%S").astimezone()

        filepath = settings.EMAIL_FILE_PATH / filename
        context["email_content"] = filepath.read_text()

        context["subject"] = ""
        for line in context["email_content"].split("\n"):
            if line.startswith("Subject:"):
                context["subject"] = line[8:].strip()
                break

        context["file_inbox_base_template"] = BASE_TEMPLATE
        return context
