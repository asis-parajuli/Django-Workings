from django.conf.urls import url

from .views import (
        CourseListView, 
        CourseDetailSlugView
        )

urlpatterns = [
    url(r'^$', CourseListView.as_view(), name='list'),
    url(r'^(?P<slug>[\w-]+)/$', CourseDetailSlugView.as_view(), name='detail'),    
]
