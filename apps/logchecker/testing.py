from . import models
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save
from django.db.models import Q


def read_log(pk):
    print("Reading logs:", pk)
    val = pk
    return val

@receiver(post_save, sender=models.Log)
def check_status(sender, instance, created, **kwargs):
    status_log = models.STATUS[3][0]
    for status in models.STATUS:
        logs = models.Log.objects.filter(Q(client=instance.client) & Q(status=status[0]))
        if logs:
            if status[0] == models.STATUS[0][0]:
                status_log = status[0]
            elif status[0] == models.STATUS[1][0]:
                status_log = status[0]
            elif status[0] == models.STATUS[2][0]:
                status_log = status[0]
    if created:
        instance.client.status = status_log
        instance.client.save()
    if created == False:
        instance.client.status = status_log
        instance.client.save()


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
