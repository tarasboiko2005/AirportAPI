from django.db import models
from django.conf import settings
from django.utils import timezone
from datetime import timedelta

class Order(models.Model):
    STATUS_CHOICES = [
        ('booked', 'Booked'),
        ('paid', 'Paid'),
        ('expired', 'Expired'),
        ('cancelled', 'Cancelled'),
    ]

    PAYMENT_CHOICES = [
        ('card', 'Card'),
        ('paypal', 'PayPal'),
        ('cash', 'Cash'),
    ]

    CURRENCY_CHOICES = [
        ('USD', 'US Dollar'),
        ('EUR', 'Euro'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='USD')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="booked")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    expires_at = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.pk and not self.expires_at:
            self.expires_at = timezone.now() + timedelta(minutes=15)
        super().save(*args, **kwargs)

    @property
    def is_expired(self):
        if self.status in ('paid', 'cancelled'):
            return False
        if self.expires_at and timezone.now() > self.expires_at:
            return True
        return False

    def __str__(self):
        return f"Order {self.pk or 'unsaved'} by {self.user}"

    class Meta:
        ordering = ['-created_at']