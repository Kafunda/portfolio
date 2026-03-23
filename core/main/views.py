from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Project, Service, Skill
from .forms import ContactForm

# Create your views here.


def home(request):

    project_list = Project.objects.all().order_by('id')
    paginator = Paginator(project_list, 3)  # 3 projets par page

    page_number = request.GET.get('page')
    projects = paginator.get_page(page_number)

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            nom = form.cleaned_data['nom']
            email = form.cleaned_data['email']
            sujet = form.cleaned_data['sujet']
            message = form.cleaned_data['message']
            contenu = f"""
            Nouveau message depuis ton portfolio
            Nom : {nom}
            Email : {email}
            Sujet : {sujet}
            Message :
            {message}
"""
            send_mail(
                subject=f"[Portfolio] {sujet}",
                message=contenu,
                from_email=None,
                recipient_list=['emmanuelkafunda01@gmail.com'],
                fail_silently=False,
            )

            messages.success(request, "Votre message a bien été envoyé.")
            return redirect('/#contact')
    else:
        form = ContactForm()


    return render(request, "main/home.html", {
        "projects": projects,
        "services": Service.objects.all(),
        "skills": Skill.objects.all(),
    })


def dashboard(request):
    return render(request, "main/dashboard.html", {
        "total_projects": Project.objects.count(),
        "projects": Project.objects.all(),
        "services": Service.objects.all(),
        "skills": Skill.objects.all(),
    })











