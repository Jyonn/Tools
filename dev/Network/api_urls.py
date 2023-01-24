from django.urls import path, include

urlpatterns = [
    path('vpnnet/', include('dev.Network.VPNNet.api_urls'))
]
