from django.urls import path

from tunnels.views import (
    TunnelCreateView,
    TunnelDeleteView,
    TunnelDetailView,
    TunnelListView,
    TunnelUpdateView,
)

app_name = "tunnels"

urlpatterns = [
    path("", TunnelListView.as_view(), name="list"),
    path("create/", TunnelCreateView.as_view(), name="create"),
    path("<int:pk>/", TunnelDetailView.as_view(), name="detail"),
    path("<int:pk>/update/", TunnelUpdateView.as_view(), name="update"),
    path("<int:pk>/delete/", TunnelDeleteView.as_view(), name="delete"),
]
