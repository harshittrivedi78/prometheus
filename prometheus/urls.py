from django.conf.urls import url
from prometheus.views import PrometheusMetricsView, PrometheusMetricsPushView

urlpatterns = (
    url(r'^metrics', PrometheusMetricsView.as_view(), name='get-metrics'),
    url(r'^push/metrics', PrometheusMetricsPushView.as_view(), name='push-metrics'),
)
