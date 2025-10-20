# Admin 500 Error Fix - Deployment Checklist

## Quick Reference for Deploying Admin Fixes

### Pre-Deployment Checklist

- [ ] Read `ADMIN_500_ERROR_FIX.md` for full technical details
- [ ] Have cPanel File Manager access
- [ ] Have cPanel Terminal access
- [ ] Know your project path: `/home/magmafit/magma7_proj`

---

## Deployment Steps

### 1. Upload Files via cPanel File Manager

#### File 1: production.py
- [ ] Navigate to: `/home/magmafit/magma7_proj/magma7/settings/`
- [ ] Upload: `production.py`
- [ ] Confirm file size: ~7 KB
- [ ] Verify timestamp is current

#### File 2: admin.py
- [ ] Navigate to: `/home/magmafit/magma7_proj/cms/`
- [ ] Upload: `admin.py`
- [ ] Confirm file size: ~15 KB
- [ ] Verify timestamp is current

---

### 2. Run Deployment Script

#### Connect to Terminal
- [ ] Open cPanel Terminal
- [ ] Navigate to project:
  ```bash
  cd /home/magmafit/magma7_proj
  ```

#### Run Script
- [ ] Execute:
  ```bash
  bash deploy_admin_fixes.sh
  ```
- [ ] Answer "yes" when prompted
- [ ] Wait for completion (2-3 minutes)

#### Expected Output
- [ ] See "Step 1: Fixing BooleanField values" (should fix 3-4 rows)
- [ ] See "Step 2: Verifying settings update" (shows timezone config)
- [ ] See "Step 3: Testing admin pages" (lists plans and errors)
- [ ] See "Step 4: Restarting application" (✓ restarted)
- [ ] See "✓ Deployment Complete!"

---

### 3. Verify Admin Pages Work

#### Test Memberships Plans
- [ ] Visit: https://www.magma7fitness.com/admin/memberships/plan/
- [ ] Should load without errors
- [ ] Should show list of plans
- [ ] Should see checkboxes for "is_featured" and "is_active"
- [ ] No `KeyError: '0'`

#### Test Error Logs
- [ ] Visit: https://www.magma7fitness.com/admin/cms/errorlog/
- [ ] Should load without errors
- [ ] Should show list of errors sorted by newest first
- [ ] Can filter by severity, resolved status, timestamp
- [ ] No timezone ValueError

---

### 4. Post-Deployment Tasks

#### Set Featured Plan
- [ ] Go to: https://www.magma7fitness.com/admin/memberships/plan/
- [ ] Click on the Quarterly (3-month) plan
- [ ] Check the "Is featured" checkbox
- [ ] Save
- [ ] Uncheck "Is featured" on all other plans
- [ ] Verify only one plan has "Most Popular" badge on frontend

#### Monitor for Errors
- [ ] Visit: https://www.magma7fitness.com/admin/cms/errorlog/
- [ ] Check for any new errors
- [ ] Mark old errors as resolved

---

## Troubleshooting

### If Memberships Plans Still Shows 500 Error

**Check:**
1. Was `production.py` uploaded correctly?
   - Path: `/home/magmafit/magma7_proj/magma7/settings/production.py`
   - Check file timestamp - should be recent

2. Did the SQL updates run?
   - Re-run: `bash deploy_admin_fixes.sh`
   - Check output for "Fixed is_featured" and "Fixed is_active"

3. Did the application restart?
   - Manually restart:
     ```bash
     cd /home/magmafit/magma7_proj
     touch passenger_wsgi.py
     ```

### If Error Logs Still Shows Timezone Error

**Check:**
1. Was `admin.py` uploaded correctly?
   - Path: `/home/magmafit/magma7_proj/cms/admin.py`
   - Check file timestamp - should be recent

2. Is `date_hierarchy` disabled?
   - View file line 355 - should be commented out
   - Should see: `# date_hierarchy = 'timestamp'`

3. Did the application restart?
   - Manually restart:
     ```bash
     cd /home/magmafit/magma7_proj
     touch passenger_wsgi.py
     ```

### If Both Still Don't Work

**Check Settings Module:**
```bash
cd /home/magmafit/magma7_proj
source ~/virtualenv/magma7_proj/3.12/bin/activate
export DJANGO_SETTINGS_MODULE=magma7.settings.production
python manage.py shell
```

Then run:
```python
from django.conf import settings
print(settings.DATABASES['default']['OPTIONS'])
# Should show timezone config
```

**Check Error Logs:**
- cPanel → Errors (last 300 messages)
- Look for new Python exceptions
- Share error message if issue persists

---

## Files Changed Summary

| File | Location | Lines Changed | Purpose |
|------|----------|---------------|---------|
| `production.py` | `magma7/settings/` | 37-42 | Add MySQL timezone config |
| `admin.py` | `cms/` | 354-355 | Disable date_hierarchy, add ordering |

---

## Rollback Instructions

If you need to undo the changes:

### Restore production.py
```python
# Line 37-42 in production.py - Remove timezone config
'OPTIONS': {
    'charset': 'utf8mb4',
},
```

### Restore admin.py
```python
# Line 354-355 in admin.py - Re-enable date_hierarchy
date_hierarchy = 'timestamp'
# Remove: ordering = ('-timestamp',)
```

### Restart
```bash
cd /home/magmafit/magma7_proj
touch passenger_wsgi.py
```

---

## Success Criteria

✓ Deployment is successful when:
- Memberships Plans admin loads without KeyError
- Error Logs admin loads without timezone ValueError
- Both pages display data correctly
- Can create/edit plans and error logs
- Featured plan badge shows correctly on frontend

---

## Timeline

**Estimated Time:** 15-20 minutes

1. Upload files: 5 minutes
2. Run script: 3 minutes
3. Verify pages: 5 minutes
4. Set featured plan: 2 minutes
5. Final testing: 5 minutes

---

## Support Documents

- **Full Guide:** `ADMIN_500_ERROR_FIX.md`
- **Featured Plan Setup:** `SET_FEATURED_PLAN.md`
- **Error Logging Guide:** `ERROR_LOG_GUIDE.md`
- **Deployment Script:** `deploy_admin_fixes.sh`

---

## Contact

If issues persist after following this checklist:
1. Check cPanel error logs
2. Review `ADMIN_500_ERROR_FIX.md` troubleshooting section
3. Provide error messages from cPanel errors or Django admin

---

**Status:** Ready to Deploy ✓

**Last Updated:** 2025-10-20
