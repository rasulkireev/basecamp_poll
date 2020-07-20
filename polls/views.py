from django.shortcuts import render
from django.urls import reverse_lazy
from django.conf import settings
from django.views.generic.edit import CreateView

from djstripe.models import Product

from .models import Poll
from .forms import CreatePollForm
from .utils import get_all_bc_projects

class CreatePollView(CreateView):
    form_class = CreatePollForm
    success_url = reverse_lazy('home')
    template_name = 'polls/new_poll.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['STRIPE_PUBLIC_KEY'] = settings.STRIPE_PUBLIC_KEY
        context['products'] = Product.objects.filter(livemode=settings.STRIPE_LIVE_MODE)
        context['basecamp_projects'] = get_all_bc_projects(self.request.user.email) 

        return context