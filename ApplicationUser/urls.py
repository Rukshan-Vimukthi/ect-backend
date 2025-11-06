from django.urls import path
from .views import *

urlpatterns = [
    path("signup", signup),
    path("sign_in", sign_in),
    path("admin/signin", admin_sign_in),
	path("tourinquiry/create", create_tourinquiry),
	path("tourinquiries/get", get_tourinquiries),
	path("tourinquiry/get", get_tourinquiry),
	path("tourinquiry/update", update_tourinquiry),
	path("tourinquiry/delete", delete_tourinquiry),
	path("tourinquiryhasagecategory/create", create_tourinquiryhasagecategory),
	path("tourinquiryhasagecategory/get", get_tourinquiryhasagecategory),
	path("tourinquiryhasagecategory/update", update_tourinquiryhasagecategory),
	path("tourinquiryhasagecategory/delete", delete_tourinquiryhasagecategory),
    path("tourpackage/create", create_new_tourpackage),
    path("tourpackages/get", get_tourpackages),
    path("tourpackage/edit", edit_tourpackage)
]