from account.services.users.userServices import UserService

"""
Frontend mapping user structure - 

interface User {
  id: number;
  first_name: string;
  full_name: string;
  email: string;
  role: string;
  // account_name: string;
  organisation_id: number;
  organisation_name: string;
  location_id: number;
  location_name: string;
}

const mapUser = (user: any): User => ({
  id: user?.id ?? null,
  first_name: user?.first_name ?? user?.name ?? "Guest",
  full_name: user?.full_name ?? user?.name ?? "Guest",
  email: user?.email ?? "guest@example.com",
  role: user?.role ?? "guest",
  // account_name: user?.account_name ?? "Guest",
  organisation_id: user?.organisation_id ?? 0,
  organisation_name: user?.organisation_name ?? "Guest",
  location_id: user?.location_id ?? 0,
  location_name: user?.location_name ?? "Guest",
});
"""


def fetch_user(user):
    try:
        data = UserService.get_context_map_user(user,user.id)
        
        user_data = {
            "id":data.get('mapped_user_id'),
            "first_name":data.get('profile_first_name',"Guest"),
            "full_name":data.get('display_name',"Guest"),
            "email":data.get('email',"guest@example.com"),
            "role":data.get('user_role',"Guest"),
            "organisation_id":data.get('organization_id',0),
            "organisation_name":data.get('user_organization_name',"Guest"),
            "location_id":data.get('location_id',0),
            "location_name":data.get('user_location_name',"Guest")
        }
        return user_data
    except Exception as e:
        return {'error',str(e)}