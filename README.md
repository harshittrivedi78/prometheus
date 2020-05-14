# prometheus
Python prometheus library for django and django rest framework.
This helps in monitoring the application on a granular level. You can customize which part 
of the application you want to monitor. Through this you can monitor a REST API, a python 
function , a code segment.

## Usage

### Requirements

* Django >= 1.8
* djangorestframework >= 3.0
* prometheus_client >= 0.7.1

### Installation

Install with:

```shell
pip install prometheus-python
```

Or, if you're using a development version cloned from this repository:

```shell
git clone https://github.com/harshittrivedi78/prometheus.git
python prometheus/setup.py install
```
This will install Django >= 1.8 and djangorestframework >= 3.0 and [prometheus_client](https://github.com/prometheus/client_python) as a dependency if not installed already.
### Quickstart

In your settings.py:

```python
INSTALLED_APPS = [
   ...
   'prometheus',
   ...
]
```

In your urls.py:

```python
urlpatterns = [
    ...
    url('', include('prometheus.urls')),
]
```

In your views.py:

```python
from rest_framework import generics, status
from rest_framework.response import Response
from prometheus import monitor

class TestAPIView(generics.RetrieveAPIView):
    
    @monitor(app_name="test") # app_name should be unique through out the application.
    def retrieve(self, request, *args, **kwargs):
        data = {}
        return Response(data, status=status.HTTP_200_OK)
```

So as you can see in the above example I have decorated the retrieve function by our monitor
decorator which will provide monitoring metrics for this function only. And you can identify
how much time this function is taking to execute, how many requests are in progress currently, 
how many request totally served till now.

Metrics are exposed to:
```
http://localhost:8000/metrics
```

### Default list of monitored metrics 
```
* request_count
* request_latency
* request_in_progress
* response_by_status_total
```

### Configuration
Prometheus uses Histogram based grouping for monitoring latencies. The default
buckets are here: https://github.com/prometheus/client_python/blob/master/prometheus_client/core.py

You can define custom buckets for latency, adding more buckets decreases performance but
increases accuracy: https://prometheus.io/docs/practices/histograms/

In your settings.py
```python
PROMETHEUS_LATENCY_BUCKETS = (.1, .2, .5, .6, .8, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.5, 9.0, 12.0, 15.0, 20.0, 30.0, float("inf"))
```

### Monitor in multiprocess mode (uWSGI, Gunicorn)
In your settings.py
```python
PROMETHEUS_MULTIPROC_MODE = True # default is False
PROMETHEUS_MULTIPROC_DIR = /path/to/prometheus_multiproc_dir # default it will save db files in prometheus/multiproc_dir/
```
### Monitoring of Batch Jobs
So in prometheus legacy system we have to collect the metrics and push those metrics to the pushgateway and then prometheus server has to scrape those metrics from push gateway. But now I have modified this apporach. Now I have exposed an endpoint in this prometheus client to push your metrics.

So as usual you must be running prometheus client with server (Django, Django Rest Framework).

In settings.py: these settings is actually where your server is running.
```python
PROMETHEUS_METRICS_PROTOCOL = "HTTP" # or HTTPS
PROMETHEUS_METRICS_HOST = "127.0.0.1"
PROMETHEUS_METRICS_PORT = "8000"
PROMETHEUS_PUSH_METRICS_URL = "/push/metrics"
```
In your any batch_job.py
```python
from prometheus import batch_monitor

@batch_monitor(app_name="sum")
def sum(a,b):
   return a+b
   
sum(10, 20)
```
So here this batch_monitor decorator will push the metrics to you server and add monitored metrics into your server's metrics.

### Default Batch Job Monitored Metrics
```
* request_count
* time_takne
* last_success
* Last_failure
```
These metrics can be seen at `/metrics` endpoint.
