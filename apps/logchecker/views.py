import datetime
import json

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.serializers import serialize
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import (HttpResponse, HttpResponseRedirect,
                              get_object_or_404, redirect, render)
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView

from apps.logchecker.models import SERVERS, STATUS, District, Log

from .forms import DistrictModelForm
from .testing import get_chart_values, read_log, update_servers


class HomeView(ListView):
    model = District
    template_name = "home.html"
    success_url = 'home'

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(HomeView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return self.model.objects.all()

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            if 'action' in request.POST:
                peka = request.POST['action']
                user = User.objects.get(username='rulo')
                var = read_log(peka)
                client = District(user_id=user.pk, name="Dist"+str(var), psid=222222)
                client.save()
            if 'test' in request.POST:
                result = serialize('json', self.get_queryset())
                res = json.loads(result)
                res_f = []
                for d in res:
                    var_a = d['fields']
                    var_a.update({'pk':d['pk']})
                    res_f.append(var_a)
                data = json.dumps(res_f)
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(data, 'aplication/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search = self.request.GET.get('search_')
        districts = District.objects.all()
        if search:
            districts = District.objects.filter(
                Q(name__icontains=search) | 
                Q(psid__icontains=search) | 
                Q(status__icontains=search))
        pagin = Paginator(districts, 2)
        servers = update_servers()
        chart_values = get_chart_values()
        page_num = self.request.GET.get('page')
        try:
            page_obj = pagin.page(page_num)
        except PageNotAnInteger:
            page_obj = pagin.page(1)
        except EmptyPage:
            page_obj = pagin.page(pagin.num_pages)
        context['chart_values'] = chart_values
        context['chart_labels'] = [label[0] for label in STATUS]
        context['page_obj'] = page_obj
        context['servers'] = servers
        context['page_name'] = "APP-LogChecker"
        context['page_title'] = "General Status Dashboard"
        return context


def update_log_view(request, psid):
    var = read_log(psid)
    
    dist = District.objects.get(psid=psid)
    Log.objects.create(client=dist, entity_name="Demographics", status="Ok")

    return redirect('logchecker:home')


def chart_detail_view(request, label):
    context = {}
    today = datetime.datetime.today()
    content = District.objects.filter(status=label)
    context['content'] = content
    context['template'] = 'chart_detail.html'
    context['modal_title'] = 'Chart Detail ' + label
    return render(request, "generic_modal.html", context)


def create_view(request):
    context = {}
    if request.method == 'POST':
        form = DistrictModelForm(request.POST)
        if form.is_valid():
            form.save()
            redirect('logchecker:home')
        elif request.is_ajax():
            data = {}
            data['error'] =[[field.label,error] for field in form for error in field.errors]
            return JsonResponse(data, status=400)
    url_page = reverse('logchecker:district_new')
    form = DistrictModelForm(request.POST or None)
    form.fields['user'].initial = request.user
    context['url_page'] = url_page
    context['form'] = form
    context['template'] = "district_new-update.html"
    context['modal_title'] = "New District"
    return render(request, 'generic_modal.html', context)


def update_view(request, psid):
    context = {}
    obj = get_object_or_404(District, psid=psid)
    if request.method == 'POST':
        form = DistrictModelForm(request.POST, instance=obj)
        form.fields['psid'] = obj.psid
        if form.is_valid():
            form.save()
            redirect('logchecker:home')
        elif request.is_ajax():
            form.fields['psid'] = obj.psid
            data = {}
            data['error'] =[[field.label,error] for field in form for error in field.errors]
            return JsonResponse(data, status=400)
    url_page = reverse('logchecker:district_update', kwargs={'psid' : obj.psid})
    context['url_page'] = url_page
    context['form'] = DistrictModelForm(request.POST or None, instance=obj)
    context['district'] = obj
    context['template'] = "district_new-update.html"
    context['modal_title'] = "Update District"
    return render(request, 'generic_modal.html', context)
