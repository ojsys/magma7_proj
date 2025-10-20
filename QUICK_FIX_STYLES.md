# Quick Fix for Missing Styles

## Your Django app is working but needs static files! 🎨

---

## Option 1: Automated Script (Easiest)

Upload `setup_static_files.sh` to your server and run:

```bash
cd /home/magmafit/magma7_proj
chmod +x setup_static_files.sh
./setup_static_files.sh
```

This will do everything automatically!

---

## Option 2: Manual Commands (3 Steps)

### Step 1: Collect Static Files
```bash
cd /home/magmafit/magma7_proj
source ~/virtualenv/magma7_proj/3.12/bin/activate
export DJANGO_SETTINGS_MODULE=magma7.settings.production
python manage.py collectstatic --noinput
```

### Step 2: Link to public_html
```bash
ln -s /home/magmafit/magma7_proj/staticfiles /home/magmafit/public_html/static
mkdir -p /home/magmafit/magma7_proj/media
ln -s /home/magmafit/magma7_proj/media /home/magmafit/public_html/media
```

**If symlinks don't work:**
```bash
cp -r /home/magmafit/magma7_proj/staticfiles /home/magmafit/public_html/static
cp -r /home/magmafit/magma7_proj/media /home/magmafit/public_html/media
```

### Step 3: Configure in cPanel
1. Go to **cPanel → Setup Python App**
2. Click **Edit** on your app
3. Scroll to **"Static files"**
4. Add mapping:
   - **URL:** `/static/`
   - **Path:** `/home/magmafit/public_html/static`
5. **Save** and **Restart** the app

---

## Test It!

Visit: `https://www.magma7fitness.com/static/admin/css/base.css`

- If you see CSS code → Static files are working! ✅
- If you get 404 → Follow troubleshooting in `FIX_STATIC_FILES.md`

Then refresh your main site - styles should now load!

---

## Still Not Working?

**Quick checks:**
```bash
# Check files exist
ls -la /home/magmafit/public_html/static/

# Check permissions
chmod 755 /home/magmafit/public_html/static
```

**Check browser console (F12):**
- Look for 404 errors
- Note the URLs it's trying to load

**See full guide:** `FIX_STATIC_FILES.md`

---

## Summary

Your Django app is **100% working** - just needs CSS/JS files to be served from the right location. This is a common final step in Django deployment!
