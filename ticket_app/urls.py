from . import views
from django.urls import path

urlpatterns = [
    path("view_tickets", views.TicketsView.as_view()),
    path("ticket_create", views.TicketCreateView.as_view()),
    path("ticket_retrieve/<int:pk>", views.TicketDetailView.as_view()),
    path("ticket_update/<int:pk>", views.TicketDeleteView.as_view()),
    path("ticket_delete/<int:pk>", views.TicketDeleteView.as_view()),
    path("filter", views.TicketFilteringView.as_view()),
    path("ticket_purchase/<int:pk>", views.TicketPurchaseView.as_view()),
]
