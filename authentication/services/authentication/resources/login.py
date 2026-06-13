from django.contrib.auth import authenticate, get_user_model
from .tokens import TokenManager
from django.http import JsonResponse
from rest_framework import status
import logging
from ..resources.cookies import Cookies
from django.conf import settings

logger = logging.getLogger(__name__)

def login_service(username, password):
    login_handler = UserLogin(username, password)
    logger.debug(f"Login_service user: {login_handler.user}")
    
    if login_handler.user:
        login_handler.set_tokens()
        
    #login_handler.generate_response_with_token_headers()
    login_handler.generate_response_with_tokens()
    logger.debug(f"Login_service response: {login_handler.response}")
    
    return login_handler.response

class UserLogin:
    ACCESS_TOKEN_MAX_AGE = int(settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"].total_seconds())
    REFRESH_TOKEN_MAX_AGE = int(settings.SIMPLE_JWT["REFRESH_TOKEN_LIFETIME"].total_seconds())
    ACCESS_TOKEN_NAME = settings.SIMPLE_JWT["ACCESS_TOKEN_NAME"]
    REFRESH_TOKEN_NAME = settings.SIMPLE_JWT["REFRESH_TOKEN_NAME"]

    def __init__(self, username, password):
        """Initialize and authenticate user."""
        self.user = authenticate(username=username, password=password)
        if not self.user:
            logger.warning(f"Authentication failed for username: {username}")

        self.refresh = None
        self.access = None
        self.response = None

    def set_tokens(self):
        """Generates JWT tokens if authentication is successful."""
        if self.user:
            tokens = TokenManager.create_tokens(self.user)
            self.refresh = tokens.get("refresh_token")
            self.access = tokens.get("access_token")
        else:
            logger.warning("set_tokens() called with no authenticated user.")

    def generate_response_with_token_headers(self):
        """Creates the JSON response with cookies if authentication succeeds."""
        logger.debug(f"generate_response: {self.user}, {self.refresh}, {self.access}")
        
        if self.user and self.refresh and self.access:
            self.response = JsonResponse({'message': 'Login successful'}, status=status.HTTP_200_OK)
            Cookies(self.response).set_cookie(self.ACCESS_TOKEN_NAME, self.access, self.ACCESS_TOKEN_MAX_AGE)
            Cookies(self.response).set_cookie(self.REFRESH_TOKEN_NAME, self.refresh, self.REFRESH_TOKEN_MAX_AGE)
        else:
            self.response = JsonResponse({'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

    def generate_response_with_tokens(self):
        if self.user and self.refresh and self.access:
            self.response = JsonResponse({
                    self.ACCESS_TOKEN_NAME: self.access,
                    self.REFRESH_TOKEN_NAME:self.refresh,
                }, status=status.HTTP_200_OK)
        else:
            self.response = JsonResponse({'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)