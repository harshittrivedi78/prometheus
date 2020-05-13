from prometheus_client import Counter, Histogram, Gauge
from prometheus import settings


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
        orig_app_name = app_name
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
                settings, "PROMETHEUS_LATENCY_BUCKETS"
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
            {orig_app_name: app}
        )
        return app


class BatchMetrics:
    _instance = None

    @classmethod
    def get_instance(cls):
        if not cls._instance:
            cls._instance = cls()
        return cls._instance

    def __init__(self):
        self.apps = {}

    def setup_metrics(self, app_name):
        orig_app_name = app_name
        app = self.apps.get(app_name, dict())
        if app:
            return app
        app_name += "_"
        app['REQUEST_COUNT'] = Counter(
            app_name + 'requests_total', 'Total Request Count',
        )
        app["TIME_TAKEN"] = Gauge(
            app_name + 'time_taken_seconds', 'Time Taken By the Job in seconds',
        )
        app["LAST_SUCCESS"] = Gauge(
            app_name + 'last_success', 'Last Success Time of the Job',
        )
        app["LAST_FAILURE"] = Gauge(
            app_name + 'last_failure', 'Last Failure Time of the Job',
        )
        self.apps.update(
            {orig_app_name: app}
        )
        return app

    def push_metrics(self, data):
        app = self.setup_metrics(data["APP_NAME"])
        app["REQUEST_COUNT"].inc(float(data["REQUEST_COUNT"]))
        app["TIME_TAKEN"].set(data["TIME_TAKEN"])
        app["LAST_SUCCESS"].set(data["LAST_SUCCESS"])
        app["LAST_FAILURE"].set(data["LAST_FAILURE"])


batch_metrics = BatchMetrics.get_instance()