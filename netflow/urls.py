from django.conf.urls import patterns
from django.conf.urls import url
from django.conf.urls import include
from .views import IndexView, GraphsDetailView, InRateDetailView, OutRateDetailView, GraphsDetailRateView
from openstack_dashboard.dashboards.project.netflow import views
    
urlpatterns = patterns('',
	url(r'^$', IndexView.as_view(), name='index'),
	url(r'^(?P<resource_id>[^/]+)/graphsdetail/$', GraphsDetailView.as_view(), name='graphsdetail'),
	url(r'^(?P<iface_id>[^/]+)/graphsdetailrate/$', GraphsDetailRateView.as_view(), name='graphsdetailrate'),
	url(r'^(?P<date>[^/]+)/in/$', InRateDetailView.as_view(), name='in'),
	url(r'^(?P<date>[^/]+)/out/$', OutRateDetailView.as_view(), name='out'),
	url(r'^(?P<metric>[^/]+)/(?P<resource_id>[^/]+)/$', views.get_ceilometer_data, name='get_ceilometer_data'),
	url(r'^(?P<metric>[^/]+)/(?P<resource_id>[^/]+)/(?P<time>[^/]+)/$', views.get_ceilometer_data_rate, name='get_ceilometer_data_rate'),
)
