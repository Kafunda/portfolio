from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib import messages
from django.core.paginator import Paginator
from django.conf import settings
from .models import Project, Service, Skill
from .forms import ContactForm

def home(request):
    # Pagination
    project_list = Project.objects.all().order_by('id')
    paginator = Paginator(project_list, 3)
    page_number = request.GET.get('page')
    projects = paginator.get_page(page_number)

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Extraction des données
            data = form.cleaned_data
            contenu = f"Nouveau message de {data['nom']} ({data['email']})\n\nSujet : {data['sujet']}\n\n{data['message']}"
            
            try:
                send_mail(
                    subject=f"[Portfolio] {data['sujet']}",
                    message=contenu,
                    from_email=None, # Utilise DEFAULT_FROM_EMAIL de settings.py
                    recipient_list=[settings.CONTACT_EMAIL],
                    fail_silently=False,
                )
                messages.success(request, "Votre message a bien été envoyé.")
                return redirect('/#contact')
            except Exception:
                messages.error(request, "Une erreur est survenue lors de l'envoi du message.")
    else:
        form = ContactForm()

    context = {
        "projects": projects,
        "services": Service.objects.all(),
        "skills": Skill.objects.all(),
        "total_projects": Project.objects.count(),
        "form": form,
    }
    
    return render(request, "main/home.html", context)