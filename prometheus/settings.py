import os
from django.conf import settings

if not settings.configured:
    settings.configure()

# Prometheus Settings
DEFAULT_LATENCY_BUCKETS = (
    0.01,
    0.025,
    0.05,
    0.075,
    0.1,
    0.25,
    0.5,
    0.75,
    1.0,
    2.5,
    5.0,
    7.5,
    10.0,
    25.0,
    50.0,
    75.0,
    float("inf"),
)

BASE_DIR = getattr(settings, "BASE_DIR",
                   os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

PROMETHEUS_MULTIPROC_MODE = getattr(settings, "PROMETHEUS_MULTIPROC_MODE", False)
PROMETHEUS_MULTIPROC_DIR = getattr(settings, "PROMETHEUS_MULTIPROC_DIR",
                                   BASE_DIR + '/prometheus/multiproc_dir')

PROMETHEUS_LATENCY_BUCKETS = getattr(settings, "PROMETHEUS_LATENCY_BUCKETS", DEFAULT_LATENCY_BUCKETS)

# For pushing batch job metrics to the client where it has
# exposed the metrics api.
# PrometheusServer  ---scrapes_from--> PrometheusClient(RunningWithDjango) <----push_metrics--- BatchJob
PROTOCOL = "HTTP"  # HTTPS
PROMETHEUS_METRICS_HOST = "127.0.0.1"
PROMETHEUS_METRICS_PORT = "8000"


def setup():
    print("Setting up prometheus")
    if PROMETHEUS_MULTIPROC_MODE:
        dir_name = PROMETHEUS_MULTIPROC_DIR
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
        os.environ["prometheus_multiproc_dir"] = dir_name
        return dir_name
