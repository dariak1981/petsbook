from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
User = settings.AUTH_USER_MODEL
Profile = settings.AUTH_PROFILE_MODULE
from django.http import HttpResponse, HttpResponseRedirect
from django.template import context
from django.urls import reverse
from django.views.generic.edit import FormMixin
from django.forms import models as forms_models
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login, get_user_model
from .signals import user_logged_in
from .forms import LoginForm, RegisterForm, ReactivateEmailForm
from django.views.generic import CreateView, FormView, DeleteView, View
from django.utils.http import is_safe_url
from django.utils.safestring import mark_safe
from mains.mixins import NextUrlMixin, RequestFormAttachMixin
from .models import EmailActivation

User = get_user_model()

class LoginView(NextUrlMixin, RequestFormAttachMixin, FormView):
    form_class = LoginForm
    success_url = 'user/dashboard'
    template_name = 'accounts/login.html'

    def form_valid(self, form):
        next_path = self.get_next_url()
        return redirect(next_path)


class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'accounts/register.html'
    success_url = '/accounts/login/'


class UserDeleteView(LoginRequiredMixin, DeleteView):
    model = User
    success_url = '/'

class AccountEmailActivateView(FormMixin, View):
    success_url = '/accounts/login/'
    form_class = ReactivateEmailForm
    key = None
    def get(self, request, key=None, *args, **kwargs):
        self.key = key
        if key is not None:
            qs = EmailActivation.objects.filter(key__iexact=key)
            confirm_qs = qs.confirmable()
            if confirm_qs.count() == 1:
                obj = qs.first()
                obj.activate()
                messages.success(request, "Адрес вашей почты подтвержден.")
                return redirect('login')
            else:
                activated_qs = qs.filter(activated=True)
                if activated_qs.exists():
                    reset_link = reverse('password_reset')
                    msg = """Ваш эмейл уже подтвержден.
                    Попробовать<a href="{link}"> сбросить пароль</a>?
                    """.format(link=reset_link)
                    messages.success(request, mark_safe(msg))
                    return redirect('login')
        context = {'form':self.get_form(), 'key':key}
        return render(request, 'accounts/activation-error.html', context)

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        msg = """Отправлена ссылка на активащию, пожалуйста проверьте почту."""
        request = self.request
        messages.success(request, msg)
        email = form.cleaned_data.get('email')
        obj = EmailActivation.objects.email_exists(email).first()
        user = obj.user
        new_activation = EmailActivation.objects.create(user=user, email=email)
        new_activation.send_activation()
        return super(AccountEmailActivateView, self).form_valid(form)

    def form_invalid(self, form):
        context = { 'form': form, 'key':self.key }
        return render(self.request, 'accounts/activation-error.html', context)
