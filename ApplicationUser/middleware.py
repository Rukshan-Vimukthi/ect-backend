from channels.db import database_sync_to_async
from urllib.parse import parse_qs

from django.contrib.auth import get_user_model
from asgiref.sync import sync_to_async


async def get_user(token):
    from django.conf import settings
    import jwt
    from django.contrib.auth.models import AnonymousUser

    if token is None:
        return AnonymousUser()
    
    try:
        if isinstance(token, bytes):
            token = token.decode("utf-8")
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        userID = payload["user_id"]
        if userID is None:
            return AnonymousUser()
        
        user = await sync_to_async(get_user_model().objects.get)(id=userID)
        return user
    except Exception as e:
        print(e)
        return AnonymousUser()
    

class JWTAuthMiddleware:
    def __init__(self, inner):
        self.inner = inner
    
    async def __call__(self, scope, receive, send):
        # print(scope)
        query_string = parse_qs(scope["query_string"].decode())
        token = query_string.get("token", [None])[0]

        if isinstance(token, bytes):
            token = token.decode("utf-8")

        user = await get_user(token)
        scope["user"] = user
        # print("Token: ", token)
        print("User: ", user)
        return await self.inner(scope, receive, send)
