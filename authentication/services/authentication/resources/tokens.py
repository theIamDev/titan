from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken

class TokenManager:
    @staticmethod
    def create_tokens(user):
        """Generate access and refresh tokens for a given user."""
        refresh = RefreshToken.for_user(user)
        return {
            "access_token": str(refresh.access_token),
            "refresh_token": str(refresh),
        }

    @staticmethod
    def renew_access_token(refresh_token):
        """Renew an access token using a refresh token."""
        try:
            refresh = RefreshToken(refresh_token)
            return {
            "access_token": str(refresh.access_token),
            "refresh_token": str(refresh),
        }
        except (TokenError, InvalidToken) as e:
            return {"error": str(e)}
