from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth import get_user_model, authenticate, login
from django.utils.safestring import mark_safe
from django.urls import reverse
from .signals import user_logged_in
User = get_user_model()
from .models import EmailActivation

class ReactivateEmailForm(forms.Form):
    email = forms.EmailField()

    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = EmailActivation.objects.email_exists(email)
        if not qs.exists():
            register_link = reverse('register')
            msg = """Этот адрес не существует, <a href="{link}">зарегистрироваться</a>?
            """.format(link=register_link)
            raise forms.ValidationError(mark_safe(msg))
        return email


class RegisterForm(forms.ModelForm):
    """
    A form for creating new users. Includes all the required
    fields, plus a repeated password.
    """

    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Подтверждение пароля', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'username', 'full_name')

    def clean_password2(self):
        # Check that the two password entries match
        password = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")
        if password and password2 and password != password2:
            raise forms.ValidationError("Пароли не совпадают")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(RegisterForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        user.is_active = False # send confirmation email via signals

        if commit:
            user.save()
        return user


class UserAdminChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('email', 'username', 'full_name', 'password', 'is_active', 'admin')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class LoginForm(forms.Form):
    email = forms.EmailField(label='Email')
    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, request, *args, **kwargs):
        self.request = request
        super(LoginForm, self).__init__(*args, **kwargs)

    def clean(self):
        request = self.request
        data = self.cleaned_data
        email = data.get('email')
        password = data.get('password')
        qs = User.objects.filter(email=email)
        if qs.exists():
            #user email is registered, check active/email activation
            not_active = qs.filter(is_active=False)
            if not_active.exists():
            #not active, check email activation
                link = reverse('resend-activation')
                reconfirm_msg = """ Перейдите по ссылке
                <a href="{resend_link}">для повторного подтверждения<a/>
                """.format(resend_link = link)
                confirm_email = EmailActivation.objects.filter(email=email)
                is_confirmable = confirm_email.confirmable().exists()
                if is_confirmable:
                    msg1 = 'Пожалуйста проверьте ваш почтовый ящик или ' + reconfirm_msg.lower()
                    # Please check your email to confirm your account or
                    raise forms.ValidationError(mark_safe(msg1))
                email_confirm_exists = EmailActivation.objects.email_exists(email).exists()
                if email_confirm_exists:
                    msg2 = 'Адрес не подтвержден. ' + reconfirm_msg
                    raise forms.ValidationError(mark_safe(msg2))
                if not is_confirmable and not email_confirm_exists:
                    raise forms.ValidationError('Этот пользователь не активирован')
        user = authenticate(request, username=email, password=password)
        if user is None:
            raise forms.ValidationError('Неверные данные')
        login(request, user)
        self.user = user
        return data
        # if user and user.is_active:
        #     login(request, user)
        #     self.user = user
        #     user_logged_in.send(user.__class__, instance=user, request=request)
        # else:
        #     reset_link = reverse('password_reset')
        #     register_link = reverse('register')
        #     activation_link = reverse('resend-activation')
        #     msg = """Incorrect credentials, try one of the following:
        #     <br><a href="{link1}">reset your password</a>
        #     <br><a href="{link2}">register</a>
        #     <br><a href="{link3}">activate your account</a>
        #     """.format(link1=reset_link, link2=register_link, link3=activation_link)
        #     raise forms.ValidationError(mark_safe(msg))

        # return data
