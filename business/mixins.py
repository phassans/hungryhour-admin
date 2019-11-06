from django.http import HttpResponseRedirect
from django.urls import reverse


class UserRequiredMixin:

    def dispatch(self, request, *args, **kwargs):
        print(request.session.get('userId'), '====')
        if request.session.get('userId'):
            return super(UserRequiredMixin, self).dispatch(request, *args, **kwargs)
        return HttpResponseRedirect(reverse('login'))
