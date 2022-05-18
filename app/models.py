from django.db import models
from django.db import models

# Create your models here.


class Voter(models.Model):
    ac_no = models.SmallIntegerField()
    part_no = models.SmallIntegerField()
    section_no = models.SmallIntegerField()
    serial_no = models.SmallIntegerField()
    houseno = models.TextField(blank=True, null=True)
    name = models.TextField(blank=True, null=True)
    gender = models.TextField(blank=True, null=True)
    relname = models.TextField(blank=True, null=True)
    rtype = models.TextField(blank=True, null=True)
    epic_no = models.TextField(blank=True, null=True)
    contactno = models.TextField(blank=True, null=True)
    pincode = models.FloatField(blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
    year = models.TextField(blank=True, null=True)
    s_no = models.AutoField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'voters'

    def __str__(self):
        return self.name+" "+str(self.ac_no) +" " +str(self.part_no)  + " " +str(self.s_no)
