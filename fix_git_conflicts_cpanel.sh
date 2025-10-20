#!/bin/bash
# Fix Git conflicts on cPanel production server

echo "=========================================="
echo "Fixing Git Merge Conflicts"
echo "=========================================="
echo ""

cd /home/magmafit/magma7_proj

echo "Current status:"
git status

echo ""
echo "=========================================="
echo "Step 1: Accept all incoming changes (from local)"
echo "=========================================="
echo ""

# Remove the old backup files that are causing conflicts
rm -f cms/migrations/0007_merge_BACKUP.py.bak
rm -f cms/migrations/0008_merge_BACKUP.py.bak
rm -f cms/migrations/0009_merge_BACKUP.py.bak

# Remove the conflicted file
rm -f cms/migrations/0010_alter_mediaasset_options_and_more.py

echo "✓ Removed conflicting backup files"
echo ""

echo "Step 2: Accept incoming changes"
git checkout --theirs .
git add .

echo ""
echo "Step 3: Complete the merge"
git commit -m "Resolve migration conflicts - accept incoming changes"

echo ""
echo "=========================================="
echo "Git conflicts resolved!"
echo "=========================================="
echo ""

echo "Current migration files:"
ls -1 cms/migrations/*.py | grep -E "000[1-9]" || echo "No migration files found"

echo ""
echo "Next steps:"
echo "1. Activate virtual environment:"
echo "   source ~/virtualenv/magma7_proj/3.12/bin/activate"
echo ""
echo "2. Set production settings:"
echo "   export DJANGO_SETTINGS_MODULE=magma7.settings.production"
echo ""
echo "3. Run migrations:"
echo "   python manage.py migrate"
echo ""
echo "4. Fix boolean fields:"
echo "   python manage.py fix_boolean_fields"
echo ""
echo "5. Restart application:"
echo "   touch passenger_wsgi.py"
echo ""
