# django-file-inbox

## Purpose

## Installation & configuration

### settings.py
The following values may be added to the `settings.py` file:

| Name | Description | Default |
| ---- | ----------- | ------- |
| `FILE_INBOX_BOOTSTRAP` | Whether the project is using Bootstrap  | `False` |
| `FILE_INBOX_TABLE_CLASSES` | CSS classes to apply to the table. This supercedes `FILE_INBOX_BOOTSTRAP` | Empty string  |
| `FILE_INBOX_PAGINATION` | Numver of records to show per page for the Inbox ListView | 10 |
| `FILE_INBOX_BASE_TEMPLATE` | Base template name to use for the inbox list and detail views | `base.html` |
| `FILE_INBOX_BLOCK_NAME` | Name of the tempalte block to use for the inbox list and detail views | `content` |


