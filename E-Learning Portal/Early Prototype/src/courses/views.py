from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.views.generic import ListView, DetailView
from django.shortcuts import render, get_object_or_404

from analytics.mixins import ObjectViewedMixin
from carts.models import Cart

from .models import Course

class CourseFeaturedListView(ListView):
    template_name = "courses/list.html"
    
    def get_context_data(self, *args, **kwargs):
        context = super(CourseFeaturedListView, self).get_context_data(*args, **kwargs)
        cart_obj , new_obj = Cart.objects.new_or_get(self.request)
        context['cart'] = cart_obj
        return context

class CourseFeaturedDetailView(ObjectViewedMixin, DetailView):
    queryset = Course.objects.all().featured()
    template_name = "courses/featured-detail.html"


class UserHistoryView(LoginRequiredMixin, ListView):
    template_name = "courses/user-history.html"
   
    def get_queryset(self, *args, **kwargs):
        request = self.request
        views = request.user.objectviewed_set.by_model(Course) #.all().filter(content_type='course') 
        # viewed_ids = [x.object_id for x in views]
        return views


class CourseListView(ListView):
    template_name = "courses/list.html"
   
    def get_queryset(self, *args, **kwargs):
        request = self.request
        return Course.objects.all()



class CourseDetailSlugView(ObjectViewedMixin, DetailView):
    queryset = Course.objects.all()
    template_name = "courses/detail.html"

    def get_context_data(self, *args, **kwargs):
        context = super(CourseDetailSlugView, self).get_context_data(*args, **kwargs)
        cart_obj , new_obj = Cart.objects.new_or_get(self.request)
        context['cart'] = cart_obj
        return context

    def get_object(self, *args, **kwargs):
        request = self.request
        slug = self.kwargs.get('slug')
        #instance = get_object_or_404(Course, slug=slug, active=True)
        try:
            instance= Course.objects.get(slug=slug, active=True)
        except Course.DoesNotExist:
            raise Http404("Not found..")
        except Course.MultipleObjectsReturned:
            qs = Course.objects.filter(slug=slug, active=True)
            instance = qs.first() 
        except:
            raise Http404("Oops!")
        #object_viewed_signal.send(instance.__class__, instance = instance, request = request)    
        return instance


class CourseDetailView(ObjectViewedMixin, DetailView):
    template_name = "courses/detail.html"

    def get_context_data(self, *args, **kwargs):
        context = super(CourseDetailView, self).get_context_data(*args, **kwargs)
        print (context)
        return context

    def get_object(self, *args, **kwargs):
        request = self.request
        pk = self.kwargs.get('pk')
        instance = Course.objects.get_by_id(pk)
        if instance is None:
            raise Http404("Course doesn't exitst")
        return instance
