from django.contrib import admin
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy

from django.contrib.admin.sites import AdminSite

admin.site.disable_action('delete_selected')

class MyAdminSite(AdminSite):
    # Text to put at the end of each page's <title>.
    site_title = gettext_lazy('Call Transcript Analysis Tool')

    # Text to put in each page's <h1>.
    site_header = gettext_lazy('Call Transcript Analysis Tool')

    # Text to put at the top of the admin index page.
    index_title = gettext_lazy('Call Transcript Analysis Tool')
    login_form = AuthenticationForm
    def has_permission(self, request):
        """
        Return True if the given HttpRequest has permission to view
        *at least one* page in the admin site.
        """
        #return True
        return request.user.is_active
    #or overwrite some methods for different functionality

myadmin = MyAdminSite(name="myadmin")


