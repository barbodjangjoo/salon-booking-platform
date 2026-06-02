from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Availability
from .tasks import generate_slots


@receiver(post_save, sender=Availability)
def create_slots_after_availability_created(
    sender,
    instance,
    created,
    **kwargs
):
    if not created:
        return

    transaction.on_commit(
        lambda: generate_slots.delay(instance.id)
    )