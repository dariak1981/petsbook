from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
from .forms import ContactForm
from .models import Guidance, Intro
from django.conf import settings
User = settings.AUTH_USER_MODEL
Profile = settings.AUTH_PROFILE_MODULE
from django.contrib.auth import get_user_model
User = get_user_model()


@login_required
def contact(request):
    intro = Intro.objects.first()
    form = ContactForm()

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():

            subject = form.cleaned_data.get('subject')
            from_email = request.user.email
            message = form.cleaned_data.get('message')
            name = request.user.full_name
            try:
                message_format = "Сообщение от пользователя {0}, {1}:\n\n{2}".format(name, from_email, message)

                msg = EmailMessage(
                    subject,
                    message_format,
                    to=['kda.cnc@gmail.com'],
                    from_email='from_email'
                )
                msg.send()

            except Exception as e:
                return render(request, "support/error.html")

        return render(request, 'support/contact_success.html')

    else:
        form = ContactForm()

    context = {
        'intro' : intro,
        'form' : form,
    }

    return render(request, 'support/contact.html', context)




@login_required
def guidance(request):
    guidance = Guidance.objects.all()

    context = {
        'guidance' : guidance,
    }

    return render(request, 'support/guidance.html', context)
