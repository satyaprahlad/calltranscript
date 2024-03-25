from datetime import date, timedelta
from typing import List

from csvexport.actions import csvexport
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin


from django.contrib.admin.sites import AdminSite
from django.contrib.auth.forms import AuthenticationForm
from django.db.models import Model
from django.http import QueryDict, HttpResponseBadRequest, JsonResponse, HttpResponse
from django.urls import reverse, URLPattern
from django.utils.translation import gettext_lazy
from search_admin_autocomplete_.admin import SearchAutoCompleteAdmin_

try:
    from django.conf.urls import url
except ImportError:
    from django.urls import path
    url = path
#from admin2 import myadmin, MyAdminSite

from django import forms
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.contrib.auth.models import Group, User
from django_admin_search.admin import AdvancedSearchAdmin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from admin2 import MyAdminSite, myadmin
#from search_admin_autocomplete_.admin import SearchAutoCompleteAdmin

from calls.forms import ProductAdvancedSearch, CallDetailsAdvancedSearch
from calls.models import Product, Country, CallDetails
from functools import reduce
from operator import or_
from typing import List


from django.contrib import admin
from django.db.models import Q, Model
from django.http import HttpRequest
from django.urls.resolvers import URLPattern

from admin2 import myadmin

try:
    from django.urls import reverse
except ImportError:
    from django.core.urlresolvers import reverse  # type: ignore

#
# class MyAdminSite(AdminSite):
#     # Text to put at the end of each page's <title>.
#     site_title = gettext_lazy('Product site admin')
#
#     # Text to put in each page's <h1>.
#     site_header = gettext_lazy('Product administration for Non Staff users')
#
#     # Text to put at the top of the admin index page.
#     index_title = gettext_lazy('Master Data administration')
#     login_form = AuthenticationForm
#     index_template='myadmin/index.html'
#     def has_permission(self, request):
#         """
#         Return True if the given HttpRequest has permission to view
#         *at least one* page in the admin site.
#         """
#         return request.user.is_active
#     #or overwrite some methods for different functionality


#User = get_user_model()

# Create ModelForm based on the Group model.

class GroupAdminForm(forms.ModelForm):
    class Meta:
        model = Group
        exclude = []

    # Add the users field.
    users = forms.ModelMultipleChoiceField(
         queryset=User.objects.filter(is_staff=False),
         required=False,
         # Use the pretty 'filter_horizontal widget'.
         widget=FilteredSelectMultiple('users', False)
    )

    def __init__(self, *args, **kwargs):
        # Do the normal form initialisation.
        super(GroupAdminForm, self).__init__(*args, **kwargs)
        # If it is an existing group (saved objects have a pk).
        if self.instance.pk:
            # Populate the users field with the current Group users.
            self.fields['users'].initial = self.instance.user_set.all()

    def save_m2m(self):
        # Add the users to the Group.
        self.instance.user_set.set(self.cleaned_data['users'])

    def save(self, *args, **kwargs):
        # Default save
        instance = super(GroupAdminForm, self).save()
        # Save many-to-many data
        self.save_m2m()
        return instance

# Unregister the original Group admin.
admin.site.unregister(Group)

# Create a new Group admin.

class GroupAdmin(admin.ModelAdmin):
    # Use our custom form.
    form = GroupAdminForm
    # Filter permissions horizontal as well.
    filter_horizontal = ['permissions']

# Register the new Group ModelAdmin.
admin.site.register(Group, GroupAdmin)


class ProductResource(resources.ModelResource):
    class Meta:
        model = Product
        fields = ['name', 'description']

class CallResource(resources.ModelResource):
    class Meta:
        model = Product
        fields = ['customer_id', 'call_type']

# class SearchAutoCompleteAdmin(admin.ModelAdmin):
#     """
#     Basic admin class that allows to enable search autocomplete for certain model.
#
#     Usage:
#
#     .. code-block:: python
#
#         class MyModelAdmin(SearchAutoCompleteAdmin)
#             search_fields = ['search_field', ]
#
#         admin.site.register(MyModel, MyModelAdmin)
#     """
#     #change_list_template = 'admin/change_list.html'
#     search_fields = []  # type: List[str]
#     search_prefix = '__contains'
#     max_results = 10
#
#     def get_urls(self) -> List[URLPattern]:
#         urls = super(SearchAutoCompleteAdmin, self).get_urls()
#         api_urls = [url(r'search/<str:search_term>', self.search_api)]
#         return api_urls + urls
#
#     def my_search(self, request):
#         return self.changelist_view(request, None)
#
#
#     def search_api(self, request: HttpRequest, search_term: str) -> HttpResponse:
#         """
#         API view that perform search by search term for current model.
#         """
#         if len(self.search_fields) == 0:
#             return HttpResponseBadRequest(reason='Mo search_fields defined in {}'.format(self.__class__.__name__))
#
#         query = [Q(**{'{}{}'.format(field, self.search_prefix): search_term}) for field in self.search_fields]
#         # https://github.com/python/mypy/issues/4150
#         query = reduce(or_, query)  # type: ignore
#         return JsonResponse(data=[{'keyword': self.get_instance_name(item), 'url': self.get_instance_url(item)}
#                                   for item in self.model.objects.filter(query)[0:self.max_results]], safe=False)
#
#     def get_instance_name(self, instance: Model) -> str:
#         """
#         Format instance name based on value of search fields.
#         """
#         values = []
#
#         for field in self.search_fields:
#             value = getattr(instance, field)
#             if not value:
#                 continue
#             values.append(str(value))
#
#         if not values:
#             return ""
#
#         return ", ".join(values)
#
#     def get_instance_url(self, instance: Model) -> str:
#         """
#         Returns url admin change view for model instance.
#         """
#         url_name = "{}:{}_{}_change".format(self.admin_site.name,self.model._meta.app_label, str(self.model.__name__).lower())
#         return reverse(url_name, args=(instance.pk,))
#


class ProductAdmin(AdvancedSearchAdmin, ImportExportModelAdmin ):

    list_display = ('name', 'description', 'created_at', 'country')
    search_fields = ('name', 'description')
    search_help_text = 'Search me'
    search_form = ProductAdvancedSearch
    readonly_fields = ('name', 'description', 'created_at', 'country')
    save_as_continue = False
    save_on_top = False

    def has_change_permission(self, request, obj=None):
        return False

    # Disable deletion functionality
    def has_delete_permission(self, request, obj=None):
        return False

    actions = [csvexport]
    CSV_EXPORT_FORMAT_FORM = False
    csvexport_export_fields = [
        'name',
        'description',
        'country.name'
    ]

    def render_change_form(
        self, request, context, add=False, change=False, form_url="", obj=None
    ):
        extra_context = {'is_popup':1}
        context.update(extra_context)
        return super(ProductAdmin, self).render_change_form(request, context, add=add, change=change, form_url=form_url, obj=obj)

    class Meta:
        fields = '__all__'
    change_list_template = 'myadmin/change_list.html'
    change_form_template = 'myadmin/change_form.html'
    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['show_save_and_continue'] = True  # Hide "Save and continue editing" button
        return super().change_view(request, object_id, form_url=form_url, extra_context=extra_context)

    def get_queryset(self, request):
        params = request.GET.copy()
        if 'date_filter' in params:
            date_filter = request.GET['date_filter']

            # Determine the date range based on the selected option
            if date_filter == '10':
                # Calculate the date 10 days ago
                filter_date = date.today() - timedelta(days=100)
            elif date_filter == '30':
                # Calculate the date 30 days ago
                filter_date = date.today() - timedelta(days=200)
            else:
                # Default case: show all records
                filter_date = None

            # Perform filtering based on the selected date range
            if filter_date:
                queryset = self.model.objects.filter(created_at__gte=filter_date)
                params['created_at__gte'] = filter_date
            else:
                queryset = self.model.objects.all()
            del params['date_filter']  # Delete the parameter from the copy


        # Create a new QueryDict without the 'date_filter' parameter
        new_get_params = QueryDict(params.urlencode(), mutable=True)

        # Assign the modified QueryDict to the request.GET attribute (as it's immutable, you need to replace it)
        request.GET = new_get_params
        return super().get_queryset(request)

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['is_good'] = True
        params = request.GET.copy()
        queryset= None

        # Remove the 'date_filter' parameter if it exists
        if 'date_filter' in params:
            date_filter = request.GET['date_filter']
            extra_context['date_filter'] = date_filter

            # Determine the date range based on the selected option
            if date_filter == '10':
                # Calculate the date 10 days ago
                filter_date = date.today() - timedelta(days=100)
            elif date_filter == '30':
                # Calculate the date 30 days ago
                filter_date = date.today() - timedelta(days=200)
            else:
                # Default case: show all records
                filter_date = None

            # Perform filtering based on the selected date range
            if filter_date:
                queryset = self.model.objects.filter(created_at__gte=filter_date)
                params['created_at__gte'] = filter_date
            else:
                queryset = self.model.objects.all()
            del params['date_filter']  # Delete the parameter from the copy


        # Create a new QueryDict without the 'date_filter' parameter
        new_get_params = QueryDict(params.urlencode(), mutable=True)

        # Assign the modified QueryDict to the request.GET attribute (as it's immutable, you need to replace it)
        request.GET = new_get_params
        return super().changelist_view(request, extra_context=extra_context)


class CallDetailsAdmin(AdvancedSearchAdmin, ImportExportModelAdmin, SearchAutoCompleteAdmin_):

    list_display = ('customer_id', 'call_type')
    search_fields = ('customer_id', 'call_type')
    search_help_text = ''
    search_form = CallDetailsAdvancedSearch
    readonly_fields = ('customer_id', 'call_type')
    save_as_continue = False
    save_on_top = False

    def has_change_permission(self, request, obj=None):
        return False

    # Disable deletion functionality
    # def has_delete_permission(self, request, obj=None):
    #     return False

    actions = [csvexport]
    CSV_EXPORT_FORMAT_FORM = False
    csvexport_export_fields = [
        'customer_id', 'call_type'

    ]

    def render_change_form(
        self, request, context, add=False, change=False, form_url="", obj=None
    ):
        extra_context = {'is_popup':1}
        context.update(extra_context)
        return super(CallDetailsAdmin, self).render_change_form(request, context, add=add, change=change, form_url=form_url, obj=obj)

    class Meta:
        fields = '__all__'
    change_list_template = 'myadmin/change_list.html'

    change_form_template = 'myadmin/change_form.html'
    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['show_save_and_continue'] = True  # Hide "Save and continue editing" button
        return super().change_view(request, object_id, form_url=form_url, extra_context=extra_context)

    def get_queryset(self, request):
        params = request.GET.copy()
        if 'date_filter' in params:
            date_filter = request.GET['date_filter']

            # Determine the date range based on the selected option
            if date_filter == '10':
                # Calculate the date 10 days ago
                filter_date = date.today() - timedelta(days=100)
            elif date_filter == '30':
                # Calculate the date 30 days ago
                filter_date = date.today() - timedelta(days=200)
            else:
                # Default case: show all records
                filter_date = None

            # Perform filtering based on the selected date range
            if filter_date:
                queryset = self.model.objects.filter(created_at__gte=filter_date)
                params['created_at__gte'] = filter_date
            else:
                queryset = self.model.objects.all()
            del params['date_filter']  # Delete the parameter from the copy


        # Create a new QueryDict without the 'date_filter' parameter
        new_get_params = QueryDict(params.urlencode(), mutable=True)

        # Assign the modified QueryDict to the request.GET attribute (as it's immutable, you need to replace it)
        request.GET = new_get_params
        return super().get_queryset(request)

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['is_good'] = True
        params = request.GET.copy()
        queryset= None

        # Remove the 'date_filter' parameter if it exists
        if 'date_filter' in params:
            date_filter = request.GET['date_filter']
            extra_context['date_filter'] = date_filter

            # Determine the date range based on the selected option
            if date_filter == '10':
                # Calculate the date 10 days ago
                filter_date = date.today() - timedelta(days=100)
            elif date_filter == '30':
                # Calculate the date 30 days ago
                filter_date = date.today() - timedelta(days=200)
            else:
                # Default case: show all records
                filter_date = None

            # Perform filtering based on the selected date range
            if filter_date:
                queryset = self.model.objects.filter(created_at__gte=filter_date)
                params['created_at__gte'] = filter_date
            else:
                queryset = self.model.objects.all()
            del params['date_filter']  # Delete the parameter from the copy


        # Create a new QueryDict without the 'date_filter' parameter
        new_get_params = QueryDict(params.urlencode(), mutable=True)

        # Assign the modified QueryDict to the request.GET attribute (as it's immutable, you need to replace it)
        request.GET = new_get_params
        return super().changelist_view(request, extra_context=extra_context)



#myadmin.template_path = 'myadmin'
#myadmin.register([Product], ProductAdmin)
myadmin.register([CallDetails], CallDetailsAdmin)
#myadmin.register(Country)
#admin.site.register([Product])

#admin.site.disable_action('delete_selected')
