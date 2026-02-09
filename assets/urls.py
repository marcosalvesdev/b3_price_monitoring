from django.urls import path

from assets.views import AssetListView
from assets.views import AssetDetailView
from assets.views import AssetCreateView
from assets.views import AssetUpdateView
from assets.views import AssetDeleteView

app_name = 'assets'

urlpatterns = [
    path('', AssetListView.as_view(), name='list'),
    path('<int:pk>/', AssetDetailView.as_view(), name='detail'),
    path('create/', AssetCreateView.as_view(), name='create'),
    path('<int:pk>/update/', AssetUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', AssetDeleteView.as_view(), name='delete'),
]
