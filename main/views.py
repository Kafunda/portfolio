import logging
import requests

from django.shortcuts import render
from django.core.mail import send_mail
from django.contrib import messages
from django.core.paginator import Paginator
from django.conf import settings

from .models import Project, Service, Skill
from .forms import ContactForm

logger = logging.getLogger(__name__)


def get_client_ip(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        return x_forwarded_for.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR")


def verify_turnstile_token(token, remote_ip=None):
    try:
        response = requests.post(
            "https://challenges.cloudflare.com/turnstile/v0/siteverify",
            data={
                "secret": settings.TURNSTILE_SECRET_KEY,
                "response": token,
                "remoteip": remote_ip,
            },
            timeout=10,
        )
        response.raise_for_status()
        result = response.json()

        if not result.get("success", False):
            logger.warning("Turnstile validation failed: %s", result)

        return result.get("success", False)

    except requests.RequestException as e:
        logger.exception("Erreur lors de la vérification Turnstile: %s", e)
        return False


def home(request):
    project_list = Project.objects.all()
    paginator = Paginator(project_list, 3)
    page_number = request.GET.get("page")
    projects = paginator.get_page(page_number)

    form = ContactForm()

    if request.method == "POST":
        form = ContactForm(request.POST)
        turnstile_token = request.POST.get("cf-turnstile-response")
        client_ip = get_client_ip(request)

        if not turnstile_token:
            logger.warning("Turnstile token manquant depuis IP %s", client_ip)
            messages.error(request, "La vérification de sécurité a échoué.")
        elif not verify_turnstile_token(turnstile_token, client_ip):
            logger.warning("Captcha failed from IP %s", client_ip)
            messages.error(
                request,
                "La vérification de sécurité a échoué. Veuillez réessayer."
            )
        elif form.is_valid():
            data = form.cleaned_data
            contenu = (
                f"Nouveau message de {data['nom']} ({data['email']})\n\n"
                f"Sujet : {data['sujet']}\n\n"
                f"{data['message']}"
            )

            try:
                send_mail(
                    subject=f"[Portfolio] {data['sujet']}",
                    message=contenu,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[settings.CONTACT_EMAIL],
                    fail_silently=False,
                )
                messages.success(request, "Votre message a bien été envoyé.")
                form = ContactForm()
            except Exception:
                logger.exception("Erreur lors de l'envoi du mail")
                messages.error(
                    request,
                    "Une erreur est survenue lors de l'envoi du message."
                )

    context = {
        "projects": projects,
        "services": Service.objects.all(),
        "skills": Skill.objects.all(),
        "total_projects": Project.objects.count(),
        "form": form,
        "TURNSTILE_SITE_KEY": settings.TURNSTILE_SITE_KEY,
    }

    return render(request, "main/home.html", context)