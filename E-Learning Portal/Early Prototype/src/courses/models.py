import random
import os
from django.db import models
from django.db.models import Q
from django.db.models.signals import pre_save, post_save
from django.urls import reverse


from Elearning.utils import unique_slug_generator

def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext

def upload_image_path(instance, filename):
    new_filename = random.randint(1, 454687545)
    name, ext = get_filename_ext(filename)
    final_filename = '{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)
    return "courses/{new_filename}/{final_filename}".format(
            new_filename=new_filename,
            final_filename=final_filename
            )

class CourseQuerySet(models.query.QuerySet):
    def active(self):
        return self.filter(active = True)

    def featured(self):
        return self.filter(featured=True, active = True)

    def search(self, query):
        lookups = (
                Q(title__icontains=query) |
                Q(description__icontains=query) |
                Q(tag__title__icontains=query)
                )
        return self.filter(lookups).distinct()    

class CourseManager(models.Manager):
    def get_queryset(self):
        return CourseQuerySet(self.model, using=self._db)

    def all(self):
        return self.get_queryset().active()

    def featured(self): #Course.objects.featured()
        return self.get_queryset().featured()
     
    def get_by_id(self, id):
        qs = self.get_queryset().filter(id=id)
        if qs.count() ==1:
            return qs.first()
        return None   

    def search(self, query):  
        return self.get_queryset().active().search(query)

# Create your models here.
class Course(models.Model):
    title           = models.CharField(max_length=120)
    slug            = models.SlugField(null=True, blank=True, unique=True)
    description     = models.TextField()
    playlist_id     = models.TextField(default='playlist_id')
    price           = models.DecimalField(decimal_places=2, max_digits=20, default=107.84)
    image           = models.ImageField(upload_to='courses/', null=True, blank = True)
    featured        = models.BooleanField(default=False)
    active          = models.BooleanField(default=True)

    objects = CourseManager()

    def get_absolute_url(self):
        #return "/courses/{slug}/".format(slug=self.slug)
        return reverse("courses:detail", kwargs={"slug":self.slug})

    def __str__(self):
        return self.title
        
    @property
    def name(self):
        return self.title    

def course_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(course_pre_save_receiver, sender=Course)    