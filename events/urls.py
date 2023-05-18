from django.urls import path
from . import views
from django.conf.urls import include
from .models import Event
from rest_framework import routers, serializers, viewsets
# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Event
        fields = ['uid', 'summary', 'description', 'location', 'dtstart', 'dtend', 'dtstamp', 'originalurl', 'categories', 'image_url']

# ViewSets define the view behavior.
class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = UserSerializer

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'events', EventViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('wastunupdate', views.events_update, name='events_update'),
    path('kassaupdate', views.events_update_kassa, name='events_update_kassa')
]