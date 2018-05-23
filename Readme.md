Auth Credentials
username 3b78ec4d306732385b9af3b088b84f831a689a66
admin 8344d4dccc9d2f83a19c67e2edd6b063e47a4b7c


To Generate new token
1. Create a new user from django shell
2. Execute following commands
>>> from django.contrib.auth.models import User
>>> from rest_framework.authtoken.models import Token
>>>
>>> users = User.objects.all()
>>> for user in users:
...     token, created = Token.objects.get_or_create(user=user)
...     print user.username, token.key

To get a token for existing user. Refer Postman collection's API "Get Auth Token"

Create, Update, Delete requires Auth token. Read is open API doesn't require any authentication.


Note: This document is not Markdown styled