from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Avg
from django.shortcuts import redirect, render
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from .models import Testimonial, MediaAsset, HomeGalleryImage, ErrorLog


def testimonials(request):
    qs = Testimonial.objects.filter(is_approved=True)
    avg = qs.aggregate(avg=Avg('rating'))['avg'] or 0
    return render(request, 'cms/testimonials.html', {"testimonials": qs, "avg_rating": round(avg, 1)})


@login_required
def submit_testimonial(request):
    if request.method == 'POST':
        name = request.POST.get('name') or request.user.get_full_name() or request.user.username
        role = request.POST.get('role', '')
        quote = request.POST.get('quote', '')
        rating = int(request.POST.get('rating') or 5)
        avatar_url = request.POST.get('avatar_url', '')
        if quote and 1 <= rating <= 5:
            Testimonial.objects.create(name=name, role=role, quote=quote, rating=rating, avatar_url=avatar_url, is_approved=True)
            messages.success(request, 'Thanks for your feedback!')
            return redirect('cms:testimonials')
        messages.error(request, 'Please provide a quote and rating.')
    return render(request, 'cms/submit_testimonial.html')


@staff_member_required
def bulk_upload_media(request):
    """Bulk upload interface for media assets - WordPress style"""
    if request.method == 'GET':
        return render(request, 'admin/cms/mediaasset/bulk_upload.html', {
            'title': 'Bulk Upload Media',
            'site_title': 'Magma7 Fitness',
            'site_header': 'Magma7 Admin',
        })
    return redirect('admin:cms_mediaasset_changelist')


@staff_member_required
@require_POST
def ajax_upload_media(request):
    """Handle AJAX file upload for bulk uploads"""
    if not request.FILES.getlist('files'):
        # Log a warning for diagnostics
        try:
            ErrorLog.objects.create(
                severity='WARNING',
                message='Bulk upload (media) called with no files',
                path=request.path,
                method=request.method,
                user=getattr(request.user, 'username', ''),
                ip_address=request.META.get('HTTP_X_FORWARDED_FOR', '').split(',')[0] or request.META.get('REMOTE_ADDR', ''),
                user_agent=request.META.get('HTTP_USER_AGENT', ''),
                exception_type='',
                traceback=''
            )
        except Exception:
            pass
        return JsonResponse({'error': 'No files provided'}, status=400)

    uploaded_files = []
    errors = []

    for uploaded_file in request.FILES.getlist('files'):
        try:
            # Auto-detect asset type
            file_ext = uploaded_file.name.lower().split('.')[-1]
            if file_ext in ['jpg', 'jpeg', 'png', 'gif', 'svg', 'webp']:
                asset_type = 'image'
            elif file_ext in ['mp4', 'webm']:
                asset_type = 'video'
            elif file_ext in ['pdf']:
                asset_type = 'document'
            else:
                asset_type = 'other'

            # Create MediaAsset
            media_asset = MediaAsset(
                title=uploaded_file.name,
                file=uploaded_file,
                asset_type=asset_type,
                uploaded_by=request.user
            )

            # Save to trigger file size/dimension detection
            media_asset.save()

            uploaded_files.append({
                'id': media_asset.id,
                'title': media_asset.title,
                'url': media_asset.get_absolute_url(),
                'asset_type': media_asset.asset_type,
                'file_size': media_asset.file_size,
                'dimensions': f"{media_asset.width}×{media_asset.height}" if media_asset.width else None
            })

        except Exception as e:
            errors.append({'filename': uploaded_file.name, 'error': str(e)})
            # Server-side diagnostic logging
            try:
                import traceback as _tb
                ErrorLog.objects.create(
                    severity='ERROR',
                    message=f"Bulk upload (media) failed for {uploaded_file.name}: {e}",
                    path=request.path,
                    method=request.method,
                    user=getattr(request.user, 'username', ''),
                    ip_address=request.META.get('HTTP_X_FORWARDED_FOR', '').split(',')[0] or request.META.get('REMOTE_ADDR', ''),
                    user_agent=request.META.get('HTTP_USER_AGENT', ''),
                    exception_type=type(e).__name__,
                    traceback=_tb.format_exc(),
                )
            except Exception:
                pass

    return JsonResponse({
        'success': True,
        'uploaded': uploaded_files,
        'errors': errors,
        'total': len(uploaded_files),
        'failed': len(errors)
    })


@staff_member_required
def bulk_upload_home_gallery(request):
    """Bulk upload interface dedicated for Home Gallery images."""
    if request.method == 'GET':
        return render(request, 'admin/cms/homegallery/bulk_upload.html', {
            'title': 'Bulk Upload Home Gallery Images',
        })
    return redirect('admin:cms_homegalleryimage_changelist')


@staff_member_required
@require_POST
def ajax_upload_home_gallery(request):
    """Upload files and create HomeGalleryImage records automatically."""
    files = request.FILES.getlist('files')
    if not files:
        try:
            ErrorLog.objects.create(
                severity='WARNING',
                message='Bulk upload (home gallery) called with no files',
                path=request.path,
                method=request.method,
                user=getattr(request.user, 'username', ''),
                ip_address=request.META.get('HTTP_X_FORWARDED_FOR', '').split(',')[0] or request.META.get('REMOTE_ADDR', ''),
                user_agent=request.META.get('HTTP_USER_AGENT', ''),
                exception_type='',
                traceback=''
            )
        except Exception:
            pass
        return JsonResponse({'error': 'No files provided'}, status=400)

    uploaded = []
    errors = []

    # Determine starting order
    try:
        start_order = (HomeGalleryImage.objects.order_by('-order').first().order or 0) + 1
    except Exception:
        start_order = 1

    order_counter = start_order

    for f in files:
        try:
            # Save to MediaAsset for library reference
            file_ext = f.name.lower().split('.')[-1]
            if file_ext in ['jpg', 'jpeg', 'png', 'gif', 'svg', 'webp']:
                asset_type = 'image'
            elif file_ext in ['mp4', 'webm']:
                asset_type = 'video'
            elif file_ext in ['pdf']:
                asset_type = 'document'
            else:
                asset_type = 'other'

            ma = MediaAsset(title=f.name, file=f, asset_type=asset_type, uploaded_by=request.user)
            # Set usage to gallery if image
            if asset_type == 'image':
                ma.usage = 'gallery'
            ma.save()

            # Derive title from filename (without extension)
            title = f.name.rsplit('.', 1)[0]

            # Create HomeGalleryImage
            hgi = HomeGalleryImage.objects.create(
                title=title,
                image_url=ma.get_absolute_url(),
                description='',
                order=order_counter,
                is_active=True,
            )
            order_counter += 1

            uploaded.append({
                'id': hgi.id,
                'title': hgi.title,
                'image_url': hgi.image_url,
                'order': hgi.order,
            })
        except Exception as e:
            errors.append({'filename': f.name, 'error': str(e)})
            try:
                import traceback as _tb
                ErrorLog.objects.create(
                    severity='ERROR',
                    message=f"Bulk upload (home gallery) failed for {f.name}: {e}",
                    path=request.path,
                    method=request.method,
                    user=getattr(request.user, 'username', ''),
                    ip_address=request.META.get('HTTP_X_FORWARDED_FOR', '').split(',')[0] or request.META.get('REMOTE_ADDR', ''),
                    user_agent=request.META.get('HTTP_USER_AGENT', ''),
                    exception_type=type(e).__name__,
                    traceback=_tb.format_exc(),
                )
            except Exception:
                pass

    return JsonResponse({
        'success': True,
        'uploaded': uploaded,
        'errors': errors,
        'total': len(uploaded),
        'failed': len(errors),
    })
