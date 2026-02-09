from django.urls import path
from tunnels.views import TunnelListView
from tunnels.views import TunnelDetailView
from tunnels.views import TunnelCreateView
from tunnels.views import TunnelUpdateView
from tunnels.views import TunnelDeleteView

app_name = 'tunnels'

urlpatterns = [
    path('', TunnelListView.as_view(), name='list'),
    path('create/', TunnelCreateView.as_view(), name='create'),
    path('<int:pk>/', TunnelDetailView.as_view(), name='detail'),
    path('<int:pk>/update/', TunnelUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', TunnelDeleteView.as_view(), name='delete'),
]
