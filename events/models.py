from django.db import models
from django.utils import timezone
# Create your models here.


class Event(models.Model):
    wastunuid = models.CharField(max_length=200, unique=True)
    dtstart = models.DateTimeField()
    dtend = models.DateTimeField()
    dtstamp = models.DateTimeField()
    originalurl = models.CharField(max_length=255)
    summary = models.CharField(max_length=1024)
    description = models.TextField()
    categories = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    xapple_structured_location = models.CharField(max_length=255)
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.summary