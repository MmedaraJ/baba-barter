from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^$', views.intro, name='intro'),
    url(r'^image/$', views.image, name='image'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^signin/$', views.signin, name='signin'),
    url(r'^home/(?P<id>\d+)$', views.home, name='home'),
    url(r'^user/show/(?P<id>\d+)$', views.show_user, name='show_user'),
    url(r'^process/image/$', views.process_image, name='process_image'),
    url(r'^swappables/(?P<id>\d+)$', views.swappables, name='swappables'),
    url(r'^process/signup/$', views.process_signup, name='process_signup'),
    url(r'^process/signin/$', views.process_signin, name='process_signin'),
    url(r'^privacy-policy/$', views.privacy_policy, name='privacy_policy'),
    url(r'^edit/profile/(?P<id>\d+)$', views.edit_profile, name='edit_profile'),
    url(r'^swappable/show/(?P<id>\d+)$', views.show_swappable, name='show_swappable'),
    url(r'^edit/swappable/(?P<id>\d+)$', views.edit_swappable, name='edit_swappable'),
    url(r'^create/swappable/(?P<id>\d+)$', views.create_swappable, name='create_swappable'),
    url(r'^update/swappable/(?P<id>\d+)$', views.update_swappable, name='update_swappable'),
    url(r'^register/swappable/(?P<id>\d+)$', views.register_swappable, name='register_swappable'),
]

if settings.DEBUG: 
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)