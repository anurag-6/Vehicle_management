
from django.db import models



COLOR_CHOICES = (

    ('Two Wheeler','2 Wheeler'),
    ('Three Wheeler', '3 Wheeler'),
    ('Four Wheeler','4 Wheeler')
   
)


class Vehicle(models.Model):
    vh_number = models.CharField(max_length=20,verbose_name="Vehicle Number",blank=False)
    vh_type = models.CharField(max_length=20,verbose_name="Vehicle Type", choices=COLOR_CHOICES,blank=False)
    vh_model = models.CharField(max_length=20,verbose_name="Vehicle Model",blank=False)
    vh_disc = models.TextField(verbose_name="Vehicle Discription",blank=False)

    class Meta:
        db_table = "Vehicles"
