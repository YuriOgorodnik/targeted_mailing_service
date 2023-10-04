from django.contrib.auth.decorators import login_required
from django.urls import path
from django.views.decorators.cache import cache_page

from mailings.apps import MailingsConfig
from mailings.views import (ClientCreateView, ClientUpdateView, ClientListView,
                            ClientDetailView, ClientDeleteView, MailingListCreateView,
                            MailingListListView, MailingListDetailView,
                            MailingLogListView, index, MailingMessageCreateView,
                            MailingMessageUpdateView, MailingMessageDetailView, MailingMessageDeleteView)

app_name = MailingsConfig.name

urlpatterns = [
    path('', index, name='index'),
    path('clients/create/', login_required(ClientCreateView.as_view()), name='clients_create'),
    path('clients/', login_required(ClientListView.as_view()), name='clients_list'),
    path('clients/view/<int:pk>/', login_required(ClientDetailView.as_view()), name='clients_view'),
    path('clients/edit/<int:pk>/', login_required(ClientUpdateView.as_view()), name='clients_edit'),
    path('clients/delete/<int:pk>/', login_required(ClientDeleteView.as_view()), name='clients_delete'),

    path('mailings/create/', login_required(MailingListCreateView.as_view()), name='mailings_create'),
    path('mailings/', login_required(MailingListListView.as_view()), name='mailings_list'),
    path('mailings/view/<int:pk>/', login_required(MailingListDetailView.as_view()), name='mailings_view'),

    path('', MailingLogListView.as_view(), name='list'),
    path('mailings/message_create/<int:mailing_pk>/', login_required(MailingMessageCreateView.as_view()), name='message_create'),
    path('mailings/message_view/<int:pk>/', cache_page(60)(login_required(MailingMessageDetailView.as_view())), name='message_view'),
    path('mailings/message_edit/<int:pk>/', login_required(MailingMessageUpdateView.as_view()), name='message_edit'),
    path('mailings/message_delete/<int:pk>/', login_required(MailingMessageDeleteView.as_view()), name='message_delete'),

]
