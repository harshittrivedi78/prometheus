from django.conf.urls import url
from prometheus.views import PrometheusMetricsView

urlpatterns = (
    url(r'^metrics', PrometheusMetricsView.as_view(), name='get-metrics'),
)
