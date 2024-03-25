"""
URL configuration for CallTranscript project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
#import notifications.urls
#from admin_notification.views import check_notification_view
# CallTranscript/urls.py

from django.contrib import admin
from django.contrib.auth.views import LoginView
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path, include, re_path
from calls.admin import myadmin

#from admin2 import myadmin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('grappelli/', include('grappelli.urls')), # grappelli URLS
    path('calls/', include('calls.urls')),  # Include calls app URLs

    path('login', LoginView.as_view()),
    #path('check/notification', check_notification_view, name="check_notifications"),
    #path('^inbox/notifications/', include(notifications.urls, namespace='notifications')),
    path('',myadmin.urls),
]
urlpatterns += staticfiles_urlpatterns()