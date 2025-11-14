from django.shortcuts import render

from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from .models import PlaceImage
from .models import Place, PlaceType

from django.conf import settings


# Create your views here.

@api_view(["POST"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def create_currency(request):
	response = {"status": "failed", "message": ""}


	data = request["data"]

	PlaceImage = PlaceImage.objects.create(
			)

	if PlaceImage is not None:
		response["status"] = "ok"


	return Response(response)

@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_currency(request):
	response = {"status": "failed", "message": ""}

	data = request["data"]
	id = data["id"]
	placeimage = PlaceImage.objects.get(id=id)
	response["id"] = placeimage.id
	response["image"] = placeimage.image


	return Response(response)

@api_view(["POST"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def update_currency(request):
	response = {"status": "failed", "message": ""}


	data = request["data"]
	id = data["id"]

	try:
		placeimage = PlaceImage.objects.get(id=id)
		placeimage.id = data["id"]
		placeimage.image = data["image"]
		placeimage.save()
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
		placeimage = PlaceImage.objects.get(id=id)

		if placeimage is not None:
			placeimage.delete()
			response["status"] = "ok"
	except:
		pass


	return Response(response)

@api_view(["POST"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def create_place(request):
	response = {"status": "failed", "message": ""}

	data = request.data
	print(data)

	name = data["name"]
	about = data["about"]
	highlights = data["highlights"]
	bestTime = data["bestTime"]
	location = data["location"]
	type = data["type"]

	place = None

	images = request.FILES

	try:
		type = PlaceType.objects.get(id=type)
		print(type)
		place = Place.objects.create(
			name=name,
			about=about,
			highlights=highlights,
			bestTime=bestTime,
			location=location,
			type=type
		)

		if place is not None:
			for key, value in images.items():
				print(key)
				print(value)
				placeImage = PlaceImage.objects.create(
					image=value,
					place=place
				)
			
			try:
				source = data["source"]
				place.source = source
				place.save()
			except Exception as exception:
				print(exception)
				pass
			response["status"] = "ok"
	except Exception as e:
		print(e)
		pass
	# images = data["images"]

	# Place = Place.objects.create(
	# 	images=images,
	# )

	# if Place is not None:
	# 	response["status"] = "ok"


	return Response(response)

@api_view(["GET"])
@authentication_classes([])
@permission_classes([])
def get_place(request):
	response = {"status": "failed", "message": ""}


	data = request.data
	try:
		id = data["id"]
		place = Place.objects.get(id=id)
		response["id"] = place.id
		response["name"] = place.name
		response["PlaceImage"] = [{"id": item.id, "image": item.image} for item in place.placeimage_set.all()]
	except:
		places = []
		for place in Place.objects.all():
			# print(dir(place))
			places.append({
				"id": place.id,
				"name": place.name,
				"type": place.type.type,
				"about": place.about,
				"highlights": place.highlights,
				"bestTime": place.bestTime,
				"location": place.location,
				"source": place.source,
				"images": [{"id": image.id, "url": settings.DOMAIN + image.image.url} for image in place.placeimage_set.all()]
			})
		response["places"] = places
		# print(places)

	response["status"] = "ok"

	return Response(response)

@api_view(["POST"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def update_place(request):
	response = {"status": "failed", "message": ""}


	data = request["data"]
	id = data["id"]

	try:
		place = Place.objects.get(id=id)
		place.id = data["id"]
		place.name = data["name"]
		place.images = data["images"]
		place.save()
		response["status"] = "ok"
	except:
		pass

	return Response(response)

@api_view(["POST"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def delete_place(request):
	response = {"status": "failed", "message": ""}

	data = request.data
	id = data["id"]
	try:
		place = Place.objects.get(id=id)
		if place is not None:
			place.delete()
			response["status"] = "ok"
	except:
		pass

	return Response(response)


@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([AllowAny])
def get_place_types(request):
	response = {"status": "failed", "message": ""}
	data = []
	
	for placeType in PlaceType.objects.all():
		data.append({
			"id": placeType.id,
			"type": placeType.type
		})
	response["placeTypes"] = data
	response["status"] = "ok"

	return Response(response)

