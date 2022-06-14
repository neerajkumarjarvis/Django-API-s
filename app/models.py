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



class SaralBooth(models.Model):
    id = models.BigAutoField(primary_key=True, auto_created=True)
    state = models.TextField(blank=True, null=True)
    ac = models.BigIntegerField(blank=True, null=True)
    ac_name = models.TextField(blank=True, null=True)
    booth_number = models.BigIntegerField(blank=True, null=True)
    booth_name = models.TextField(blank=True, null=True)
    saral_state_id = models.BigIntegerField(blank=True, null=True)
    saral_ac_id = models.BigIntegerField(blank=True, null=True)
    current_voters = models.BigIntegerField(blank=True, null=True)
    pm_targeted_votes = models.FloatField(blank=True, null=True)
    cm_targeted_votes = models.FloatField(blank=True, null=True)
    corrected_voters = models.BigIntegerField(blank=True, null=True)
    voter_list_url = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'saral_booth'


# class SaralBooth(models.Model):
#     id = models.BigIntegerField(primary_key=True)
#     state = models.TextField(blank=True, null=True)
#     ac = models.BigIntegerField(blank=True, null=True)
#     ac_name = models.TextField(blank=True, null=True)
#     booth_number = models.BigIntegerField(blank=True, null=True)
#     booth_name = models.TextField(blank=True, null=True)
#     saral_state_id = models.BigIntegerField(blank=True, null=True)
#     saral_ac_id = models.BigIntegerField(blank=True, null=True)
#     current_voters = models.BigIntegerField(blank=True, null=True)
#     pm_targeted_votes = models.FloatField(blank=True, null=True)
#     cm_targeted_votes = models.FloatField(blank=True, null=True)
#     corrected_voters = models.BigIntegerField(blank=True, null=True)
#     voter_list_url = models.TextField(blank=True, null=True)
#
#     class Meta:
#         managed = False
#         db_table = 'saral_booth'

class BjpVotes(models.Model):
    id = models.BigAutoField(primary_key=True,auto_created = True)
    booth = models.ForeignKey('SaralBooth', models.DO_NOTHING, blank=True, null=True,related_name='bjpvote')
    election_year = models.BigIntegerField(blank=True, null=True)
    election_type = models.TextField(blank=True, null=True)
    vote_ssecured_by_bjp = models.TextField(blank=True, null=True)
    bjp_position = models.BigIntegerField(blank=True, null=True)
    corrected_votes = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'bjp_votes'

class Ac(models.Model):
    id = models.BigIntegerField(primary_key=True)
    name = models.TextField(blank=True, null=True)
    number = models.BigIntegerField(blank=True, null=True)
    country_state= models.ForeignKey('State', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ac'


class State(models.Model):
    id = models.BigIntegerField(primary_key=True)
    name = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'state'

