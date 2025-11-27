from django.db import models

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