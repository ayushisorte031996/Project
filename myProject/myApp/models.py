from django.db import models

# Create your models here.

class Organization(models.Model):
    organization_id = models.AutoField(db_column = 'organization_id', primary_key=True)
    name = models.CharField(db_column = 'name', max_length=500, blank=True, null=True)
    description = models.TextField(db_column = 'description', blank=True, null=True)
    created_at = models.DateTimeField(db_column = 'created_at', blank=True, null=True)
    
    class Meta:
        managed = True
        db_table = 'Organization'


class Role(models.Model):
    id = models.AutoField(db_column = 'id', primary_key=True)
    name = models.CharField(db_column = 'name', max_length=500, blank=True, null=True)
    description = models.TextField(db_column = 'description', blank=True, null=True)
    organization_id = models.ForeignKey(Organization, models.CASCADE, db_column='organization_id', blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'Role'

class User(models.Model):
    id = models.AutoField(db_column = 'id', primary_key=True)
    username = models.CharField(db_column = 'username', max_length=200, blank=True, null=True)
    email = models.EmailField(unique=True)
    organization_id = models.ForeignKey(Organization, models.CASCADE, db_column='organization_id', blank=True, null=True)
    roles = models.ManyToManyField(Role)
    class Meta:
        managed = True
        db_table = 'User'