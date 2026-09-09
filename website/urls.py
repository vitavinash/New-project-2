from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("thanks/", views.thanks, name="thanks"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("workspace/", views.workspace, name="workspace"),
    path("workspace/actions/<int:pk>/status/", views.update_action, name="update_action"),
]
