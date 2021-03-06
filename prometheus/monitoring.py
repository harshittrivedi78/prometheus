import requests
from prometheus.metrics import Metrics, BatchMetrics
from prometheus.utils import Time, TimeSince
from prometheus import settings


class Monitor:
    metrics_cls = Metrics

    def __init__(self, app_name):
        self.app_name = app_name
        self.metrics = self.metrics_cls.get_instance()
        self.app_metric = self.metrics.apps.get(app_name, None)
        if not self.app_metric:
            self.app_metric = self.metrics.setup_metrics(app_name)

    def __call__(self, func):
        def inner(*args, **kwargs):
            start_time = Time()
            self.app_metric['REQUEST_COUNT'].inc()
            self.app_metric['REQUEST_IN_PROGRESS'].inc()
            error, response = None, None
            try:
                response = func(*args, **kwargs)
            except Exception as exc:
                error = exc
            status = getattr(response, "status_code", 200 if not error else 400)
            self.app_metric['RESPONSE_BY_STATUS'].labels(status=status).inc()
            self.app_metric['REQUEST_LATENCY'].observe(
                TimeSince(start_time)
            )
            self.app_metric['REQUEST_IN_PROGRESS'].dec()
            if error:
                raise error
            return response

        return inner


monitor = Monitor


class BatchMonitor(Monitor):
    metrics_cls = BatchMetrics

    def __init__(self, app_name):
        super().__init__(app_name=app_name)
        self.push_metrics_url = settings.PROMETHEUS_PUSH_METRICS_URL

    def __call__(self, func):
        def inner(*args, **kwargs):
            error, response = None, None
            start_time = Time()
            self.app_metric['REQUEST_COUNT'].inc()
            try:
                response = func(*args, **kwargs)
            except Exception as exc:
                error = exc
                self.app_metric["LAST_FAILURE"].set_to_current_time()
            else:
                self.app_metric["LAST_SUCCESS"].set_to_current_time()
            finally:
                self.app_metric['TIME_TAKEN'].set(
                    TimeSince(start_time)
                )
                self.push_metrics()
            if error:
                raise error
            return response

        return inner

    def _collect_metrics(self):
        metrics = {}
        for key, value in self.app_metric.items():
            metrics[key] = value.collect()[0].samples[0].value
        metrics["APP_NAME"] = self.app_name
        return metrics

    def push_metrics(self):
        print("pushing metrics")
        base_url = "%s://%s:%s" % (
            settings.PROMETHEUS_METRICS_PROTOCOL, settings.PROMETHEUS_METRICS_HOST, settings.PROMETHEUS_METRICS_PORT)
        base_url += self.push_metrics_url
        data = self._collect_metrics()
        response = requests.post(base_url, data=data)
        if response.status_code == 200:
            print("metrics pushed successfully")
        else:
            print(response.content)
            print("could not push metrics")


batch_monitor = BatchMonitor
