from django.db import models
from django.utils import timezone
import requests
from PIL import Image
import os
from bs4 import BeautifulSoup
from django.conf import settings
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from urllib.request import urlopen
# Create your models here.


class Event(models.Model):
    uid = models.CharField(max_length=200, unique=True)
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
    image = models.ImageField(upload_to="eventpics", null= True, blank=True)
    image_url = models.URLField(blank=True, null=True)
    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.summary
    def get_image_from_url(self, url):
       #img_tmp = NamedTemporaryFile(dir='media')
       #with urlopen(url) as uo:
         #  assert uo.status == 200
        #   img_tmp.write(uo.read())
       #    img_tmp.flush()
       #img = File(img_tmp)
       #print(img_tmp.name)
       #self.image.save(img_tmp.name, img)
       self.image_url = url    
    def download_and_analyze_image(self):
        # Fetch the HTML code of the original URL
        response = requests.get(self.originalurl)
        html_code = response.content.decode('utf-8')
        
        # Parse the HTML code using BeautifulSoup
        soup = BeautifulSoup(html_code, 'html.parser')
        
        # Find the first img tag with class 'wp-post-image'
        img_tag = soup.find('img', class_='wp-post-image')
        if img_tag is None:
            # No image found
            return None
        
        # Download the image from the URL
        image_url = str(img_tag['src'])
        self.get_image_from_url(image_url)