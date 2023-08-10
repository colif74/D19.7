from django.shortcuts import render
from string import hexdigits
from django.contrib.auth.models import User, Group
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.views.generic import CreateView
import random
from django.conf import settings
from .models import OneTimeCode
from Game.forms import BaseRegisterForm


class BaseRegisterView(CreateView):
    model = User
    form_class = BaseRegisterForm
    template_name = 'account/signup.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = BaseRegisterForm()
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            common_group = Group.objects.get(name='common')
            common_group.user_set.add(user)

        return redirect('coder', request.POST['username'])


# Представление для активации зарегистрированного пользователя по коду на почту
class CodeRandomView(CreateView):
    template_name = 'account/coder.html'

    def get_context_data(self, **kwargs):
        user_ = self.kwargs.get('user')
        if not OneTimeCode.objects.filter(user=user_).exists():
            code = ''.join(random.sample(hexdigits, 5))
            OneTimeCode.objects.create(user=user_, code=code)
            user = User.objects.get(username=user_)
            send_mail(
                subject='Код активации',
                message=f'Код активации аккаунта: {code}',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
            )

    def post(self, request, *args, **kwargs):
        if 'code' in request.POST:
            user = request.path.split('/')[-1]
            if OneTimeCode.objects.filter(code=request.POST['code'], user=user).exists():
                User.objects.filter(username=user).update(is_active=True)
                OneTimeCode.objects.filter(code=request.POST['code'], user=user).delete()
            else:
                return render(self.request, 'account/invalid_code.html')
        return redirect('login')
