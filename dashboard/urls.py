from django.urls import path

from .views import AdminPanelView, DashboardView

urlpatterns = [
    path("", DashboardView.as_view(), name="dashboard"),
    path("home/", DashboardView.as_view(), name="dashboard_home"),
    path("admin-panel/", AdminPanelView.as_view(), name="admin_panel"),
]