from django.db import models


class TwitterUsers(models.Model):
    name = models.CharField(max_length=200)
    comment = models.CharField(max_length=1000)

    def __str__(self):
        return self.comment

    def register(self):
        self.save()
