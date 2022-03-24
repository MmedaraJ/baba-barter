from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^$', views.intro, name='intro'),
    url(r'^image/$', views.image, name='image'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^signin/$', views.signin, name='signin'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^home/(?P<id>\d+)$', views.home, name='home'),
    url(r'^compare/(?P<id>\d+)$', views.compare, name='compare'),
    url(r'^category/(?P<id>\w+)$', views.category, name='category'),
    url(r'^user/show/(?P<id>\d+)$', views.show_user, name='show_user'),
    url(r'^process/image/$', views.process_image, name='process_image'),
    url(r'^swappables/(?P<id>\d+)$', views.swappables, name='swappables'),
    url(r'^process/signup/$', views.process_signup, name='process_signup'),
    url(r'^process/signin/$', views.process_signin, name='process_signin'),
    url(r'^privacy-policy/$', views.privacy_policy, name='privacy_policy'),
    url(r'^report/user/(?P<id>\d+)$', views.report_user, name='report_user'),
    url(r'^edit/profile/(?P<id>\d+)$', views.edit_profile, name='edit_profile'),
    url(r'^swappable/show/(?P<id>\d+)$', views.show_swappable, name='show_swappable'),
    url(r'^edit/swappable/(?P<id>\d+)$', views.edit_swappable, name='edit_swappable'),
    url(r'^filter/category/(?P<id>\d+)$', views.filter_category, name='filter_category'),
    url(r'^create/swappable/(?P<id>\d+)$', views.create_swappable, name='create_swappable'),
    url(r'^delete/swappable/(?P<id>\d+)$', views.delete_swappable, name='delete_swappable'),
    url(r'^update/swappable/(?P<id>\d+)$', views.update_swappable, name='update_swappable'),
    url(r'^process/edit/profile/$', views.process_edit_profile, name='process_edit_profile'),
    url(r'^edit/profile/picture/$', views.edit_profile_picture, name='edit_profile_picture'),
    url(r'^filter/swappables/(?P<id>\d+)$', views.filter_swappables, name='filter_swappables'),
    url(r'^register/swappable/(?P<id>\d+)$', views.register_swappable, name='register_swappable'),
    url(r'^process/edit/user/(?P<id>\d+)$', views.process_edit_profile, name='process_edit_profile'),
    url(r'^process/report/user/(?P<id>\d+)$', views.process_report_user, name='process_report_user'),
    url(r'^edit/swappable/delete/images/$', views.delete_swappable_images, name='delete_swappable_images'),
    url(r'^filter/compare/swappables/(?P<id>\d+)$', views.filter_other_swappables, name='filter_other_swappables'),
    url(r'^process/edit/profile/picture/$', views.process_edit_profile_picture, name='process_edit_profile_picture'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', views.activate, name='activate'),
    url(r'^activate_new_email/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', views.activate_new_email, name='activate_new_email'),
]

if settings.DEBUG: 
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)