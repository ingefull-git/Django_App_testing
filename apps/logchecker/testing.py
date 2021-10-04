from datetime import datetime as dt
from . import models
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save
from django.db.models import Q, Count


def read_log(pk):
    print("Reading logs:", pk)
    log_last = models.Log.objects.filter(client_id=pk).order_by('created').last()
    date_last = log_last.created.date()
    logs = models.Log.objects.filter(
            Q(client_id=pk) & Q(created__date=date_last)).\
                values('entity_id').annotate(
                    error=Count('status', filter=Q(status='Error')),
                    warning=Count('status', filter=Q(status='Warning')),
                    undefined=Count('status', filter=Q(status='Undefined')),
                    ok=Count('status', filter=Q(status='Ok'))).order_by('entity_id')
    print(logs)
    print(logs.query)
    estado = ""
    for entity in logs:
        if entity['error']:
            estado = "Error"
        elif entity["warning"] and estado != "Error":
            estado = "Warning"
        elif entity["ok"] and estado != "Warning": 
            estado = "Ok"
        elif estado != "Error" and estado != "Warning" and estado != "Ok":
            estado = "Undefined"
    return estado

@receiver(post_save, sender=models.District)
def check_status(sender, instance, created, **kwargs):
    if created:
        print("District Created: ", instance)
    if created == False:
        histoid = f'{dt.now().date()}_{instance}'
        histoobj = models.ClientHistoric.objects.filter(histo=histoid).first()
        if histoobj:
            histoobj.status = instance.status
            histoobj.save()
        else:
            models.ClientHistoric.objects.create(client=instance)

def update_servers():
    server_dict = {}
    for server in models.SERVERS:
        d_tot = []
        for sta in models.STATUS:
            d_count = models.District.objects.filter(Q(server=server) & Q(status=sta[0])).count()
            d_tot.append(d_count)
            server_dict[server] = d_tot
    return server_dict

def get_chart_values():
    dist_total = models.District.objects.all().count()
    chart_values = []
    if dist_total:
        for stat in models.STATUS:
            cant = models.District.objects.filter(status=stat[0]).count()
            val = int(round((cant*100/dist_total),0))
            chart_values.append(val)
    return chart_values

def query_districts(item, iterator):
    status = {}
    status_label = []
    result = {}
    for var in iterator:
        status[var]= models.District.objects.filter(Q(**{item:var})).aggregate(
            error=Count('status', filter=Q(status='Error')),
            warning=Count('status', filter=Q(status='Warning')),
            undefined=Count('status', filter=Q(status='Undefined')),
            ok=Count('status', filter=Q(status='Ok')))
        for key, val in status[var].items():
            if key not in result:
                result[key] = [val]
            else:
                result[key].append(val)
        status_label.append(var)
    return result, status_label
    