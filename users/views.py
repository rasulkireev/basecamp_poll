import json
import stripe
import djstripe

from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.views.generic import TemplateView
from django.conf import settings
from django.http import JsonResponse
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.db import transaction

from .models import CustomUser
from .forms import CustomUserCreationForm
from djstripe.models import Product



class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'

class UpgradeView(TemplateView):
    template_name="users/upgrade.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['STRIPE_PUBLIC_KEY'] = settings.STRIPE_PUBLIC_KEY
        context['products'] = Product.objects.all()

        return context


stripe.api_key = settings.STRIPE_SECRET_KEY

@login_required
@require_POST
@transaction.atomic
def create_customer_and_subscription(request):
    """
    Create a Stripe Customer and Subscription object and map them onto the User object
    Expects the inbound POST data to look something like this:
    {
        'email': 'cory@saaspegasus.com',
        'payment_method': 'pm_1GGgzaIXTEadrB0y0tthO3UH',
        'plan_id': 'plan_GqvXkzAvxlF0wR',
    }
    """
    stripe.api_key = settings.STRIPE_SECRET_KEY

    # parse request, extract details, and verify assumptions
    request_body = json.loads(request.body.decode('utf-8'))
    
    email = request_body['customer_email']
    assert request.user.email == email  
    
    payment_method = request_body['payment_method']
    plan_id = request_body['plan_id']
    price_id = request_body['price_id']

    # first sync payment method to local DB to workaround 
    # https://github.com/dj-stripe/dj-stripe/issues/1125
    payment_method_obj = stripe.PaymentMethod.retrieve(payment_method)
    djstripe.models.PaymentMethod.sync_from_stripe_data(payment_method_obj)

    # create customer objects
    # This creates a new Customer in stripe and attaches the default PaymentMethod in one API call.
    customer = stripe.Customer.create(
      payment_method=payment_method,
      email=email,
      invoice_settings={
        'default_payment_method': payment_method,
      },
    )
    print("This is the created customer")
    print(customer)

    djstripe_customer = djstripe.models.Customer.sync_from_stripe_data(customer)

    # create subscription
    subscription = stripe.Subscription.create(
      customer=customer.id,
      items=[
        {
          'plan': plan_id,
          'price': plan_id,
        },
      ],
      expand=['latest_invoice.payment_intent'],
    )
    print("This is the created subsription")
    print(subscription)

    djstripe_subscription = djstripe.models.Subscription.sync_from_stripe_data(subscription)

    print(djstripe_customer)
    print(djstripe_subscription)

    # associate customer and subscription with the user
    request.user.customer = djstripe_customer
    request.user.subscription = djstripe_subscription
    request.user.save()

    # return information back to the front end
    data = {
        'customer': customer,
        'subscription': subscription
    }
    return JsonResponse(
        data=data,
    )