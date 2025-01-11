from django.db import models

# Create your models here.
class Region(models.Model):
    name  =  models.CharField(max_length=200)



    def __str__(self):
        return self.name
    


class Districts(models.Model):
    region =  models.ForeignKey(Region, on_delete=models.PROTECT)
    name  =  models.CharField(max_length=200)

    def __str__(self):
        return self.name 
    
    