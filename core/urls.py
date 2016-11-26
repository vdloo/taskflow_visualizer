from django.conf.urls import url, include

urlpatterns = [
    url(r'^', include('taskflow_visualizer.urls')),
]
