import datetime
import json
import re
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.core.serializers import serialize
from django.db.models import Q, Sum, Count, Min, F, Case, Value, When
from django.http import JsonResponse
from django.shortcuts import (
    HttpResponse,
    HttpResponseRedirect,
    get_object_or_404,
    redirect,
    render,
)
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView

from apps.logchecker.models import District, Log, SERVERS, STATUS

from .forms import DistrictModelForm
from .testing import get_chart_values, read_log, update_servers, query_districts

class HomeView(ListView):
    model = District
    template_name = "home.html"
    success_url = 'home'
   
    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        districts = District.objects.all()
        if request.is_ajax():
            if "refresh" in self.request.GET:
                data = districts.values()
                return JsonResponse(list(data), safe=False)
        context = self.get_context_data()
        servers = update_servers()
        bars_values, bars_labels = query_districts('server', SERVERS)
        histo_values, histo_labels = query_districts('created__day', range(1,31))
        context['chart_labels'] = [label[0] for label in STATUS]
        context['servers'] = servers
        context['result'] = bars_values
        context['histo_val'] = histo_values
        context['histo_label'] = histo_labels
        context['stacked_label'] = bars_labels
        context['page_name'] = "APP-LogChecker"
        context['page_title'] = "General Status Dashboard"
        return render(request, 'home.html', context)

    def post(self, request, *args, **kwargs):
        data = {}
        districts = {}
        page_obj = {}
        # if "refresh" in request.POST:
        districts = District.objects.all()
        if 'searchfield' in request.POST:
            search = request.POST['formData[1][value]']
            if search:
                districts = District.objects.filter(Q(psid_str__icontains=search) |
                                        Q(name__icontains=search) | 
                                        Q(status__icontains=search))
            
        pagin = Paginator(districts, 10)
        page_obj = pagin.get_page(1)
        data = [{'name':obj.name, 'psid':obj.psid, 'status':obj.status} for obj in page_obj]
        return JsonResponse(list(data), safe=False)


def pie_chart(request):
    labels = []
    data = []
    if 'psid' in request.GET:
        psid = request.GET.get("psid")
        dist = District.objects.get(psid=psid)
        Log.objects.create(client=dist, entity_name="Demographics", status="Undefined")
    
    chart_values = get_chart_values()
    chart_lables = [label[0] for label in STATUS]
    data = {'labels':chart_lables, 'values': chart_values}
    return JsonResponse(data)


def update_log_view(request, psid):
    estado = read_log(psid)
    
    dist = District.objects.get(psid=psid)
    # Log.objects.create(client=dist, entity_name="Demographics", status="Warning")
    dist.status = estado
    dist.save()

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
            return redirect('logchecker:home')
        elif request.is_ajax():
            data = {}
            data['error'] =[[field.label, error] for field in form for error in field.errors]
            print("Data: ", data)
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
