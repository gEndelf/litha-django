from django.conf.urls import patterns, url

from companies import views


urlpatterns = patterns('',
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^company_form/$', views.CompanyFormView.as_view(), name='company_form'),
    url(r'^companies/$', views.CompanyListView.as_view(), name='company_list'),
    url(r'^companies/(?P<pk>\d+)/$', views.CompanyDetailView.as_view(), name='company_detail'),
)
