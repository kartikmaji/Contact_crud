from django.conf.urls import url, include
from api.views import create, read, update, delete
from rest_framework.urlpatterns import format_suffix_patterns

from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = {
    url(r'^contact/create/$', create, name="create"),
    url(r'^contact/get/$', read, name="read"),
    url(r'^contact/update/$', update, name="update"),
    url(r'^contact/delete/$', delete, name="delete"),
    url(r'^auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^get-token/', obtain_auth_token),
}

urlpatterns = format_suffix_patterns(urlpatterns)