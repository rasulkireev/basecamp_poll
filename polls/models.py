from django.db import models
from django.conf import settings

# Create your models here.

class Poll(models.Model):
    name = models.CharField(max_length = 50)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
    )
        
    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse('lists')
