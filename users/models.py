from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext as _

class CustomUser(AbstractUser):
    customer = models.ForeignKey(
        'djstripe.Customer', null=True, blank=True, on_delete=models.CASCADE,
        help_text=_("The user's Stripe Customer object, if it exists")
    )
    subscription = models.ForeignKey(
        'djstripe.Subscription', null=True, blank=True, on_delete=models.CASCADE,
        help_text=_("The user's Stripe Subscription object, if it exists")
    )

    def __str__(self):
        return self.username