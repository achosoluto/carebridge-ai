"""Signals for core models."""

from django.db.models.signals import pre_save
from django.dispatch import receiver


@receiver(pre_save)
def update_metrics_on_save(sender, instance, **kwargs):
    """
    Update system metrics when relevant models are saved.
    This is a placeholder for more sophisticated metrics collection.
    """
    pass