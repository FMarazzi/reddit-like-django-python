from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('create_user', views.create_user, name='create_user'),
    path('delete_user', views.delete_user, name='delete_user'),
    path('create_discussion', views.create_discussion, name='create_discussion'),
    path('remove_discussion', views.remove_discussion, name='remove_discussion'),
    path('create_post', views.create_post, name='create_post'),
    path('remove_post', views.remove_post, name='remove_post'),
    path('vote', views.vote, name='vote'),
    path('number_of_messages', views.number_of_messages, name='number_of_messages'),
    path('number_of_partecipants', views.number_of_partecipants, name='number_of_partecipants'),
    path('add_contributor', views.add_contributor, name='add_contributor'),
]