from django.urls import path
from .views import *

urlpatterns = [
	path("tourinquiryhasplace/create", create_tourinquiryhasplace),
	path("tourinquiryhasplace/get", get_tourinquiryhasplace),
	path("tourinquiryhasplace/update", update_tourinquiryhasplace),
	path("tourinquiryhasplace/delete", delete_tourinquiryhasplace),
	path("message/create", create_message),
	path("messages/get", get_message),
	path("message/update", update_message),
	path("message/delete", delete_message),
    path("waiting-list", get_waiting_list),
    path("accept-request", accept_request),
    path("list", get_contact_list),
    path("init", init_chat),
]