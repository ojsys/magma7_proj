#!/bin/bash
# Export production data to JSON file
# RUN THIS ON CPANEL SERVER

echo "=========================================="
echo "Export Production Data to JSON"
echo "=========================================="
echo ""

cd /home/magmafit/magma7_proj
source ~/virtualenv/magma7_proj/3.12/bin/activate
export DJANGO_SETTINGS_MODULE=magma7.settings.production

echo "Exporting data from production database..."
echo ""

python manage.py dumpdata \
  cms.sitesettings \
  cms.heroslide \
  cms.program \
  cms.service \
  cms.partner \
  cms.testimonial \
  cms.mediaasset \
  cms.homegalleryimage \
  cms.aboutpage \
  cms.corevalue \
  cms.whychooseusitem \
  cms.aboutgalleryimage \
  cms.aboutstatistic \
  cms.facility \
  cms.teammember \
  cms.facilitiespage \
  cms.teampage \
  cms.richpage \
  memberships.plan \
  memberships.planfeature \
  --indent 2 \
  --output production_data.json

echo ""
echo "=========================================="
echo "✓ Export Complete!"
echo "=========================================="
echo ""
echo "Created: production_data.json"
echo "Location: /home/magmafit/magma7_proj/production_data.json"
echo ""
echo "Next steps:"
echo "  1. Download production_data.json from cPanel File Manager"
echo "  2. Place it in your local project root"
echo "  3. Run: ./import_from_production.sh"
echo ""

# Show file size
ls -lh production_data.json

echo ""
