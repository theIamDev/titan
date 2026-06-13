from ....models.locationsModels import Locations
from django.core.exceptions import ValidationError
from rest_framework import status

class CreateLocations():
    def __init__(self, data):
        self.data = data

    def create(self):
        """Creates a new organization after validating the input data."""
        try:
            data = self._prepare_location_data()
            location = Locations.objects.create(**data)
            return_response = {
                "body": {"message": "Location created successfully", "location_obj": location},
                "status": status.HTTP_201_CREATED
            }
        except ValidationError as e:
            return_response = {
                "body": {"error": str(e)},
                "status": status.HTTP_400_BAD_REQUEST
            }

        except Exception as e:
            return_response = {
                "body": {"error": "An unexpected error occurred in location", "details": str(e)},
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR
            }

        return return_response

    def _prepare_location_data(self):
        """Validates and prepares organization data before creation."""
        required_fields = ['name']
        missing_fields = [field for field in required_fields if not self.data.get(field, "").strip()]

        if missing_fields:
            raise ValidationError(f"Missing required fields: {', '.join(missing_fields)}")

        return {
            'name': self.data['name'].strip(),
            'organization': self.data['organization'],
            'description': self.data.get('description', '').strip(),
            'address': self.data.get('address', '').strip(),
        }
