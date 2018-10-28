from django.conf.urls import patterns, url
from views import RegistrarUsuarioView

urlpatterns = pattern('',
	url(r'^registrar/$',RegistrarUsuarioView.as_view(), name="registrar")
)
