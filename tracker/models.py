from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth import get_user_model

User = get_user_model()

class Track(models.Model):

    categories = [
        ("unsorted", "Unsorted"),
        ("education", "Education"),
        ("food", "Food")
    ]

    category = models.CharField(
        choices=categories, 
        default="unsorted", 
        null=False, 
        blank=False,
        max_length=10
        )
    amount = models.FloatField(
        validators=[MinValueValidator(100.0)], 
        null=False, 
        blank=False
        )
    date = models.DateField(
        auto_now_add=True, 
        null=False
        )
    
    user = models.ForeignKey(
        to=User, 
        blank=False, 
        null=False,
        related_name="transactions",
        on_delete=models.CASCADE
        )
    
    def save(self, *args, **kwargs):
        self.full_clean()

        return super().save(*args, **kwargs)