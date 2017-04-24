from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.Login),
    url(r'^login/$', views.Login),
    url(r'^register/$', views.register),
    url(r'^logout/$', views.Logout),
    url(r'^home/$', views.Home),
    url(r'^notifications/$', views.notifications),
    url(r'^clear_notifications/$', views.clear_notifications),
    url(r'^chat/$', views.chat),
    url(r'^clear_chat/(?P<to_user>\w+)$', views.clear_chat),
    url(r'^chat/(?P<to_user>\w+)$', views.chat),
    url(r'^post/$', views.Post, name='post'),
    url(r'^post/(?P<to_user>\w+)$', views.Post, name='post'),
    url(r'^messages/$', views.Messages, name='messages'),
    url(r'^add/$', views.add),
    url(r'^circle/$', views.circle),
    url(r'^chat_circle/$', views.chat_circle),
    url(r'^remove/(?P<username>\w+)$', views.remove),


]
