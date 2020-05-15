from django.conf.urls import url

from courses.views import UserHistoryView

from .views import (
        AccountHomeView,
        )

urlpatterns = [
    url(r'^$', AccountHomeView.as_view(), name='home'),
    url(r'history/course/$',UserHistoryView.as_view(), name='user-course-history'),
]
