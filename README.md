# django-file-inbox

## Purpose
This package adds 2 view endpoints to a Django project: 
    - A ListView for Inbox items
    - A TemplateView for individual emails

It is intended for use with the `django.core.mail.backends.filebased.EmailBackend` email backend, primarily for local developement 
purposes to make it easier to view emails your project sends.

## Installation & configuration
1. Install the package into your environment: `pip install django-file-inbox`
2. Add `django_file_inbox` to your `INSTALLED_APPS` setting:
```
INSTALLED_APPS = [
    ...
]
if DEBUG: 
    INSTALLED_APPS += ['django_file_inbox']
```
3. Set the email backend to `django.core.mail.backends.filebased.EmailBackend`:
```
if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
    EMAIL_FILE_PATH = BASE_DIR / "email"
```
4. Configure any axtra settings for the package. See the `settings.py` section below for options. 
5. Add the inbox links to a suitable `urls.py`: 
```
urlpatterns = [...]
if DEBUG:
    urlpatterns += [
        path('__inbox/', include('django_file_inbox.urls')),
    ]
```
6. You can then include the inbox links in your project's base template, navbar, or wherever you like. 
```
<a href="{% url 'django_file_inbox:file_inbox' %}">Inbox</a>
```

### settings.py
The following values may be added to the `settings.py` file:

| Name                       | Description                                                               |   Default   |
| -------------------------- | ------------------------------------------------------------------------- | :---------: |
| `FILE_INBOX_BOOTSTRAP`     | Whether the project is using Bootstrap                                    | `False`     |
| `FILE_INBOX_TABLE_CLASSES` | CSS classes to apply to the table. This supercedes `FILE_INBOX_BOOTSTRAP` | `""`        |
| `FILE_INBOX_PAGINATION`    | Numver of records to show per page for the Inbox ListView                 | `10`        |
| `FILE_INBOX_BASE_TEMPLATE` | Base template name to use for the inbox list and detail views             | `base.html` |
| `FILE_INBOX_BLOCK_NAME`    | Name of the tempalte block to use for the inbox list and detail views     | `content`   |

Setting `FILE_INBOX_BOOTSTRAP` to `True` will apply the bootstrap classes `table table-striped table-bordered table-hover` to the table.
Setting `FILE_INBOX_TABLE_CLASSES` will will apply whatever classes you set in that value.

`FILE_INBOX_BASE_TEMPLATE` and `FILE_INBOX_BLOCK_NAME` are set to allow the inbox and email detail views to display in the main content block of your base template. 

Set `FILE_INBOX_BASE_TEMPLATE` if your base template is called anything other than `base.html`, or is not in the root template directory. 
Set `FILE_INBOX_BLOCK_NAME` if your base template uses a block name other than `content` for the main content block.

For example, if your base template looks as follows: 
*mybase.html*
```
<html>
...
<body>
    <div class="container">
        {% block main_block %}
        {% endblock main_block %}
    </div>
</body>
</html>
```
Then set:
```
FILE_INBOX_BASE_TEMPLATE = "mybase.html"
FILE_INBOX_BLOCK_NAME = "main_block"
```
