from rest_framework.authentication import TokenAuthentication as BaseTokenAuth
from rest_framework.authtoken.models import Token
#see definition to determine an expiration

class TokenAuthentication(BaseTokenAuth):
    keyword = 'Bearer'