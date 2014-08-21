from django.conf.urls import patterns, url, include
from rest_framework import routers
from smokesrv import views

router = routers.DefaultRouter()

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browseable API.
urlpatterns = patterns('',
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^users/$', views.UserList.as_view()),
    url(r'^login/$', views.register_or_login),
    url(r'', include('gcm.urls')),

)
