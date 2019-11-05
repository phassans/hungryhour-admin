from django.urls import path
from .views import *


urlpatterns = [
    path('', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('business/', BusinessView.as_view(), name='business'),
    path('business/add/', BusinessAddView.as_view(), name='business_add'),
    path('business/edit/<int:id>/', BusinessEditView.as_view(), name='business_edit'),
    path('business/delete/<int:id>', BusinessDeleteView.as_view(), name='business_delete'),
    path('business/<int:id>/listing/', BusinessListingPageView.as_view(), name='business_listing'),
    path('listing/', ListingPageView.as_view(), name='listing'),
    path('listing/add/', ListingAddView.as_view(), name='listing_add'),
    path('listing/all/', BusinessListingAjaxView.as_view(), name='listing_all'),
    path('listing/edit/<int:id>/', BusinessListingEditView.as_view(), name='listing_edit'),
    path('listing/delete/<int:id>', BusinessListingDeleteView.as_view(), name='listing_delete'),

]
