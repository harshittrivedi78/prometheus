import os
import prometheus_client
from prometheus_client import multiprocess
from django.http import HttpResponse
from rest_framework import generics


class PrometheusMetricsView(generics.RetrieveAPIView):

    def retrieve(self, request, *args, **kwargs):
        if "prometheus_multiproc_dir" in os.environ:
            # prometheus_client.values.ValueClass = prometheus_client.values.MultiProcessValue(
            #     os.getpid  # in case of uwsgi mode: uwsgi.worker_id
            # )
            registry = prometheus_client.CollectorRegistry(auto_describe=True)
            multiprocess.MultiProcessCollector(registry)
        else:
            registry = prometheus_client.REGISTRY
        metrics_page = prometheus_client.generate_latest(registry)
        return HttpResponse(
            metrics_page, content_type=prometheus_client.CONTENT_TYPE_LATEST
        )
