from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.views.generic import ListView

from apps.logchecker.models import District


def home(request):
    context = {}
    dist_all = District.objects.all()
    if request.method == 'POST':
        context['title'] = "Es un POST"
        return redirect('logchecker:home')
    elif request.method == 'GET':
        context['title'] = "APP-LogChecker"
        context['districs'] = dist_all
    return render(request, 'home.html', context)

@login_required
class HomeView(ListView):
    model = District
    template_name = "home.html"
    success_url = 'home'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["a"] = 1
        return context