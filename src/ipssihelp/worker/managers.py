from django.contrib.auth.models import BaseUserManager


class WorkerUserManager(BaseUserManager):
    def create_user(self, email, password=None, is_staff=False, is_active=True, **extra_fields):
        """
        Creates and saves a superuser with the given email, first_name, last_name
        and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            is_active=is_active,
            is_staff=is_staff,
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        return self.create_user(
            email, password, is_staff=True, is_superuser=True, **extra_fields
        )
