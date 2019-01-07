from rest_framework.urlpatterns import format_suffix_patterns

from django.conf.urls import include, url
from django.conf import settings

from .views import *

urlpatterns = [
    url(r'^chat', chat, name="chatfunctions"),
    url(r'^trainData/', traininputdata),
    url(r'^processData/', processingdata),
    url(r'^save_ratings/', saveRatings),
    url(r'^download_chat/', chatDownload),
    url(r'^download_logs/', logsDownload),
    url(r'^get_user_ratings', getRatings),
    url(r'^download_training_data/', trainDataDownload),
    url(r'^upload_training_data/', trainDataUpload),
    url(r'^restart_server/', restartserver),
    url(r'^clear_history/', clearhistory),
    #url(r'^getauthor/(?P<u_id>\d{1,3})/$', getAuthor),
    # url(r'^image_resize/$',users.image_resize),

    # url(r'^export_users_xls/', leavereport.export_users_xls),


]
# + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns = format_suffix_patterns(urlpatterns)
