import datetime
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.

now = datetime.datetime.now()

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

class Domains(models.Model):
    """Domains for scraping"""
    class Attr(models.TextChoices):
        ID = '1', 'id'
        CLASS = '2', 'class'
    domain = models.CharField(max_length=50)
    price_element = models.CharField(max_length=50)
    attr = models.CharField(max_length=5, choices=Attr.choices, default='1')

    def __str__(self):
        return self.domain

class Exterior(models.Model):
    """Model for exterior items"""
    exterior_category = models.ForeignKey(ExteriorCategory, on_delete=models.PROTECT)
    link = models.URLField(max_length=500)
    price = models.FloatField(default=0)
    purchased = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)

class Engine(models.Model):
    """Model for engine items"""
    engine_category = models.ForeignKey(EngineCategory, on_delete=models.PROTECT)
    link = models.URLField(max_length=500)
    price = models.FloatField(default=0)
    purchased = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)

class Running(models.Model):
    """Model for running items"""
    running_category = models.ForeignKey(RunningCategory, on_delete=models.PROTECT)
    link = models.URLField(max_length=500)
    price = models.FloatField(default=0)
    purchased = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)

class Interior(models.Model):
    """Model for interior items"""
    interior_category = models.ForeignKey(InteriorCategory, on_delete=models.PROTECT)
    link = models.URLField(max_length=500)
    price = models.FloatField(default=0)
    purchased = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)

class Cars(models.Model):
    """Cars for a build"""
    make = models.CharField(max_length=30)
    model = models.CharField(max_length=30)
    trim = models.CharField(max_length=45)
    year = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1900),
            MaxValueValidator(now.year)
        ]
    )
    price = models.FloatField(default=0)
    purchased = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.make} {self.model} {self.trim}'

class Builds(models.Model):
    """Model for builds"""
    build_id = models.CharField(unique=True, editable=False, null=True, blank=True, max_length=32)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    price_hidden = models.BooleanField(default=False)
    total = models.FloatField()
    private = models.BooleanField(default=False)
    car = models.ForeignKey(Cars, on_delete=models.CASCADE)
    exterior_parts = models.ManyToManyField(Exterior, blank=True) 
    engine_parts = models.ManyToManyField(Engine, blank=True)
    running_gear_parts = models.ManyToManyField(Running, blank=True)
    interior_parts = models.ManyToManyField(Interior, blank=True)
    views = models.IntegerField(default=0)
    like_count = models.IntegerField(default=1)
    likes = models.ManyToManyField(User, related_name="%(class)s_likes", blank=True)
    dislike_count = models.IntegerField(default=0)
    dislikes = models.ManyToManyField(User, related_name="%(class)s_dislikes", blank=True)
    qrcode = models.ImageField(upload_to='qr_codes', null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('-id',)
