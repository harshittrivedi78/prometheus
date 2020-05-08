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
pip install prometheus
```

Or, if you're using a development version cloned from this repository:

```shell
git clone <repo-url>
python prometheus/setup.py install
```

This will install [prometheus_client](https://github.com/prometheus/client_python) as a dependency.

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
    
    @monitor(app_name="test")
    def retrieve(self, request, *args, **kwargs):
        data = {}
        return Response(data, status=status.HTTP_200_OK)
```

So as you can see in the above example I have decorated the retrieve function by our monitor
decorator which will provide monitoring metrics for this function only. And you can identify
how much time this function is taking to execute, how many requests are in progress currently, 
how many request totally served till now.


