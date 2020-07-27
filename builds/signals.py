from django.db.models.signals import pre_delete
from django.dispatch import receiver
from .models import Builds

@receiver(pre_delete, sender=Builds)
def delete_assoc_cateogries(sender, instance, **kwargs):
    print(instance)
    for item in instance.exterior_parts.all():
        item.delete()
    for item in instance.engine_parts.all():
        item.delete()
    for item in instance.running_gear_parts.all():
        item.delete()
    for item in instance.interior_parts.all():
        item.delete()
