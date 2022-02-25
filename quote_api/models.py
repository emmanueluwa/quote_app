from django.db import models

class Quote(models.Model):
    name = models.CharField(max_length=255)
    number = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    job = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.address
