# Fixing "Bad Request (400)" Error

## Good News! 🎉
Your Django app is now running! The 400 error means Django is working but rejecting the request because the hostname isn't in `ALLOWED_HOSTS`.

---

## Quick Fix

### Step 1: Update .env File on Server

SSH into your server and edit the `.env` file:

```bash
ssh magmafit@yourserver
cd /home/magmafit/magma7_proj
nano .env
```

### Step 2: Update DJANGO_ALLOWED_HOSTS

Find this line:
```env
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1,magma7fitness.com,www.magma7fitness.com
```

**Add all possible hostnames** that users might use to access your site:

```env
DJANGO_ALLOWED_HOSTS=magma7fitness.com,www.magma7fitness.com,localhost,127.0.0.1,s4834.sureserver.com
```

**Important:**
- No spaces between hostnames
- Include both `magma7fitness.com` and `www.magma7fitness.com`
- Include your server's hostname (check what shows in your browser's address bar)
- If you have an IP address, add it too

### Step 3: Check What Hostname You're Using

Look at your browser's address bar. Are you accessing via:
- `http://magma7fitness.com` ✅
- `http://www.magma7fitness.com` ✅
- `http://s4834.sureserver.com` ❓ (Add this if this is what you see)
- `http://123.45.67.89` ❓ (Add IP if you're using it)

### Step 4: Optional - Enable DEBUG Temporarily

To see the exact error, you can temporarily enable DEBUG in `.env`:

```env
DEBUG=True
```

**IMPORTANT:** Set this back to `False` before going live!

With DEBUG=True, Django will show you exactly which host is causing the issue.

### Step 5: Save and Restart

Save the `.env` file (Ctrl+X, Y, Enter in nano) and restart:

```bash
touch /home/magmafit/magma7_proj/passenger_wsgi.py
```

Or restart via cPanel → Setup Python App → Restart

### Step 6: Test Again

Visit your site. You should now see the Django application!

---

## Common Scenarios

### Scenario 1: Accessing via cPanel Preview URL

If you're using a cPanel preview URL like `s4834.sureserver.com`:

```env
DJANGO_ALLOWED_HOSTS=s4834.sureserver.com,magma7fitness.com,www.magma7fitness.com
```

### Scenario 2: IP Address Access

If accessing via IP like `123.45.67.89`:

```env
DJANGO_ALLOWED_HOSTS=123.45.67.89,magma7fitness.com,www.magma7fitness.com
```

### Scenario 3: Allow Everything (TEMPORARY TESTING ONLY)

**⚠️ Only for testing! Not secure for production!**

```env
DJANGO_ALLOWED_HOSTS=*
```

This allows all hostnames. Once you figure out which hostname works, replace `*` with the actual hostname.

---

## Troubleshooting

### Still Getting 400 Error?

1. **Check the logs** to see which host is being rejected:
   ```bash
   tail -f /home/magmafit/magma7_proj/logs/django_errors.log
   ```

2. **Enable DEBUG temporarily** to see the exact error:
   ```env
   DEBUG=True
   ```

   The error page will show: "Invalid HTTP_HOST header: 'xxxxx'. You may need to add 'xxxxx' to ALLOWED_HOSTS."

3. **Check your .env is being loaded:**
   ```bash
   cd /home/magmafit/magma7_proj
   python manage.py shell
   ```

   Then in Python shell:
   ```python
   from django.conf import settings
   print(settings.ALLOWED_HOSTS)
   ```

   This should show your list of allowed hosts.

### .env Not Being Loaded?

Check the production settings file loads the .env:

```bash
cat /home/magmafit/magma7_proj/magma7/settings/base.py | grep -A5 "load_dotenv"
```

### Environment Variables Not Working?

You can also set ALLOWED_HOSTS directly in cPanel:

1. Go to cPanel → Setup Python App
2. Scroll to "Environment variables"
3. Add:
   ```
   Name: DJANGO_ALLOWED_HOSTS
   Value: magma7fitness.com,www.magma7fitness.com
   ```
4. Click "Save"
5. Restart app

---

## Production Checklist

Once it's working, update your `.env` for production:

```env
# Set to False in production
DEBUG=False

# Add only your actual domains
DJANGO_ALLOWED_HOSTS=magma7fitness.com,www.magma7fitness.com

# Generate a real secret key
DJANGO_SECRET_KEY=your-actual-generated-secret-key-here

# Update database credentials
DB_NAME=magmafit_db
DB_USER=magmafit_dbuser
DB_PASSWORD=your-actual-db-password
```

Generate a new SECRET_KEY:
```bash
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

---

## Success Indicators

✅ You'll know it's working when:
- No more 400 error
- You see your Django homepage
- `/admin` is accessible
- Logs show no errors

---

## Next Steps After Fixing 400

1. ✅ Run migrations if not done yet
2. ✅ Create superuser account
3. ✅ Collect static files
4. ✅ Test all functionality
5. ✅ Set DEBUG=False
6. ✅ Enable SSL/HTTPS

Need help with any of these? Let me know!
