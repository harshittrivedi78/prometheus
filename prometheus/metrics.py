from django.conf import settings

from prometheus_client import Counter, Histogram, Gauge
from prometheus.utils import *


class Metrics:
    _instance = None

    @classmethod
    def get_instance(cls):
        if not cls._instance:
            cls._instance = cls()
        return cls._instance

    def __init__(self):
        self.apps = {}

    def setup_metrics(self, app_name):
        app = self.apps.get(app_name, dict())
        if app:
            return app
        app_name += "_"
        app['REQUEST_COUNT'] = Counter(
            app_name + 'requests_total', 'Total Request Count',
        )
        app['REQUEST_LATENCY'] = Histogram(
            app_name + 'request_latency_seconds', 'Request latency',
            buckets=getattr(
                settings, "PROMETHEUS_LATENCY_BUCKETS", DEFAULT_LATENCY_BUCKETS
            ),
        )
        app['REQUEST_IN_PROGRESS'] = Gauge(
            app_name + 'requests_in_progress_total', 'Requests in progress',
            multiprocess_mode='livesum',
        )
        app['RESPONSE_BY_STATUS'] = Counter(
            app_name + 'responses_by_status_total', 'Total Response Count By Status',
            ['status']
        )
        self.apps.update(
            {app_name: app}
        )
        return app
