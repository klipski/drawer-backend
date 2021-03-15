from django.conf.urls import url
from django.urls import include

urlpatterns = [
    url(r'', include('djoser.urls')),
    url(r'', include('djoser.urls.jwt')),
]
