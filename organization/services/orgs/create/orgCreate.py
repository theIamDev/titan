from ....models.orgsModels import Organizations
from django.core.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework import status

class Create_orgs():
    def __init__(self, data):
        self.data = data

    def create(self):
        """Creates a new organization after validating the input data."""
        try:
            data = self._prepare_org_data()
            org = Organizations.objects.create(**data)
            return_response = {
                "body": {"message": "Organization created successfully", "organization_obj": org},
                "status": status.HTTP_201_CREATED
            }
        except ValidationError as e:
            return_response = {
                "body": {"error": str(e)},
                "status": status.HTTP_400_BAD_REQUEST
            }

        except Exception as e:
            return_response = {
                "body": {"error": "An unexpected error occurred in orgs create", "details": str(e)},
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR
            }

        return return_response

    def _prepare_org_data(self):
        """Validates and prepares organization data before creation."""
        required_fields = ['name']
        missing_fields = [field for field in required_fields if not self.data.get(field, "").strip()]

        if missing_fields:
            raise ValidationError(f"Missing required fields: {', '.join(missing_fields)}")

        return {
            'name': self.data['name'].strip(),
            'description': self.data.get('description', '').strip(),
        }
