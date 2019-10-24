from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static

from main.views import *

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', IndexPageView.as_view(), name='index'),
    path('business', BusinessPageView.as_view(), name='business'),
    path('business/add', AddBusinessPageView.as_view(), name='addbusiness'),
    path('business/insert', InsertBusiness, name='insertbusiness'),
    path('business/edit/<id>', EditBusinessPageView.as_view(), name='editbusiness'),
    path('business/delete/<id>',
         DeleteBusinessPageView.as_view(), name='deletebusiness'),

    path('listing', ListingPageView.as_view(), name='listing'),
    path('listing/add', AddListingPageView.as_view(), name='addbusiness'),
    path('listing/insert', InsertListing, name='insertlisting'),

    path('i18n/', include('django.conf.urls.i18n')),
    path('language/', ChangeLanguageView.as_view(), name='change_language'),

    path('accounts/', include('accounts.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
