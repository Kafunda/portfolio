from django.db import models

# Create your models here.

class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='projects/', blank=True, null=True)
    category = models.CharField(max_length=100)
    lien = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.title


class Service(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.title


class Skill(models.Model):
    name = models.CharField(max_length=50)
    category = models.CharField(max_length=50)

    def __str__(self):
        return self.name