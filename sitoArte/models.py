from django.db import models
from urllib.parse import quote
from simoneMartinotta import settings

# Create your models here.
class Opera(models.Model):
    titolo = models.CharField(max_length=255)
    anno = models.IntegerField()
    descrizione = models.TextField(blank =True, null=True)

    immaginePrincipale = models.ImageField(
        upload_to='opere/', #controlla a cosa si riferisce il path
        blank=True, 
        null=True)
    
    def __str__(self):
        return self.titolo
    

class ImmagineOpera(models.Model):
    opera = models.ForeignKey(
        Opera,
        related_name='immagini', 
        on_delete=models.CASCADE)
    
    immagine = models.ImageField(upload_to='immaginiOpere/')
    
    def __str__(self):
        return f"immagine di {self.opera.titolo} ({self.immagine.name})"
    
class VideoOpera(models.Model):
    opera = models.ForeignKey(
        Opera,
        related_name='video',
        on_delete=models.CASCADE)
    
    video = models.FileField(upload_to='videoOpere/')
    
    def __str__(self):
        return f"video di {self.opera.titolo}"


from django.utils import timezone

class Mostra(models.Model):
    titolo = models.CharField(max_length=255)
    descrizione = models.TextField(blank=True, null=True)
    data_inizio = models.DateField()
    data_fine = models.DateField()
    luogo = models.CharField(max_length=255)
    sito_luogo = models.URLField(blank=True, null=True)
    mappa_iframe = models.TextField(blank=True, null=True)


    @property
    def google_maps_place_url(self):
        return f"https://www.google.com/maps/search/?api=1&query={quote(self.luogo)}"

    @property
    def google_maps_embed_url(self):
        return (
            "https://www.google.com/maps/embed/v1/place"
            f"?key={settings.GOOGLE_MAPS_EMBED_API_KEY}"
            f"&q={quote(self.indirizzo)}"
        )
    class Meta:
        ordering = ['-data_inizio']
    
    def __str__(self):
        return self.titolo
    
    @property
    def stato(self):
        oggi = timezone.now().date()
        if self.data_inizio > oggi:
            return "Prossima"
        elif self.data_fine < oggi:
            return "Passata"
        else:
            return "In corso"

class Biografia(models.Model):
    nome = models.CharField(max_length=255)
    data_nascita = models.DateField()
    esperienza = models.TextField(blank=True, null=True)
    competenze = models.TextField(blank=True, null=True)
    obiettivi = models.TextField(blank=True, null=True)
    descrizione = models.TextField(blank=True, null=True)
    curriculum = models.FileField(upload_to='cvBiografie/', blank=True, null=True)

    def __str__(self):
        return self.nome