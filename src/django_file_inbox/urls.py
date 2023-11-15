from django.urls import path

from django_file_inbox.views import Inbox, InboxMail

app_name = "django_file_inbox"

urlpatterns = [
    path("<str:filename>", InboxMail.as_view(), name="file_inbox_mail"),
    path("", Inbox.as_view(), name="file_inbox"),
]
