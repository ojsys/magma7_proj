from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Avg
from django.shortcuts import redirect, render

from .models import Testimonial


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

