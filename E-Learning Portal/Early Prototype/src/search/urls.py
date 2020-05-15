from django.conf.urls import url

from .views import (
        SearchCourseView
        )

urlpatterns = [
    url(r'^$', SearchCourseView.as_view(), name='query')
]
