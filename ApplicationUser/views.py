from django.shortcuts import render

from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from .models import TourInquiry
from Common.models import AvailableLanguage
from Common.models import TransportType
from Common.models import Currency
from .models import TourInquiryHasAgeCategory
from Common.models import AgeCategory
from Place.models import Place


# Create your views here.

from django.shortcuts import render
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken

from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

from .models import *

import json
from django.conf import settings

from BininsNotification.utils import notifyAdmin

# Create your views here.


@api_view(["POST"])
@authentication_classes([])
@permission_classes([AllowAny])
def signup(request):
    response = {"status": "failed", "message": ""}
    data = request.data

    try:
        first_name = data["firstName"]
        last_name = data["lastName"]
        email = data["email"]
        password = data["password"]
        password_confirmation = data["password_confirmation"]
        phone = data["phone"]

        if password == password_confirmation:
            user = User.objects.create(
				username=first_name + ' ' + last_name,
                first_name=first_name, last_name=last_name, email=email, password=make_password(password))
            if user is not None:
                tourist = Tourist.objects.create(phone=phone, user=user)
                if tourist is not None:
                    refresh_token = RefreshToken.for_user(user)
                    access_token = str(refresh_token.access_token)
                    response["access"] = access_token
                    response["refresh"] = str(refresh_token)
                    response["status"] = "ok"
        else:
            response["message"] = "Passwords do not match"

    except Exception as e:
        print(e)
    return Response(response)


@api_view(["POST"])
@authentication_classes([])
@permission_classes([AllowAny])
def sign_in(request):
	response = {"status": "failed"}
	data = request.data
	try:
		email = data["email"]
		password = data["password"]
		user = User.objects.get(email=email)
		if user.check_password(password):
			refresh_token = RefreshToken.for_user(user)
			access_token = str(refresh_token.access_token)
			response["access"] = access_token
			response["refresh"] = str(refresh_token)
			response["status"] = "ok"
		else:
			response["status"] = "failed"
			response["message"] = "Password does not match"
	except Exception as e:
		print(e)
	return Response(response)


@api_view(["POST"])
@authentication_classes([])
@permission_classes([AllowAny])
def admin_sign_in(request):
	response = {"status": "failed"}
	data = request.data
	try:
		username = data["username"]
		password = data["password"]
		user = User.objects.get(username=username)
		
		if user.check_password(password):
			if user.is_superuser:
				refresh_token = RefreshToken.for_user(user)
				access_token = str(refresh_token.access_token)
				response["access"] = str(access_token)
				response["refresh"] = str(refresh_token)
				response["status"] = "ok"
			else:
				response["message"] = "Admin credentials are invalid. Please check them again"
		else:
			response["status"] = "failed"
			response["message"] = "Password does not match"
	except Exception as e:
		print(e)
	return Response(response)


@api_view(["POST"])
def refresh_token(request):
	response = {"status": "failed"}
	print(request.data)
	try:
		data = request.data
		refreshTokenStr = data["refresh"]
		oldRefreshToken = RefreshToken(refreshTokenStr)
		outstanding = OutstandingToken.objects.get(jti=oldRefreshToken["jti"])
		BlacklistedToken.objects.get_or_create(token=outstanding)
		user_id = oldRefreshToken["user_id"]
		print(user_id)
		user = User.objects.get(id=user_id)
		print(user)

		newRefreshToken = RefreshToken.for_user(user)
		response["refresh"] = str(newRefreshToken)
		response["access"] = str(newRefreshToken.access_token)
		response["status"] = "ok"
	except Exception as e:
		print(e)
		pass

	print(response)
	return Response(response)


@api_view(["POST"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def create_tourinquiry(request):
	response = {"status": "failed", "message": ""}

	data = request.data
	print(data)

	try:
		ageRanges = data["ageRanges"]
		transportTypes = data["transportTypes"]
		places = data["places"]
		fullName = data["fullName"]
		arrival = data["arrival"]
		departure = data["departure"]
		arrivalAirport = data["arrivalAirport"]
		departureAirport = data["departureAirport"]
		nationality = data["nationality"]
		durationOfStay = data["durationOfStay"]
		guideLanguage = data["guideLanguage"]
		estimatedBudget = data["estimatedBudget"]
		currency = data["currency"]
		needVisaAssistance = True if data["needVisaAssistance"][0] == 'true' else False
		needTravelInsurance = True if data["needTravelInsurance"] == 'true' else False

		placesObjects = []

		requestedLanguage = AvailableLanguage.objects.get(id=guideLanguage)
		currency = Currency.objects.get(id=currency)

		print(requestedLanguage)
		print(currency)

		ageRanges = json.loads(ageRanges)
		# print(ageRanges)
		# print(ageRanges[0])

		tourInquiry = TourInquiry.objects.create(
			full_name=fullName,
			arrival=arrival,
			departure=departure,
			arrival_airport=arrivalAirport,
			departure_airport=departureAirport,
			nationality=nationality,
			duration_of_stay=durationOfStay,
			guide_language=requestedLanguage,
			estimated_budget=estimatedBudget,
			currency=currency,
			need_visa_assistance=needVisaAssistance,
			need_travel_insurance=needTravelInsurance
		)

		if tourInquiry is not None:
			transportTypes = json.loads(transportTypes)
			for transportType in transportTypes:
				try:
					transportTypeObject = TransportType.objects.get(id=transportType)
					print(transportTypeObject)
					tourInquiryHasTransportType = TourInquiryHasTransportType.objects.create(
						transport_type=transportType,
						tour_inquiry=tourInquiry
					)
			# 		placesObjects.append(place)
				except Exception as e:
					print(e)

			for ageRange in ageRanges:
				ageRangeObject = AgeCategory.objects.get(id=ageRange["id"])
				tourInquiryHasAgeCategory = TourInquiryHasAgeCategory.objects.create(
					age_category=ageRangeObject,
					tour_inquiry=tourInquiry,
					numberOfPeople=ageRange["numberOfPeople"]
					)
				print(ageRangeObject)

			places = json.loads(places)
			print(places)
			print(places[0])

			for placeID in places:
				try:
					place = Place.objects.get(id=placeID)
					print(place)
					tourInquiryHasPlace = TourInquiryHasPlace.objects.create(
						place=place,
						tour_inquiry=tourInquiry
					)
			# 		placesObjects.append(place)
				except Exception as e:
					print(e)
			notifyAdmin("New Inquiry", "New inquiry has been made. please check it out!", data)
			response["status"] = "ok"
	except Exception as e:
		print(e)
		pass

	return Response(response)

@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_tourinquiry(request):
	response = {"status": "failed", "message": ""}


	data = request["data"]
	id = data["id"]
	tourinquiry = TourInquiry.objects.get(id=id)
	response["id"] = tourinquiry.id
	response["full_name"] = tourinquiry.full_name
	response["arrival"] = tourinquiry.arrival
	response["departure"] = tourinquiry.departure
	response["arrival_airport"] = tourinquiry.arrival_airport
	response["departure_airport"] = tourinquiry.departure_airport
	response["nationality"] = tourinquiry.nationality
	response["duration_of_stay"] = tourinquiry.duration_of_stay
	response["need_visa_assistance"] = tourinquiry.need_visa_assistance
	response["need_travel_insurance"] = tourinquiry.need_travel_insurance
	response["AvailableLanguage"] = [{"id": item.id, "language": item.language} for item in tourinquiry.availablelanguage_set.all()]
	response["TransportType"] = [{"id": item.id, "type": item.type} for item in tourinquiry.transporttype_set.all()]
	response["age_categories"] = tourinquiry.age_categories
	response["places"] = tourinquiry.places
	response["estimated_budget"] = tourinquiry.estimated_budget
	response["Currency"] = [{"id": item.id, "currency": item.currency} for item in tourinquiry.currency_set.all()]

	return Response(response)

@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_tourinquiries(request):
	response = {"status": "failed", "message": ""}

	tourinquiry = TourInquiry.objects.all()
	data = []
	for inquiry in tourinquiry:
		# print(dir(inquiry))
		data.append({
			"id": inquiry.id,
			"full_name": inquiry.full_name,
			"arrival": inquiry.arrival,
			"departure": inquiry.departure,
			"arrival_airport": inquiry.arrival_airport,
			"departure_airport": inquiry.departure_airport,
			"nationality": inquiry.nationality,
			"duration_of_stay": inquiry.duration_of_stay,
			"need_visa_assistance": inquiry.need_visa_assistance,
			"need_travel_insurance": inquiry.need_travel_insurance,
			"AvailableLanguage": inquiry.guide_language.language,
			"TransportType": [{"id": item.id, "type": item.type} for item in inquiry.tourinquiryhastransporttype_set.all()],
			"age_categories": [{"id": item.id, "age_category": item.age_category.category, "numberOfPeople": item.numberOfPeople, "price": item.age_category.price} for item in inquiry.tourinquiryhasagecategory_set.all()],
			"places": [
				{
					"id": item.place.id,
					"name": item.place.name,
					"about": item.place.about,
					"highlights": item.place.highlights,
					"bestTime": item.place.bestTime,
					"location": item.place.location,
					"source": item.place.source,
					"type": item.place.type.type
				} 
				for item in inquiry.tourinquiryhasplace_set.all()],
			"estimated_budget": inquiry.estimated_budget,
			"Currency": inquiry.currency.currency
		})

	response["inquiries"] = data
	response["status"] = "ok"

	return Response(response)

@api_view(["POST"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def update_tourinquiry(request):
	response = {"status": "failed", "message": ""}


	data = request["data"]
	id = data["id"]

	try:
		tourinquiry = TourInquiry.objects.get(id=id)
		tourinquiry.id = data["id"]
		tourinquiry.full_name = data["full_name"]
		tourinquiry.arrival = data["arrival"]
		tourinquiry.departure = data["departure"]
		tourinquiry.arrival_airport = data["arrival_airport"]
		tourinquiry.departure_airport = data["departure_airport"]
		tourinquiry.nationality = data["nationality"]
		tourinquiry.duration_of_stay = data["duration_of_stay"]
		tourinquiry.need_visa_assistance = data["need_visa_assistance"]
		tourinquiry.need_travel_insurance = data["need_travel_insurance"]
		tourinquiry.guide_language = data["guide_language"]
		tourinquiry.transport_type = data["transport_type"]
		tourinquiry.age_categories = data["age_categories"]
		tourinquiry.places = data["places"]
		tourinquiry.estimated_budget = data["estimated_budget"]
		tourinquiry.currency = data["currency"]
		tourinquiry.save()
		response["status"] = "ok"
	except:
		pass

	return Response(response)

@api_view(["POST"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def delete_tourinquiry(request):
	response = {"status": "failed", "message": ""}


	data = request.data
	id = data["id"]
	try:
		tourinquiry = TourInquiry.objects.get(id=id)

		if tourinquiry is not None:
			tourinquiry.delete()
			response["status"] = "ok"
	except:
		pass


	return Response(response)

@api_view(["POST"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def create_tourinquiryhasagecategory(request):
	response = {"status": "failed", "message": ""}


	data = request["data"]
	age_category = data["age_category"]
	tour_inquiry = data["tour_inquiry"]

	TourInquiryHasAgeCategory = TourInquiryHasAgeCategory.objects.create(
		age_category=age_category,
		tour_inquiry=tour_inquiry,
	)

	if TourInquiryHasAgeCategory is not None:
		response["status"] = "ok"


	return Response(response)

@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_tourinquiryhasagecategory(request):
	response = {"status": "failed", "message": ""}



	data = request["data"]
	id = data["id"]
	tourinquiryhasagecategory = TourInquiryHasAgeCategory.objects.get(id=id)
	response["id"] = tourinquiryhasagecategory.id
	response["AgeCategory"] = [{"id": item.id, "category": item.category, "min_age": item.min_age, "max_age": item.max_age} for item in tourinquiryhasagecategory.agecategory_set.all()]
	response["TourInquiry"] = [{"id": item.id, "full_name": item.full_name, "arrival": item.arrival, "departure": item.departure, "arrival_airport": item.arrival_airport, "departure_airport": item.departure_airport, "nationality": item.nationality, "duration_of_stay": item.duration_of_stay, "need_visa_assistance": item.need_visa_assistance, "need_travel_insurance": item.need_travel_insurance, "guide_language": item.guide_language, "transport_type": item.transport_type, "age_categories": item.age_categories, "places": item.places, "estimated_budget": item.estimated_budget, "currency": item.currency} for item in tourinquiryhasagecategory.tourinquiry_set.all()]


	return Response(response)

@api_view(["POST"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def update_tourinquiryhasagecategory(request):
	response = {"status": "failed", "message": ""}


	data = request["data"]
	id = data["id"]

	try:
		tourinquiryhasagecategory = TourInquiryHasAgeCategory.objects.get(id=id)
		tourinquiryhasagecategory.id = data["id"]
		tourinquiryhasagecategory.age_category = data["age_category"]
		tourinquiryhasagecategory.tour_inquiry = data["tour_inquiry"]
		tourinquiryhasagecategory.save()
		response["status"] = "ok"
	except:
		pass

	return Response(response)

@api_view(["POST"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def delete_tourinquiryhasagecategory(request):
	response = {"status": "failed", "message": ""}


	data = request.data
	id = data["id"]
	try:
		tourinquiryhasagecategory = TourInquiryHasAgeCategory.objects.get(id=id)

		if tourinquiryhasagecategory is not None:
			tourinquiryhasagecategory.delete()
			response["status"] = "ok"
	except:
		pass


	return Response(response)


@api_view(["POST"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAdminUser])
def create_new_tourpackage(request):
	response = {"status": "failed", "message": ""}

	data = request.data
	files = request.FILES
	# id = data["id"]
	

	try:
		print(data)
		name = data["name"]
		print(name)
		type = data["type"]
		print(type)
		type = TourType.objects.get(id=int(type[0]))
		# price = data["price"]
		# print(price)
		description = data["description"]
		# print(description)
		specialNotes = data["specialNotes"]
		# print(specialNotes)
		inclusions = "##".join(json.loads(data["inclusions"]))
		# print(inclusions)
		exclusions = "##".join(json.loads(data["exclusions"]))
		# print(exclusions)
		highlights = "##".join(json.loads(data["highlights"]))
		# print(highlights)

		tourPackage = TourPackage.objects.create(
			name=name,
			type=type,
			total_price=0.0,
			description=description,
			special_notes=specialNotes,
			inclusions=inclusions,
			exclusions=exclusions,
			package_highlights=highlights
		)

		if tourPackage is not None:
			if len(files) > 0:
				file = request.FILES["packageImage"]
				tourPackageMedia = TourPackageMedia.objects.create(
					image=file,
					tour_package=tourPackage
				)

			selectedAgeRange = json.loads(data["selectedAgeRanges"])
			totalPrice = 0.0
			for ageRange in selectedAgeRange:
				try:
					ageCategory = AgeCategory.objects.get(category=ageRange["category"])
					print(ageCategory)
					totalPrice += int(ageRange["numberOfPeople"]) * ageCategory.price
					tourPackageHasAgeCategory = TourPackageHasAgeCategory.objects.create(
						age_category=ageCategory,
						tour_package=tourPackage,
						numberOfPeople=int(ageRange["numberOfPeople"])
					)
				except:
					pass

			tourPackage.total_price = totalPrice
			tourPackage.save()

			selectedPlaces = json.loads(data["selectedPlaces"])
			for selectedPlace in selectedPlaces:
				try:
					place = Place.objects.get(id=int(selectedPlace))
					print(place)
					tourPackageHasPlace = TourPackageHasPlace.objects.create(
						place=place,
						tour_package=tourPackage)
				except:
					pass
			response["status"] = "ok"
			print("Successfully added tour package!")
		# tourinquiryhasagecategory = TourInquiryHasAgeCategory.objects.get(id=id)

		# if tourinquiryhasagecategory is not None:
		# 	tourinquiryhasagecategory.delete()
		# 	response["status"] = "ok"
	except Exception as e:
		print(e)
		pass


	return Response(response)


@api_view(["POST"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAdminUser])
def edit_tourpackage(request):
	response = {"status": "failed", "message": ""}

	data = request.data
	files = request.FILES
	print(data)
	try:
		id = data["id"]
		tourPackage = TourPackage.objects.get(id=id)

		if tourPackage is not None:
			try:
				name = data["name"]
				tourPackage.name = name
				print(name)
			except:
				pass

			try:
				type = TourType.objects.get(id=int(data["type"]))
				if type is not None:
					tourPackage.type = type
			except:
				pass

			try:
				description = data["description"]
				tourPackage.description = description
				print(description)
			except:
				pass

			try:
				specialNotes = data["specialNotes"]
				tourPackage.special_notes = specialNotes
				print(specialNotes)
			except:
				pass

			try:
				inclusions = "##".join(json.loads(data["inclusions"]))
				tourPackage.inclusions = inclusions
				print(inclusions)
			except:
				pass

			try:
				exclusions = "##".join(json.loads(data["exclusions"]))
				tourPackage.exclusions = exclusions
				print(exclusions)
			except:
				pass

			try:
				highlights = "##".join(json.loads(data["highlights"]))
				print(highlights)
				tourPackage.package_highlights = highlights
			except:
				pass

			tourPackage.save()

			if len(files) > 0:
				file = request.FILES["packageImage"]
				images = tourPackage.tourpackagemedia_set.all()
				if len(images) > 0:
					images[0].image = files
					images[0].save()
				else:
					tourPackageMedia = TourPackageMedia.objects.create(
						image=file,
						tour_package=tourPackage
					)
			
			selectedPlaces = json.loads(data["selectedPlaces"])
			for i in range(len(selectedPlaces)):
				if selectedPlaces[i] is not None:
					selectedPlaces[i] = int(selectedPlaces[i])

			previousSelectedPlaces = tourPackage.tourpackagehasplace_set.all()
			previousSelectedPlacesIDs = []
			for place in previousSelectedPlaces:
				previousSelectedPlacesIDs.append(place.place.id)
				if not selectedPlaces.__contains__(place.place.id):
					place.delete()

			for selectedPlaceID in selectedPlaces:
				if not previousSelectedPlacesIDs.__contains__(selectedPlaceID):
					try:
						place = Place.objects.get(id=int(selectedPlaceID))
						print(place)
						tourPackageHasPlace = TourPackageHasPlace.objects.create(
							place=place,
							tour_package=tourPackage)
					except:
						pass

			selectedAgeRange = json.loads(data["selectedAgeRanges"])
			totalPrice = 0.0
			for ageRange in selectedAgeRange:
				ageCategory = tourPackage.tourpackagehasagecategory_set.filter(agecategory_category=ageRange["category"])
				print("Existing age categories: ", ageCategory)
				try:
					ageCategory = AgeCategory.objects.get(category=ageRange["category"])
					print(ageCategory)
					# totalPrice += int(ageRange["numberOfPeople"]) * ageCategory.price
					# tourPackageHasAgeCategory = TourPackageHasAgeCategory.objects.create(
					# 	age_category=ageCategory,
					# 	tour_package=tourPackage,
					# 	numberOfPeople=int(ageRange["numberOfPeople"])
					# )
				except:
					pass

			tourPackage.total_price = totalPrice
			tourPackage.save()


			response["status"] = "ok"
		# tourinquiryhasagecategory = TourInquiryHasAgeCategory.objects.get(id=id)

		# if tourinquiryhasagecategory is not None:
		# 	tourinquiryhasagecategory.delete()
		# 	response["status"] = "ok"
	except Exception as e:
		print(e)
		pass


	return Response(response)


@api_view(["GET"])
@authentication_classes([])
@permission_classes([])
def get_tourpackages(request):
	response = {"status": "failed", "message": ""}

	data = request.data
	# id = data["id"]

	try:
		packages = []
		tourPackages = TourPackage.objects.all()
		for tourPackage in tourPackages:
			images = tourPackage.tourpackagemedia_set.all()
			packages.append({
				"id": tourPackage.id,
				"name": tourPackage.name,
				"type": tourPackage.type.type,
				"total_price": tourPackage.total_price,
				"description": tourPackage.description,
				"special_notes": tourPackage.special_notes,
				"inclusions": tourPackage.inclusions.split("##"),
				"exclusions": tourPackage.exclusions.split("##"),
				"package_highlights": tourPackage.package_highlights.split("##"),
				"image": settings.DOMAIN + images[0].image.url if len(images) > 0 else "",
				"ageRanges": [
					{
						"id": ageRange.id,
						"age_category": {
							"id": ageRange.id,
							"category": ageRange.age_category.category,
							"min_age": ageRange.age_category.min_age,
							"max_age": ageRange.age_category.max_age,
							"price": ageRange.age_category.price
						},
						"numberOfPeople": ageRange.numberOfPeople,
					} 
					for ageRange in tourPackage.tourpackagehasagecategory_set.all()],
				"places": [place.place.id for place in tourPackage.tourpackagehasplace_set.all()]
			})

		if tourPackage is not None:
			response["packages"] = packages
			response["status"] = "ok"
		# tourinquiryhasagecategory = TourInquiryHasAgeCategory.objects.get(id=id)

		# if tourinquiryhasagecategory is not None:
		# 	tourinquiryhasagecategory.delete()
		# 	response["status"] = "ok"
	except Exception as e:
		print(e)
		pass

	return Response(response)

