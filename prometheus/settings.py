import os
from django.conf import settings

# Prometheus Settings

PROMETHEUS_MULTIPROC_MODE = getattr(settings, "PROMETHEUS_MULTIPROC_MODE", True)
PROMETHEUS_MULTIPROC_DIR = getattr(settings, "PROMETHEUS_MULTIPROC_DIR",
                                   settings.BASE_DIR + '/prometheus/multiproc_dir')


def setup():
    print("Setting up prometheus")
    if PROMETHEUS_MULTIPROC_MODE:
        dir_name = PROMETHEUS_MULTIPROC_DIR
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
        os.environ["prometheus_multiproc_dir"] = dir_name
        return dir_name
