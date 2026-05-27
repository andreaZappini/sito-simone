from django.utils import timezone

from django.shortcuts import render, get_object_or_404, redirect
from .models import Biografia, Mostra, Opera, ImmagineOpera, VideoOpera
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib.auth import authenticate, login, logout
# Create your views here.

def home(request):
    ultima_opera = Opera.objects.order_by('-id').first() 
    return render(request, 'sitoArte/home.html', {'ultima_opera': ultima_opera})

def opere(request):
    opere = Opera.objects.all()
    return render(request, 'sitoArte/opere.html', {'opere': opere})

def biografia(request):
    biografia = Biografia.objects.first()
    return render(request, 'sitoArte/biografia.html', {'biografia': biografia})

def contatti(request):
    return render(request, 'sitoArte/contatti.html')

def mostre(request):
    oggi = timezone.localdate()

    in_programma = Mostra.objects.filter(data_inizio__gt=oggi).order_by('data_inizio')
    in_corso = Mostra.objects.filter(data_inizio__lte=oggi, data_fine__gte=oggi).order_by('data_inizio')
    passate = Mostra.objects.filter(data_fine__lt=oggi).order_by('-data_fine')

    return render(request, 'sitoArte/mostre.html', {
        'in_programma': in_programma,
        'in_corso': in_corso,
        'passate': passate,
    })

def dettaglio_mostra(request, pk):
    mostra = get_object_or_404(Mostra, pk=pk)
    return render(request, 'sitoArte/dettaglio_mostra.html', {'mostra': mostra})


def dettaglio_opera(request, pk):
    opera = get_object_or_404(Opera, pk=pk)
    return render(request, 'sitoArte/dettaglio_opera.html', {'opera': opera})

def owner_required(view_func):
    def wrapper(request, *args, **kwargs):

        if not request.user.is_authenticated:
            return HttpResponseForbidden("Accesso negato.")

        if request.user.username != 'simone':
            return HttpResponseForbidden("Devi essere autenticato per accedere a questa pagina.")
        
        return view_func(request, *args, **kwargs)
    return wrapper

@login_required(login_url='gestione/login/')
def dashboard(request):
    opere = Opera.objects.all()
    return render(request, 'sitoArte/dashboard.html', {'opere': opere})

@login_required(login_url='gestione/login/')
def nuova_opera(request):
    if request.method == "POST":
        titolo = request.POST['titolo']
        anno = request.POST['anno']
        descrizione = request.POST['descrizione']
        immaginePrincipale = request.FILES.get('immaginePrincipale')

        opera = Opera.objects.create(
            titolo=titolo,
            anno=anno,
            descrizione=descrizione,
            immaginePrincipale=immaginePrincipale
        )

        # immagini multiple
        for img in request.FILES.getlist('immagini'):
            ImmagineOpera.objects.create(opera=opera, immagine=img)

        # video multipli
        for vid in request.FILES.getlist('video'):
            VideoOpera.objects.create(opera=opera, video=vid)

        return redirect('dashboard')

    return render(request, 'sitoArte/nuova_opera.html')

@login_required(login_url='gestione/login/')
def modifica_opera(request, pk):
    opera = get_object_or_404(Opera, pk=pk)

    if request.method == "POST":
        opera.titolo = request.POST['titolo']
        opera.anno = request.POST['anno']
        opera.descrizione = request.POST['descrizione']

        if request.FILES.get('immaginePrincipale'):
            opera.immaginePrincipale = request.FILES['immaginePrincipale']

        opera.save()

        # aggiungi nuove immagini
        for img in request.FILES.getlist('immagini'):
            ImmagineOpera.objects.create(opera=opera, immagine=img)

        # aggiungi nuovi video
        for vid in request.FILES.getlist('video'):
            VideoOpera.objects.create(opera=opera, video=vid)

        return redirect('dashboard')

    return render(request, 'sitoArte/modifica_opera.html', {
        'opera': opera,
        'immagini': opera.immagini.all(),
        'video': opera.video.all()
    })

def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')  # torni direttamente alla dashboard
        else:
            return render(request, 'sitoArte/login.html', {
                'error': 'Credenziali non valide'
            })

    return render(request, 'sitoArte/login.html')

def logout_view(request):
    logout(request)
    return redirect('gestione_login')

