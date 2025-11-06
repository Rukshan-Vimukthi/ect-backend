from django.urls import path
from .views import *

urlpatterns = [
	path("currency/create", create_currency),
	path("currency/get", get_currency),
	path("currency/update", update_currency),
	path("currency/delete", delete_currency),
	path("create", create_place),
	path("get", get_place),
	path("update", update_place),
	path("delete", delete_place),
    path("types/get", get_place_types),
]