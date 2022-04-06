from django.urls import re_path, path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    re_path(r'^$', views.intro, name='intro'),
    re_path(r'^image/$', views.image, name='image'),
    re_path(r'^index/$', views.index, name='index'),
    re_path(r'^signup/$', views.signup, name='signup'),
    re_path(r'^signin/$', views.signin, name='signin'),
    re_path(r'^logout/$', views.logout, name='logout'),
    re_path(r'^chat/$', views.chat_room, name='chat_room'),
    re_path(r'^home/(?P<id>\d+)$', views.home, name='home'),
    re_path(r'^chat/(?P<room_name>\w+)/$', views.room, name='room'),
    re_path(r'^compare/(?P<id>\d+)$', views.compare, name='compare'),
    re_path(r'^category/(?P<id>\d+)$', views.category, name='category'),
    re_path(r'^user/show/(?P<id>\d+)$', views.show_user, name='show_user'),
    re_path(r'^process/image/$', views.process_image, name='process_image'),
    re_path(r'^swappables/(?P<id>\d+)$', views.swappables, name='swappables'),
    re_path(r'^process/signup/$', views.process_signup, name='process_signup'),
    re_path(r'^process/signin/$', views.process_signin, name='process_signin'),
    re_path(r'^privacy-policy/$', views.privacy_policy, name='privacy_policy'),
    re_path(r'^report/user/(?P<id>\d+)$', views.report_user, name='report_user'),
    re_path(r'^edit/profile/(?P<id>\d+)$', views.edit_profile, name='edit_profile'),
    re_path(r'^swappable/show/(?P<id>\d+)$', views.show_swappable, name='show_swappable'),
    re_path(r'^edit/swappable/(?P<id>\d+)$', views.edit_swappable, name='edit_swappable'),
    re_path(r'^filter/category/(?P<id>\d+)$', views.filter_category, name='filter_category'),
    re_path(r'^report/swappable/(?P<id>\d+)$', views.report_swappable, name='report_swappable'),
    re_path(r'^create/swappable/(?P<id>\d+)$', views.create_swappable, name='create_swappable'),
    re_path(r'^delete/swappable/(?P<id>\d+)$', views.delete_swappable, name='delete_swappable'),
    re_path(r'^update/swappable/(?P<id>\d+)$', views.update_swappable, name='update_swappable'),
    re_path(r'^process/edit/profile/$', views.process_edit_profile, name='process_edit_profile'),
    re_path(r'^edit/profile/picture/$', views.edit_profile_picture, name='edit_profile_picture'),
    re_path(r'^filter/swappables/(?P<id>\d+)$', views.filter_swappables, name='filter_swappables'),
    re_path(r'^register/swappable/(?P<id>\d+)$', views.register_swappable, name='register_swappable'),
    re_path(r'^process/edit/user/(?P<id>\d+)$', views.process_edit_profile, name='process_edit_profile'),
    re_path(r'^process/report/user/(?P<id>\d+)$', views.process_report_user, name='process_report_user'),
    re_path(r'^edit/swappable/delete/images/$', views.delete_swappable_images, name='delete_swappable_images'),
    re_path(r'^filter/compare/swappables/(?P<id>\d+)$', views.filter_other_swappables, name='filter_other_swappables'),
    re_path(r'^process/report/swappable/(?P<id>\d+)$', views.process_report_swappable, name='process_report_swappable'),
    re_path(r'^process/edit/profile/picture/$', views.process_edit_profile_picture, name='process_edit_profile_picture'),
    path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', views.activate, name='activate'),
    path(r'^activate_new_email/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', views.activate_new_email, name='activate_new_email'),
]

if settings.DEBUG: 
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)