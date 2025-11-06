from django.shortcuts import render

from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import TourType
from .models import AgeCategory
from .models import TransportType
from .models import AvailableLanguage
from .models import HotelCategory
from .models import RoomType
from .models import MealPlan
from .models import Accommodation
from .models import Currency


# Create your views here.

@api_view(["POST"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def create_message(request):
	response = {"status": "failed", "message": ""}


	data = request["data"]

	TourType = TourType.objects.create(
			)

	if TourType is not None:
		response["status"] = "ok"


	return Response(response)

@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_message(request):
	response = {"status": "failed", "message": ""}



	data = request["data"]
	id = data["id"]
	tourtype = TourType.objects.get(id=id)
	response["id"] = tourtype.id
	response["type"] = tourtype.type


	return Response(response)

@api_view(["POST"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def update_message(request):
	response = {"status": "failed", "message": ""}


	data = request["data"]
	id = data["id"]

	try:
		tourtype = TourType.objects.get(id=id)
		tourtype.id = data["id"]
		tourtype.type = data["type"]
		tourtype.save()
		response["status"] = "ok"
	except:
		pass

	return Response(response)

@api_view(["POST"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def delete_message(request):
	response = {"status": "failed", "message": ""}


	data = request.data
	id = data["id"]
	try:
		tourtype = TourType.objects.get(id=id)

		if tourtype is not None:
			tourtype.delete()
			response["status"] = "ok"
	except:
		pass


	return Response(response)

@api_view(["POST"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def create_agecategory(request):
	response = {"status": "failed", "message": ""}


	data = request["data"]

	AgeCategory = AgeCategory.objects.create(
			)

	if AgeCategory is not None:
		response["status"] = "ok"


	return Response(response)

@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_agecategory(request):
	response = {"status": "failed", "message": ""}

	data = request.GET
	try:
		id = data["id"]
		agecategory = AgeCategory.objects.get(id=id)
		response["id"] = agecategory.id
		response["category"] = agecategory.category
		response["min_age"] = agecategory.min_age
		response["max_age"] = agecategory.max_age
		response["status"] = "ok"
	except Exception as e:
		# print(e)
		ageCategories = []
		for ageCategory in AgeCategory.objects.all():
			ageCategories.append({
				"id": ageCategory.id,
				"category": ageCategory.category,
				"min_age": ageCategory.min_age,
                "max_age": ageCategory.max_age,
                "price": ageCategory.price
			})
		
		response["status"] = "ok"
		response["ageCategories"] = ageCategories


	return Response(response)

@api_view(["POST"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def update_agecategory(request):
	response = {"status": "failed", "message": ""}


	data = request["data"]
	id = data["id"]

	try:
		agecategory = AgeCategory.objects.get(id=id)
		agecategory.id = data["id"]
		agecategory.category = data["category"]
		agecategory.min_age = data["min_age"]
		agecategory.max_age = data["max_age"]
		agecategory.save()
		response["status"] = "ok"
	except:
		pass

	return Response(response)

@api_view(["POST"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def delete_agecategory(request):
	response = {"status": "failed", "message": ""}


	data = request.data
	id = data["id"]
	try:
		agecategory = AgeCategory.objects.get(id=id)

		if agecategory is not None:
			agecategory.delete()
			response["status"] = "ok"
	except:
		pass


	return Response(response)

@api_view(["POST"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def create_transporttype(request):
	response = {"status": "failed", "message": ""}


	data = request["data"]

	TransportType = TransportType.objects.create(
			)

	if TransportType is not None:
		response["status"] = "ok"


	return Response(response)

@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_transporttype(request):
	response = {"status": "failed", "message": ""}

	data = request.GET
	try:
		id = data["id"]
		transporttype = TransportType.objects.get(id=id)
		response["id"] = transporttype.id
		response["type"] = transporttype.type
		response["status"] = "ok"
	except Exception as e:
		# print(e)
		transportTypes = []
		for transportType in TransportType.objects.all():
			transportTypes.append({
				"id": transportType.id,
				"type": transportType.type
			})
		response["transportTypes"] = transportTypes
		response["status"] = "ok"

	return Response(response)

@api_view(["POST"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def update_transporttype(request):
	response = {"status": "failed", "message": ""}


	data = request["data"]
	id = data["id"]

	try:
		transporttype = TransportType.objects.get(id=id)
		transporttype.id = data["id"]
		transporttype.type = data["type"]
		transporttype.save()
		response["status"] = "ok"
	except:
		pass

	return Response(response)

@api_view(["POST"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def delete_transporttype(request):
	response = {"status": "failed", "message": ""}


	data = request.data
	id = data["id"]
	try:
		transporttype = TransportType.objects.get(id=id)

		if transporttype is not None:
			transporttype.delete()
			response["status"] = "ok"
	except:
		pass


	return Response(response)

@api_view(["POST"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def create_availablelanguage(request):
	response = {"status": "failed", "message": ""}


	data = request["data"]

	AvailableLanguage = AvailableLanguage.objects.create(
			)

	if AvailableLanguage is not None:
		response["status"] = "ok"


	return Response(response)

@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_availablelanguage(request):
	response = {"status": "failed", "message": ""}

	data = request.GET
	try:
		id = data["id"]
		availablelanguage = AvailableLanguage.objects.get(id=id)
		response["id"] = availablelanguage.id
		response["language"] = availablelanguage.language
		response["status"] = "ok"
	except Exception as e:
		# print(e)
		languages = []
		for language in AvailableLanguage.objects.all():
			languages.append({
				"id": language.id,
				"language": language.language
			})
		response["languages"] = languages
		response["status"] = "ok"


	return Response(response)

@api_view(["POST"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def update_availablelanguage(request):
	response = {"status": "failed", "message": ""}


	data = request["data"]
	id = data["id"]

	try:
		availablelanguage = AvailableLanguage.objects.get(id=id)
		availablelanguage.id = data["id"]
		availablelanguage.language = data["language"]
		availablelanguage.save()
		response["status"] = "ok"
	except Exception as e:
		print(e)

	return Response(response)

@api_view(["POST"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def delete_availablelanguage(request):
	response = {"status": "failed", "message": ""}


	data = request.data
	id = data["id"]
	try:
		availablelanguage = AvailableLanguage.objects.get(id=id)

		if availablelanguage is not None:
			availablelanguage.delete()
			response["status"] = "ok"
	except:
		pass


	return Response(response)

@api_view(["POST"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def create_hotelcategory(request):
	response = {"status": "failed", "message": ""}


	data = request["data"]

	HotelCategory = HotelCategory.objects.create(
			)

	if HotelCategory is not None:
		response["status"] = "ok"


	return Response(response)

@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_hotelcategory(request):
	response = {"status": "failed", "message": ""}



	data = request["data"]
	id = data["id"]
	hotelcategory = HotelCategory.objects.get(id=id)
	response["id"] = hotelcategory.id
	response["star_rating"] = hotelcategory.star_rating
	response["category"] = hotelcategory.category


	return Response(response)

@api_view(["POST"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def update_hotelcategory(request):
	response = {"status": "failed", "message": ""}


	data = request["data"]
	id = data["id"]

	try:
		hotelcategory = HotelCategory.objects.get(id=id)
		hotelcategory.id = data["id"]
		hotelcategory.star_rating = data["star_rating"]
		hotelcategory.category = data["category"]
		hotelcategory.save()
		response["status"] = "ok"
	except:
		pass

	return Response(response)

@api_view(["POST"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def delete_hotelcategory(request):
	response = {"status": "failed", "message": ""}


	data = request.data
	id = data["id"]
	try:
		hotelcategory = HotelCategory.objects.get(id=id)

		if hotelcategory is not None:
			hotelcategory.delete()
			response["status"] = "ok"
	except:
		pass


	return Response(response)

@api_view(["POST"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def create_roomtype(request):
	response = {"status": "failed", "message": ""}


	data = request["data"]

	RoomType = RoomType.objects.create(
			)

	if RoomType is not None:
		response["status"] = "ok"


	return Response(response)

@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_roomtype(request):
	response = {"status": "failed", "message": ""}



	data = request["data"]
	id = data["id"]
	roomtype = RoomType.objects.get(id=id)
	response["id"] = roomtype.id
	response["room_type"] = roomtype.room_type


	return Response(response)

@api_view(["POST"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def update_roomtype(request):
	response = {"status": "failed", "message": ""}


	data = request["data"]
	id = data["id"]

	try:
		roomtype = RoomType.objects.get(id=id)
		roomtype.id = data["id"]
		roomtype.room_type = data["room_type"]
		roomtype.save()
		response["status"] = "ok"
	except:
		pass

	return Response(response)

@api_view(["POST"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def delete_roomtype(request):
	response = {"status": "failed", "message": ""}


	data = request.data
	id = data["id"]
	try:
		roomtype = RoomType.objects.get(id=id)

		if roomtype is not None:
			roomtype.delete()
			response["status"] = "ok"
	except:
		pass


	return Response(response)

@api_view(["POST"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def create_mealplan(request):
	response = {"status": "failed", "message": ""}


	data = request["data"]

	MealPlan = MealPlan.objects.create(
			)

	if MealPlan is not None:
		response["status"] = "ok"


	return Response(response)

@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_mealplan(request):
	response = {"status": "failed", "message": ""}



	data = request["data"]
	id = data["id"]
	mealplan = MealPlan.objects.get(id=id)
	response["id"] = mealplan.id
	response["meal_plan"] = mealplan.meal_plan


	return Response(response)

@api_view(["POST"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def update_mealplan(request):
	response = {"status": "failed", "message": ""}


	data = request["data"]
	id = data["id"]

	try:
		mealplan = MealPlan.objects.get(id=id)
		mealplan.id = data["id"]
		mealplan.meal_plan = data["meal_plan"]
		mealplan.save()
		response["status"] = "ok"
	except:
		pass

	return Response(response)

@api_view(["POST"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def delete_mealplan(request):
	response = {"status": "failed", "message": ""}


	data = request.data
	id = data["id"]
	try:
		mealplan = MealPlan.objects.get(id=id)

		if mealplan is not None:
			mealplan.delete()
			response["status"] = "ok"
	except:
		pass


	return Response(response)

@api_view(["POST"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def create_accommodation(request):
	response = {"status": "failed", "message": ""}


	data = request["data"]
	hotel_category = data["hotel_category"]
	room_type = data["room_type"]
	meal_plan = data["meal_plan"]

	Accommodation = Accommodation.objects.create(
		hotel_category=hotel_category,
		room_type=room_type,
		meal_plan=meal_plan,
	)

	if Accommodation is not None:
		response["status"] = "ok"


	return Response(response)

@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_accommodation(request):
	response = {"status": "failed", "message": ""}



	data = request["data"]
	id = data["id"]
	accommodation = Accommodation.objects.get(id=id)
	response["id"] = accommodation.id
	response["HotelCategory"] = [{"id": item.id, "star_rating": item.star_rating, "category": item.category} for item in accommodation.hotelcategory_set.all()]
	response["RoomType"] = [{"id": item.id, "room_type": item.room_type} for item in accommodation.roomtype_set.all()]
	response["MealPlan"] = [{"id": item.id, "meal_plan": item.meal_plan} for item in accommodation.mealplan_set.all()]


	return Response(response)

@api_view(["POST"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def update_accommodation(request):
	response = {"status": "failed", "message": ""}


	data = request["data"]
	id = data["id"]

	try:
		accommodation = Accommodation.objects.get(id=id)
		accommodation.id = data["id"]
		accommodation.hotel_category = data["hotel_category"]
		accommodation.room_type = data["room_type"]
		accommodation.meal_plan = data["meal_plan"]
		accommodation.save()
		response["status"] = "ok"
	except:
		pass

	return Response(response)

@api_view(["POST"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def delete_accommodation(request):
	response = {"status": "failed", "message": ""}


	data = request.data
	id = data["id"]
	try:
		accommodation = Accommodation.objects.get(id=id)

		if accommodation is not None:
			accommodation.delete()
			response["status"] = "ok"
	except:
		pass


	return Response(response)

@api_view(["POST"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def create_currency(request):
	response = {"status": "failed", "message": ""}


	data = request["data"]

	Currency = Currency.objects.create(
			)

	if Currency is not None:
		response["status"] = "ok"


	return Response(response)

@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_currency(request):
	response = {"status": "failed", "message": ""}

	data = request.GET
	try:
		id = data["id"]
		currency = Currency.objects.get(id=id)
		response["id"] = currency.id
		response["currency"] = currency.currency
		response["status"] = "ok"
	except Exception as e:
		currencies = []
		for currency in Currency.objects.all():
			currencies.append({
				"id": currency.id,
				"currency": currency.currency
			})
		response["currencies"] = currencies
		response["status"] = "ok"
		# print(e)

	return Response(response)

@api_view(["POST"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def update_currency(request):
	response = {"status": "failed", "message": ""}


	data = request["data"]
	id = data["id"]
	try:
		currency = Currency.objects.get(id=id)
		currency.id = data["id"]
		currency.currency = data["currency"]
		currency.save()
		response["status"] = "ok"
	except:
		pass

	return Response(response)

@api_view(["POST"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def delete_currency(request):
	response = {"status": "failed", "message": ""}


	data = request.data
	id = data["id"]
	try:
		currency = Currency.objects.get(id=id)

		if currency is not None:
			currency.delete()
			response["status"] = "ok"
	except:
		pass


	return Response(response)

@api_view(["POST"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_tour_types(request):
	response = {"status": "failed", "message": ""}


	data = request.data
	try:
		id = data["id"]
		tourType = TourType.objects.get(id=id)
		if tourType is not None:
			response["tourType"] = {
				"id": tourType.id,
				"type": tourType.type
			}
	except:
		tourTypes = TourType.objects.all()
		data = []
		if tourTypes is not None:
			for tourType in tourTypes:
				data.append({
					"id": tourType.id,
					"type": tourType.type
				})
		response["tourTypes"] = data

	response["status"] = "ok"


	return Response(response)

