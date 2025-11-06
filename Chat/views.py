from django.shortcuts import render

from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from .models import Contact
from django.contrib.auth.models import User, AnonymousUser
from ApplicationUser.models import UnregisteredUser
from .models import Message, Contact

from datetime import datetime

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from ApplicationUser.authentication import OptionalJWTAuthentication


# Create your views here.


def getContactList(user, email):
	contacts = None
	sender = None

	if isinstance(user, AnonymousUser):
		try:
			sender = UnregisteredUser.objects.get(email=email)
			contacts = Contact.objects.filter(anonymous_user=sender.id)
			print("User matched successfully!")
		except Exception as e:
			print(e)
			pass
	else:
		sender = user
		print("Authenticated User!")
		if user.is_superuser:
			contacts = Contact.objects.filter(staff=sender.id)
		else:
			contacts = Contact.objects.filter(user=sender.id)

	print(user)
	data = []
	if contacts is not None:
		for contact in contacts:
			data.append({
				"id": contact.id,
				"accepted": contact.accepted
			})

			if isinstance(user, AnonymousUser):
				print(contact.staff)
				if contact.staff is not None:
					data[-1]["assistantID"] = contact.staff.id
					data[-1]["assistant"] = contact.staff.first_name + \
                                            ' ' + contact.staff.last_name
					
					if data[-1]["assistant"] == ' ':
						data[-1]["assistant"] = contact.staff.username
			else:
				if user.is_superuser:
					if contact.accepted:
						if contact.user is None:
							data[-1]["anonymousUserID"] = contact.anonymous_user.id
							data[-1]["anonymousUser"] = contact.anonymous_user.name
						else:
							data[-1]["userID"] = contact.user.id
							data[-1]["user"] = contact.user.first_name + \
								' ' + contact.user.last_name
				else:
					if contact.staff is not None:
						data[-1]["assistantID"] = contact.staff.id
						data[-1]["assistant"] = contact.staff.first_name + \
							' ' + contact.staff.last_name

						if data[-1]["assistant"] == ' ':
							data[-1]["assistant"] = contact.staff.username

	return data



@api_view(["POST"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def create_tourinquiryhasplace(request):
	response = {"status": "failed", "message": ""}


	data = request["data"]

	Contact = Contact.objects.create(
			)

	if Contact is not None:
		response["status"] = "ok"


	return Response(response)

@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_tourinquiryhasplace(request):
	response = {"status": "failed", "message": ""}

	data = request["data"]
	id = data["id"]
	contact = Contact.objects.get(id=id)
	response["id"] = contact.id
	response["User"] = [{"id": item.id, "first_name": item.first_name, "last_name": item.last_name, "email": item.email} for item in contact.user_set.all()]
	response["User"] = [{"id": item.id, "first_name": item.first_name, "last_name": item.last_name, "email": item.email} for item in contact.user_set.all()]


	return Response(response)

@api_view(["POST"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def update_tourinquiryhasplace(request):
	response = {"status": "failed", "message": ""}


	data = request["data"]
	id = data["id"]

	try:
		contact = Contact.objects.get(id=id)
		contact.id = data["id"]
		contact.staff = data["staff"]
		contact.user = data["user"]
		contact.save()
		response["status"] = "ok"
	except:
		pass

	return Response(response)

@api_view(["POST"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def delete_tourinquiryhasplace(request):
	response = {"status": "failed", "message": ""}


	data = request.data
	id = data["id"]
	try:
		contact = Contact.objects.get(id=id)

		if contact is not None:
			contact.delete()
			response["status"] = "ok"
	except:
		pass


	return Response(response)


@api_view(["POST"])
@authentication_classes([JWTAuthentication])
@permission_classes([AllowAny])
def init_chat(request):
	response = {"status": "failed", "message": ""}
	data = request.data
	contact = None
	try:
		if not isinstance(request.user, AnonymousUser):
			user = request.user
			print(user)
			
			# print(dir(user))
			if user.is_authenticated:
				try:
					contact = Contact.objects.filter(user=user)
				except:
					print("create chat")
					contact = Contact.objects.create(user=user)
		else:
			email = data["email"]
			name = data["name"]
			unregisteredUser = None
			if email is not None and name is not None:
				try:
					unregisteredUser = UnregisteredUser.objects.get(email=email)
				except:
					print("create anonymous user")
					unregisteredUser = UnregisteredUser.objects.create(
						email=email,
						name=name
					)

			if unregisteredUser is not None:
				try:
					contact = Contact.objects.filter(anonymous_user=unregisteredUser)
				except:
					print("create chat")
					contact = Contact.objects.create(anonymous_user=unregisteredUser)

		if contact is not None:
			response["status"] = "ok"
	except Exception as e:
		print(e)
	print(response)
	return Response(response)


@api_view(["POST"])
@authentication_classes([JWTAuthentication])
@permission_classes([AllowAny])
def create_message(request):
	response = {"status": "failed", "message": ""}

	data = request.data
	print(data)
	print(request.user)
	user = request.user
	contact = None
	groupName = ""
	targetGroupName = ""
	try:
		try:
			contact = Contact.objects.get(id=data["contactID"])
		except Exception as e:
			print(e)
			print(user)
			print(dir(user))

			if not isinstance(user, AnonymousUser):
				if user.is_authenticated:
					if not user.is_superuser:
						try:
							contact = Contact.objects.get(user=user)
						except:
							print("create chat")
							contact = Contact.objects.create(user=user)
					else:
						try:
							contact = Contact.objects.get(staff=user)
						except:
							print("create chat")
							contact = Contact.objects.create(staff=user)
			else:
				email = data["email"]
				name = data["name"]
				unregisteredUser = None
				try:
					unregisteredUser = UnregisteredUser.objects.get(email=email)
				except:
					print("create anonymous user")
					unregisteredUser = UnregisteredUser.objects.create(
						email=email,
						name=name)

				if unregisteredUser is not None:
					try:
						contact = Contact.objects.get(anonymous_user=unregisteredUser)
					except Exception as e:
						contact = Contact.objects.create(anonymous_user=unregisteredUser)

		if contact is not None:
			sender = None
			receiver = None
			source = "Me"

			try:
				responseData = {
					"id": contact.id,
					"accepted": contact.accepted
				}

				if isinstance(user, AnonymousUser):
					print("User is an anonymous user!")
					sender = contact.anonymous_user
					receiver = contact.staff
					targetGroupName = f"{receiver.username}-chat"
					groupName = f"{sender.email.replace('@', '-').replace('.', '-')}-chat"
					if contact.staff is not None:
						responseData["assistantID"] = contact.staff.id
						responseData["assistant"] = contact.staff.first_name + \
												' ' + contact.staff.last_name
				else:
					if user.is_authenticated:
						if user.is_superuser:
							sender = contact.staff
							if contact.user is not None:
								receiver = contact.user
								groupName = f"{user.username}-chat"
								targetGroupName = f"{receiver.username}-chat"
							else:
								receiver = contact.anonymous_user
								groupName = f"{user.username}-chat"
								targetGroupName = f"{receiver.email}-chat"
								targetGroupName = targetGroupName.replace("@", '-').replace(".", '-')
							
							if contact.accepted:
								if contact.user is None:
									responseData["anonymousUserID"] = contact.anonymous_user.id
									responseData["anonymousUser"] = contact.anonymous_user.name
								else:
									responseData["userID"] = contact.user.id
									responseData["user"] = contact.user.first_name + \
										' ' + contact.user.last_name
						else:
							sender = contact.user
							receiver = contact.staff
							groupName = f"{sender.username}-chat"
							targetGroupName = f"{receiver.username}-chat"

							if contact.staff is not None:
								responseData["assistantID"] = contact.staff.id
								responseData["assistant"] = contact.staff.first_name + \
									' ' + contact.staff.last_name

				# async_to_sync(get_channel_layer().group_send)
				print(f"Notifying group {groupName} about the new message")

				messageText = data["message"]
				message = Message.objects.create(
					message=messageText,
					datetime=datetime.now(),
					contact=contact)

				if message is not None:
					targetUser = ""
					if isinstance(sender, User):
						message.sender = sender
						message.save()

						if sender.is_superuser:
							if contact.user is None:
								targetUser = contact.anonymous_user.name
							else:
								targetUser = contact.user.first_name + ' ' + contact.user.last_name
						else:
							if contact.user == sender:
								targetUser = contact.staff.first_name + ' ' + contact.staff.last_name
					else:
						targetUser = contact.staff.first_name + ' ' + contact.staff.last_name
					
					responseData["newMessage"] = {
						"id": message.id,
						"sender": source,
						"message": message.message,
						"datetime": str(message.datetime)
					}

					print(f"Notifying {groupName}: sender")
					async_to_sync(get_channel_layer().group_send)(
						f"{groupName}",
						{
							"type": "updateContact",
							"message": responseData
						}
					)


					responseData["newMessage"]["sender"] = targetUser
					print(f"Notifying {targetGroupName}: receiver")
					async_to_sync(get_channel_layer().group_send)(
						f"{targetGroupName}",
						{
							"type": "updateContact",
							"message": responseData
						}
					)

					response["status"] = "ok"
			except Exception as e:
				print(e)
	except Exception as e:
		print(e)

	# contact = data["contact"]

	# Message = Message.objects.create(
	# 	contact=contact,
	# )

	return Response(response)

@api_view(["POST"])
@authentication_classes([JWTAuthentication])
@permission_classes([AllowAny])
def get_message(request):
	response = {"status": "failed", "message": ""}

	isUserAnonymous = isinstance(request.user, AnonymousUser)

	data = request.data
	id = data["contactID"]
	contact = Contact.objects.get(id=id)
	messages = contact.message_set.all()
	print(messages)
	messagesData = []
	for message in messages:
		source = "Me"
		if not isUserAnonymous:
			if message.sender is not None:
				if request.user == message.sender:
					source = "Me"
				else:
					source = f"{message.sender.first_name} {message.sender.last_name}"
			else:
				if contact.anonymous_user is not None:
					source = f"{contact.anonymous_user.name}"
		else:
			try:
				unregisteredUser = UnregisteredUser.objects.get(email=data["email"])
				if unregisteredUser == contact.anonymous_user:
					if message.sender is not None:
						source = f"{message.sender.first_name} {message.sender.last_name}"
						if source == " ":
							source = message.sender.username
			except Exception as e:
				# print(e)
				pass
		messagesData.append({
			"id": message.id,
			"sender": source,
			"message": message.message,
			"datetime": message.datetime
		})

	response["messages"] = messagesData
	response["status"] = "ok"
	# print(response)
	return Response(response)

@api_view(["POST"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def update_message(request):
	response = {"status": "failed", "message": ""}


	data = request["data"]
	id = data["id"]

	try:
		message = Message.objects.get(id=id)
		message.id = data["id"]
		message.sender = data["sender"]
		message.message = data["message"]
		message.datetime = data["datetime"]
		message.contact = data["contact"]
		message.save()
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
		message = Message.objects.get(id=id)
		if message is not None:
			message.delete()
			response["status"] = "ok"
	except:
		pass

	return Response(response)


@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_waiting_list(request):
	response = {"status": "failed"}
	contacts = Contact.objects.filter(staff__isnull=True)
	data = []
	for contact in contacts:
		if not contact.accepted:
			data.append({
					"id": contact.id
				})
			
			user = contact.user
			if user is None:
				user = contact.anonymous_user
				if user is not None:
					data[-1]["anonymousUserID"] = user.id
					data[-1]["anonymousUser"] = user.name
			else:
				data[-1]["userID"] = user.id
				data[-1]["user"] = user.first_name + ' ' + user.last_name
	
	response["waitingList"] = data
	response["status"] = "ok"
	return Response(response)


@api_view(["POST"])
@authentication_classes([OptionalJWTAuthentication])
@permission_classes([AllowAny])
def get_contact_list(request):
	response = {"status": "failed"}
	user = request.user
	requestData = request.data
	contacts = None
	sender = None

	print(requestData)

	if isinstance(user, AnonymousUser):
		email = requestData["email"]
		request.session["email"] = email
		# print(request.session.session_key)
		request.session.save()

		print("Session items: ", request.session.items())
		try:
			sender = UnregisteredUser.objects.get(email=email)
			contacts = Contact.objects.filter(anonymous_user=sender.id)
			print("User matched successfully!")
		except Exception as e:
			print(e)
			pass
	else:
		sender = user
		print("Authenticated User!")
		if user.is_superuser:
			contacts = Contact.objects.filter(staff=sender.id)
		else:
			contacts = Contact.objects.filter(user=sender.id)

	print(user)
	data = []
	if contacts is not None:
		for contact in contacts:
			data.append({
				"id": contact.id,
				"accepted": contact.accepted
			})
			
			if isinstance(user, AnonymousUser):
				if contact.staff is not None:
					data[-1]["assistantID"] = contact.staff.id
					data[-1]["assistant"] = contact.staff.first_name + \
										' ' + contact.staff.last_name
			else:
				if user.is_superuser:
					if contact.accepted:
						if contact.user is None:
							data[-1]["anonymousUserID"] = contact.anonymous_user.id
							data[-1]["anonymousUser"] = contact.anonymous_user.name
						else:
							data[-1]["userID"] = contact.user.id
							data[-1]["user"] = contact.user.first_name + \
								' ' + contact.user.last_name
				else:
					if contact.staff is not None:
						data[-1]["assistantID"] = contact.staff.id
						data[-1]["assistant"] = contact.staff.first_name + \
							' ' + contact.staff.last_name

	response["contacts"] = data
	response["status"] = "ok"
	return Response(response)


@api_view(["POST"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def accept_request(request):
	response = {"status": "failed"}
	id = request.data["id"]
	contact = Contact.objects.get(id=id)
	if contact is not None:
		contact.staff = request.user
		contact.accepted = True
		contact.save()
		response["status"] = "ok"
	return Response(response)

