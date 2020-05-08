from prometheus.metrics import Metrics
from prometheus.utils import Time, TimeSince


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
