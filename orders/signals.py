# orders/signals.py

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch        import receiver
from django.core.mail       import send_mail
from twilio.rest           import Client

from .models import Order

# 1) Email confirmation on every new order
@receiver(post_save, sender=Order)
def send_order_confirmation(sender, instance, created, **kwargs):
    if not created:
        return

    subject = f"Order #{instance.id} Received"
    body    = (
        f"Hi {instance.first_name},\n\n"
        f"Thanks for your order! We’ll see you on "
        f"{instance.pickup_datetime:%Y-%m-%d %H:%M}.\n\n"
        "– The Fudge Kettle"
    )
    # In DEBUG this will print to console; in prod it uses your SMTP settings
    send_mail(subject, body, None, [instance.email])


# 2) SMS alert when order is created and in PRODUCTION
@receiver(post_save, sender=Order)
def send_sms_alert(sender, instance, created, **kwargs):
    if not created or settings.DEBUG:
        return

    client = Client(settings.TWILIO_SID, settings.TWILIO_AUTH)
    msg_body = (
        f"Hi {instance.first_name}, your order #{instance.id} "
        f"is confirmed for {instance.pickup_datetime:%Y-%m-%d %H:%M}."
    )
    client.messages.create(
        body=msg_body,
        from_=settings.TWILIO_FROM_NUMBER,
        to=instance.phone_number,    # make sure you’ve added this field
    )


