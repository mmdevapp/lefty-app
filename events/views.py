from django.shortcuts import render
from django.http import HttpResponse
import urllib.request
import json
from events.models import Event

# I Calendar
import icalendar
# https://icalendar.readthedocs.io/en/latest/

# Create your views here.

def events_update(request):
 # Retrieve the iCalendar file from the provided URL
    ical_data = urllib.request.urlopen("https://wastun.co/events.ics").read()

    # Parse the iCalendar file using icalendar library
    cal = icalendar.Calendar.from_ical(ical_data)

    # Loop through the events in the calendar
    events = []
    # Loop through the events in the calendar and save them as Django model instances
    for event in cal.walk('VEVENT'):
    #originalurl = models.CharField(max_length=255)
    #categories = models.CharField(max_length=255)
    #xapple_structured_location = models.CharField(max_length=255)
        event_data = {
            'uid': str(event.get('UID')),
            'summary': str(event.get('SUMMARY')),
            'description': str(event.get('DESCRIPTION')),
            'location': str(event.get('LOCATION')),
            'dtstart': event.get('DTSTART').dt,
            'dtend': event.get('DTEND').dt,
            'dtstamp': event.get('DTSTAMP').dt,
            'originalurl': str(event.get('URL')),
            'categories': str(event.get('CATEGORIES').cats[0]),

        }
        try:
            # Attempt to retrieve an existing instance of the model with the provided key
            instance = Event.objects.get(uid=event_data['uid'])
        except Event.DoesNotExist:
            # If the instance does not exist, create a new one
            instance = Event.objects.create(**event_data)
            instance.download_and_analyze_image()
        else:
            instance.__dict__.update(**event_data)
            instance.download_and_analyze_image()
            instance.save()
        events.append(event_data)



    # Return the events as a simple HTML list
    html = '<ul>'
    for event in events:

        html += f'<li>{event["summary"]} ({event["dtstart"]} - {event["dtend"]})</li>'
    html += '</ul>'

    return HttpResponse(html)      
      #return render(request, 'events/events_update.html', {})

def events_update_kassa(request):
    response = urllib.request.urlopen("https://www.kassablanca.de/wp-json/wp/v2/events?per_page=100").read()
    jsonResponse = json.loads(response)
    events = []
    # Loop through the events in the calendar and save them as Django model instances
    for event in jsonResponse:
            event_ical = urllib.request.urlopen("https://www.kassablanca.de/wp-content/themes/wptheme/ical.php?e=" + str(event['id'])).read()
            cal = icalendar.Calendar.from_ical(event_ical)
            try:
                image_data = urllib.request.urlopen(str(event['_links']['wp:featuredmedia'][0]['href'])).read()
                imagejsonResponse = json.loads(image_data)
                print(imagejsonResponse['guid']['rendered'])
                image_url = imagejsonResponse['guid']['rendered']
            except:
                image_url = str()
            for thisevent in cal.walk('VEVENT'):
                event_data = {
                'uid': "kassa" + str(event['id']),
                'summary': str(thisevent.get('SUMMARY')),
                'description': str(event['content']['rendered']),
                'originalurl': str(event['link']),
                'image_url': str(image_url),
                'location': str(thisevent.get('LOCATION')),
                'dtstart': thisevent.get('DTSTART').dt,
                'dtstamp': thisevent.get('DTSTAMP').dt,
                'categories': str("Kultur"),
                }
                try:
                        # Attempt to retrieve an existing instance of the model with the provided key
                        instance = Event.objects.get(uid=event_data['uid'])
                except Event.DoesNotExist:
                        # If the instance does not exist, create a new one
                        instance = Event.objects.create(**event_data)
                else:
                        instance.__dict__.update(**event_data)

                        instance.save()

    return HttpResponse(jsonResponse)