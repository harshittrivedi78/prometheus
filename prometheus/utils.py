from timeit import default_timer
from prometheus.constants import DEFAULT_LATENCY_BUCKETS


def Time():
    return default_timer()


def TimeSince(start_time):
    return default_timer() - start_time
