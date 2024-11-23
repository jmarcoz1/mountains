from django.db import models
from .user import User
from .mountain import Mountain


class Hike(models.Model):
    participant = models.ForeignKey(User,
                                    to_field='username',
                                    on_delete=models.CASCADE,
                                    related_name='hike')
    mountain = models.ForeignKey(Mountain,
                                 on_delete=models.CASCADE,
                                 related_name='hike')
    hike_date = models.DateTimeField(auto_now_add=False)
    camping = models.BooleanField()

    def __str__(self):
        return f"Hike to {self.mountain}, \
        day {self.day}. Camping? {self.camping}."
