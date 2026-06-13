from rest_framework_simplejwt.authentication import JWTAuthentication

class HeaderJWTAuthentication(JWTAuthentication):

    def authenticate(self, request):
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            # Fallback to token from cookies
            raw_token = request.COOKIES.get("accessToken")
            if not raw_token:
                return None
        else:
            parts = auth_header.split()
            if len(parts) != 2 or parts[0].lower() != "bearer":
                return None
            raw_token = parts[1]

        try:
            validated_token = self.get_validated_token(raw_token)
        except Exception as e:
            print(e)
            return None

        return self.get_user(validated_token), validated_token
