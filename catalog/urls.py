from django.urls import path, include

from catalog.views import index

urlpatterns = [
    path('', index, name='index'),
]

app_name = 'catalog'
