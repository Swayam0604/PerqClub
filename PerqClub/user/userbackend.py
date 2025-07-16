from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

class EmailOrUsernameModelBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        user = None
        
        # Try to find user by email
        try:
            user = UserModel.objects.get(email=username)
        except UserModel.DoesNotExist:
            # Try to find user by username
            try:
                user = UserModel.objects.get(username=username)
            except UserModel.DoesNotExist:
                # Try to find user by phone number (handle multiple users with same phone)
                users_with_phone = UserModel.objects.filter(phone_number=username)
                if users_with_phone.exists():
                    # Try to authenticate each user with this phone number
                    for potential_user in users_with_phone:
                        if potential_user.check_password(password):
                            user = potential_user
                            break
        
        if user and user.check_password(password):
            return user
        return None