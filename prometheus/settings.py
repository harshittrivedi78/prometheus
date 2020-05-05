import os
from django.conf import settings

# Prometheus Settings

MULTIPROC_MODE = getattr(settings, "MULTIPROC_MODE", True)
MULTIPROC_DIR = settings.BASE_DIR + '/prometheus/multiproc_dir'


def setup():
    print("setting up prometheus")
    if MULTIPROC_MODE:
        dir_name = MULTIPROC_DIR
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
        os.environ["prometheus_multiproc_dir"] = dir_name
        return dir_name
