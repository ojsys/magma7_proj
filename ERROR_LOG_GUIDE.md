# Error Log System Guide

## Overview

The Error Log system automatically captures all application errors and displays them in the Django admin for easy monitoring and debugging.

---

## Features

### Automatic Error Capture
- **500 Errors**: All unhandled exceptions automatically logged
- **404 Errors**: Page not found errors tracked
- **Full Details**: Request info, user, IP, traceback
- **Severity Levels**: DEBUG, INFO, WARNING, ERROR, CRITICAL

### Admin Interface
- **Color-coded severity badges**
- **Search and filter** by severity, status, date, exception type
- **Full traceback viewing** with syntax highlighting
- **Mark errors as resolved** with timestamp and user tracking
- **Bulk actions** for managing multiple errors
- **Automatic cleanup** of old resolved errors

### Security
- **Superuser**: See all errors system-wide
- **Regular staff**: See only their own errors
- **Anonymous errors**: Tracked as "Anonymous" user

---

## Accessing Error Logs

### In Django Admin

1. **Login** to admin: `http://localhost:8000/admin/` or `https://www.magma7fitness.com/admin/`
2. Look for **"Error Logs"** in the CMS section
3. Click to view all errors

### Error List View

The main error log page shows:

| Column | Description |
|--------|-------------|
| **Severity** | Color-coded badge (Critical=Dark Red, Error=Red, Warning=Yellow, Info=Blue, Debug=Gray) |
| **Timestamp** | When the error occurred |
| **Message** | Short error message (first 100 chars) |
| **Path** | URL where error happened |
| **User** | Username or "Anonymous" |
| **Status** | ✓ Resolved or ✗ Unresolved |
| **Actions** | Quick action buttons |

---

## Error Severity Levels

### 🔴 CRITICAL
- System failures
- KeyboardInterrupt, SystemExit
- Requires immediate attention

### 🔴 ERROR
- Application errors
- ValueError, TypeError, AttributeError
- Breaks functionality

### 🟡 WARNING
- Non-critical issues
- 404 errors
- Permission errors
- Degrades experience

### 🔵 INFO
- Informational messages
- Audit trail events

### ⚫ DEBUG
- Development/debugging info
- Detailed diagnostic data

---

## Viewing Error Details

### Click on any error to see:

**Error Information:**
- Timestamp
- Severity level
- Full error message
- Exception type (e.g., ValueError, DoesNotExist)

**Request Details:**
- URL path
- HTTP method (GET, POST, etc.)
- Username
- IP address
- Browser user agent

**Technical Details** (collapsible):
- Full Python traceback
- Syntax-highlighted for readability
- Shows exact line where error occurred

**Resolution:**
- Resolved status (Yes/No)
- Resolved timestamp
- Who resolved it
- Admin notes

---

## Managing Errors

### Mark as Resolved

**Single Error:**
1. Click on error
2. Check "Resolved" checkbox
3. Add notes (optional)
4. Click "Save"

**Multiple Errors:**
1. Select errors with checkboxes
2. Choose "Mark selected errors as resolved" from Actions dropdown
3. Click "Go"

### Mark as Unresolved

If you need to reopen an error:
1. Select resolved errors
2. Choose "Mark selected errors as unresolved"
3. Click "Go"

### Delete Old Errors

Clean up resolved errors older than 30 days:
1. Go to Error Logs list
2. Select any error (doesn't matter which)
3. Choose "Delete resolved errors older than 30 days"
4. Click "Go"
5. Confirmation message shows how many deleted

---

## Filtering and Searching

### Filters (Right Sidebar)

- **By Severity**: DEBUG, INFO, WARNING, ERROR, CRITICAL
- **By Status**: Resolved or Unresolved
- **By Date**: Today, Past 7 days, This month, etc.
- **By Exception Type**: ValueError, DoesNotExist, etc.

### Search

Search in:
- Error messages
- URL paths
- Usernames
- Exception types
- Tracebacks

### Date Hierarchy

Navigate errors by date:
- Click year → month → day
- Quickly jump to errors from specific dates

---

## Common Error Scenarios

### 1. Page Not Found (404)

**Logged as:** WARNING
**Example:** `Page not found: /old-page/`

**What to do:**
- Check if URL should exist
- Add redirect in code if needed
- Mark resolved if intentional 404

### 2. Database Errors

**Logged as:** ERROR
**Example:** `DoesNotExist: Membership matching query does not exist`

**What to do:**
- Check database migrations
- Verify data exists
- Add error handling in code

### 3. Template Errors

**Logged as:** ERROR
**Example:** `TemplateDoesNotExist: memberships/plan.html`

**What to do:**
- Check template path
- Verify template file exists
- Fix typos in template name

### 4. Permission Errors

**Logged as:** WARNING
**Example:** `PermissionDenied: User does not have permission`

**What to do:**
- Check user permissions
- Update permission requirements
- Add proper authorization

### 5. Form Validation Errors

**Logged as:** ERROR
**Example:** `ValidationError: This field is required`

**What to do:**
- Improve form validation
- Add user-friendly error messages
- Fix frontend validation

---

## Best Practices

### Regular Monitoring

1. **Check daily** for new errors
2. **Prioritize** CRITICAL and ERROR severity
3. **Investigate** repeated errors
4. **Mark resolved** once fixed

### Error Triage

**High Priority:**
- CRITICAL errors
- Errors affecting multiple users
- Payment/transaction errors
- Security-related errors

**Medium Priority:**
- ERROR severity
- Feature-breaking issues
- Single-user errors

**Low Priority:**
- WARNING severity
- 404 errors from bots
- INFO/DEBUG messages

### Cleanup Schedule

- **Weekly**: Review and resolve errors
- **Monthly**: Delete old resolved errors
- **Quarterly**: Analyze error trends

### Adding Notes

When resolving errors, add notes about:
- What caused the error
- How it was fixed
- Steps to prevent recurrence
- Related code changes

---

## Technical Details

### How It Works

**1. Middleware Capture:**
```python
cms.middleware.ErrorLoggingMiddleware  # Captures 500 errors
cms.middleware.Custom404Middleware     # Captures 404 errors
```

**2. Database Storage:**
- Errors stored in `cms_errorlog` table
- Indexed for fast searching
- Includes full traceback

**3. Admin Display:**
- Custom admin interface
- Color-coded severity
- Bulk actions
- Search and filters

### Files

**Model:** `/cms/models.py` - ErrorLog class
**Admin:** `/cms/admin.py` - ErrorLogAdmin class
**Middleware:** `/cms/middleware.py` - Error capture logic
**Migration:** `/cms/migrations/0004_errorlog.py`

### Database Fields

```python
- timestamp: When error occurred
- severity: DEBUG/INFO/WARNING/ERROR/CRITICAL
- message: Error message text
- path: URL path
- method: HTTP method
- user: Username
- ip_address: Client IP
- user_agent: Browser info
- exception_type: Python exception class
- traceback: Full Python traceback
- resolved: Boolean flag
- resolved_at: When resolved
- resolved_by: Who resolved it
- notes: Admin notes
```

---

## Troubleshooting

### Errors Not Being Logged

**Check middleware is enabled:**
```python
# In settings/base.py
MIDDLEWARE = [
    # ...
    'cms.middleware.ErrorLoggingMiddleware',
    'cms.middleware.Custom404Middleware',
]
```

**Run migration:**
```bash
python manage.py migrate cms
```

**Check database:**
```bash
python manage.py shell
>>> from cms.models import ErrorLog
>>> ErrorLog.objects.count()
```

### Can't See Error Logs in Admin

**Check you're superuser:**
- Regular staff see only their own errors
- Superusers see all errors

**Check migration ran:**
```bash
python manage.py showmigrations cms
# Should show [X] 0004_errorlog
```

### Too Many 404 Errors

Bot traffic and crawlers cause many 404s. To filter:
1. Use the severity filter → Select WARNING
2. Use search → Enter common bot paths
3. Bulk mark as resolved

Or ignore 404s from:
- `/wp-admin/` (WordPress probes)
- `/phpmyadmin/` (Security scans)
- `.env` files (Credential harvesting)

---

## Integration with Logging

### Python Logging

The error log system works alongside Python logging:

```python
import logging
logger = logging.getLogger(__name__)

# Still use Python logging for development
logger.error("Something went wrong")
logger.warning("Careful here")
```

**Database logging** is for production monitoring.
**Python logging** is for development debugging.

### Log Files

Error logs are also written to files:
- `/logs/django_errors.log` (if configured)
- Console output in development

Database logs provide:
- Easy admin access
- Rich metadata (user, IP, path)
- Resolution tracking
- Historical analysis

---

## Production Deployment

### Update Production Server

Upload files:
```bash
scp cms/models.py cms/admin.py cms/middleware.py magmafit@server:/home/magmafit/magma7_proj/cms/
scp cms/migrations/0004_errorlog.py magmafit@server:/home/magmafit/magma7_proj/cms/migrations/
scp magma7/settings/base.py magmafit@server:/home/magmafit/magma7_proj/magma7/settings/
```

Run migration:
```bash
ssh magmafit@server
cd /home/magmafit/magma7_proj
source ~/virtualenv/magma7_proj/3.12/bin/activate
python manage.py migrate cms
touch passenger_wsgi.py
```

---

## Summary

### What You Get

✅ **Automatic error capture** - No code changes needed
✅ **Rich error details** - User, IP, path, traceback
✅ **Easy admin interface** - View and manage errors
✅ **Search and filter** - Find specific errors fast
✅ **Resolution tracking** - Mark errors as fixed
✅ **Bulk actions** - Manage multiple errors
✅ **Security** - Staff see only their errors
✅ **Performance** - Indexed for fast queries

### Quick Access

**View Errors:**
Admin → CMS → Error Logs

**Mark Resolved:**
Select errors → Actions → Mark as resolved

**Clean Up:**
Actions → Delete resolved errors older than 30 days

---

## Need Help?

**Check error details:**
- Click error to see full traceback
- Review request details (user, IP, path)
- Check timestamp to correlate with user reports

**Common fixes:**
- Run migrations: `python manage.py migrate`
- Check file permissions
- Verify environment variables
- Review recent code changes

**Still stuck?**
- Copy full traceback
- Note URL path and timestamp
- Check if error repeats
- Review user actions that triggered it

Happy debugging! 🐛
