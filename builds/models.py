from django.db import models

# Create your models here.

class ExteriorCategory(models.Model):
    """Exterior Categories"""
    title = models.CharField(max_length=50)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.title


class EngineCategory(models.Model):
    """Engine Categories"""
    title = models.CharField(max_length=50)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.title

class RunningCategory(models.Model):
    """Running Gear Categories"""
    title = models.CharField(max_length=50)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.title

class InteriorCategory(models.Model):
    """Interior Categories"""
    title = models.CharField(max_length=50)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.title