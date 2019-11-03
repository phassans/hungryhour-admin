from django.urls import path
from .views import *


urlpatterns = [
    path('', IndexPageView.as_view(), name='index'),
    path('register/', RegisterView.as_view(), name='register'),
    path('business', BusinessPageView.as_view(), name='business'),
    path('business/add', AddBusinessPageView.as_view(), name='addbusiness'),
    path('business/insert', InsertBusiness, name='insertbusiness'),
    path('business/edit/<int:id>', BusinessEditView.as_view(), name='editbusiness'),
    path('business/delete/<int:id>', BusinessDeleteView.as_view(), name='business_delete'),

    path('listing', ListingPageView.as_view(), name='listing'),
    path('business/<int:id>/listing/', BusinessListingPageView.as_view(), name='business_listing'),
    path('listing/add', AddListingPageView.as_view(), name='addbusiness'),
    path('listing/insert', InsertListing, name='insertlisting'),
    path('listing/all', BusinessListingAjaxView.as_view(), name='listing_all'),
    path('listing/edit/<int:id>', BusinessListingEditView.as_view(), name='listing_edit'),
    path('listing/delete/<int:id>', BusinessListingDeleteView.as_view(), name='listing_delete'),

    path('language/', ChangeLanguageView.as_view(), name='change_language'),
]
