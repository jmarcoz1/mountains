from django.db import models


class Mountain(models.Model):
    DIFFICULTY_CHOICES = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard')
    ]
    name = models.CharField(max_length=100)
    description = models.TextField()
    location = models.CharField(max_length=100, default='Por definir')
    difficulty = models.CharField(max_length=10,
                                  choices=DIFFICULTY_CHOICES, default='medium')
    length = models.DecimalField(max_digits=10, decimal_places=2)
    elevation_gain = models.PositiveIntegerField()
    duration = models.DurationField()
    wikiloc = models.CharField(max_length=200)

    def __str__(self):
        return self.name
