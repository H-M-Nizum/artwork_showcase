from django.contrib.auth.models import BaseUserManager

#  Custom User Manager
class UserManager(BaseUserManager):
    def create_user(self, username, email, fullname, bio, password=None, password2=None):
        """
        Creates and saves a User with the given username, email, fullname, bio and password.
        """
        if not username:
            raise ValueError('User must have an username')

        user = self.model(
            username = username,
            email = self.normalize_email(email),
            fullname = fullname,
            bio = bio,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, fullname, bio, password=None):
        """
        Creates and saves a superuser with the given username, email, fullname, bio and password.
        """
        user = self.create_user(
            username=username,
            email = email,
            password = password,
            fullname = fullname,
            bio = bio,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user
