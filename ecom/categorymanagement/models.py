from django.db import models

# Create your models here.


class Brand(models.Model):
    brand_name = models.CharField(max_length = 50)
    is_listed = models.BooleanField(default = True)
    
    
    def __str__(self) -> str:
        return self.brand_name