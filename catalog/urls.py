from django.urls import path, include

from catalog.views import index, TopicListView, NewspaperListView, NewspaperDetailView, RedactorListView, \
    RedactorDetailView, TopicCreateView, TopicUpdateView, TopicDeleteView

urlpatterns = [
    path('', index, name='index'),
    path('topics/', TopicListView.as_view(), name='topic-list'),
    path('topics/create/', TopicCreateView.as_view(), name='topic-create'),
    path('topics/<int:pk>/update/', TopicUpdateView.as_view(), name='topic-update'),
    path('topics/<int:pk>/delete/', TopicDeleteView.as_view(), name='topic-delete'),
    path('newspapers/', NewspaperListView.as_view(), name='newspaper-list'),
    path('newspapers/<int:pk>/', NewspaperDetailView.as_view(), name='newspaper-detail'),
    path('redactors/', RedactorListView.as_view(), name='redactor-list'),
    path('redactors/<int:pk>/', RedactorDetailView.as_view(), name='redactor-detail'),
]

app_name = 'catalog'
