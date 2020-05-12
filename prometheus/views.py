import os
import prometheus_client
from prometheus_client import multiprocess
from django.http import HttpResponse
from rest_framework import generics
from rest_framework.response import Response

from prometheus.metrics import batch_metrics


class PrometheusMetricsView(generics.RetrieveAPIView):

    def retrieve(self, request, *args, **kwargs):
        if "prometheus_multiproc_dir" in os.environ:
            registry = prometheus_client.CollectorRegistry(auto_describe=True)
            multiprocess.MultiProcessCollector(registry)
        else:
            registry = prometheus_client.REGISTRY
        metrics_page = prometheus_client.generate_latest(registry)
        return HttpResponse(
            metrics_page, content_type=prometheus_client.CONTENT_TYPE_LATEST
        )


class PrometheusMetricsPushView(generics.CreateAPIView):

    def create(self, request, *args, **kwargs):
        batch_metrics.push_metrics(request.data)
        return Response({})
