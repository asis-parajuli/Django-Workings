from django.shortcuts import render
from django.views.generic import ListView
from courses.models import Course

class SearchCourseView(ListView):
    template_name = "search/view.html"

    def get_context_data(self, *args, **kwargs):
        context = super(SearchCourseView, self).get_context_data(*args, **kwargs)
        query = self.request.GET.get('q')
        context['query'] = query
        return context
   
    def get_queryset(self, *args, **kwargs):
        request = self.request
        query = request.GET.get('q')
        if query is not None:
            return Course.objects.search(query)
        return Course.objects.none()
