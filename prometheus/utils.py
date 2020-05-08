from timeit import default_timer


def Time():
    return default_timer()


def TimeSince(start_time):
    return default_timer() - start_time
