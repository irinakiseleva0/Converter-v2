from django.db import models
from django.contrib.auth.models import User


class ConversionHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='conversions')
    from_currency = models.CharField(max_length=10)
    to_currency = models.CharField(max_length=10)
    amount = models.FloatField()
    converted_amount = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username}: {self.amount} {self.from_currency} -> {self.converted_amount} {self.to_currency}"
