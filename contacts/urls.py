from django.urls import path
from .views import ContactCreateView, ContactDetailView, get_contacts_view

urlpatterns = [
    path('contacts/all', get_contacts_view, name='contact-list'),
    path('contacts/', ContactCreateView.as_view(), name='contact-create'),
    path('contacts/<int:pk>/', ContactDetailView.as_view(), name='contact-detail'),
]
